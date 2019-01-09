from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import NameForm
from django.template import loader

import requests
import json
import sys
import time
import os
from .champion import extractChampsFromFile
from .spell import extractSpellsFromFile

KEY_PHRASE = "?api_key=RGAPI-f7094294-8236-4b26-a369-09089e9fcf7d"
STARTER = "https://na1.api.riotgames.com/"
game_dict = {"RANKED_SOLO_5x5": "Solo/Duo", "RANKED_FLEX_SR": "Flex SR", "RANKED_FLEX_TT": "Flex TT"}
game_modes = {400: "5v5 Draft", 420: "5v5 Ranked Solo/Duo", 430: "5v5 Blind", 440: "5v5 Ranked Flex", 450: "5v5 ARAM"}

def get_name(request):

	if request.method == 'POST':
		
		form = NameForm(request.POST)
	
		if form.is_valid():

			template = loader.get_template('main_app/form_det.html')
			context = {'summoner_name' : form.cleaned_data['summoner_name']}

			data = main(form.cleaned_data['summoner_name'])

			if(data[0] == True):
				return HttpResponse(loader.get_template('main_app/error.html').render({"error":data[1]}, request))

			else:
				return HttpResponse(template.render(data[1], request))
	else:

		form = NameForm()
		return render(request, 'main_app/detail.html', {'form':form})


def getData(url):
	time.sleep(1.2)
	content = requests.get(url).content
	return content


def returnRankedInfo(summonerId):

	return_string = ""
	ranked_info = getData(STARTER + "lol/league/v3/positions/by-summoner/" + str(summonerId) + KEY_PHRASE)

	for queue in json.loads(ranked_info):

		if game_dict[queue["queueType"]] == "Solo/Duo":
			return {"TIER": queue["tier"], "RANK": queue["rank"], "LP": queue["leaguePoints"], "WINS": queue["wins"], "LOSSES": queue["losses"]}

	return None

def getAccountID(summonerId):

	summoner_info = json.loads(getData(STARTER + "lol/summoner/v3/summoners/" + str(summonerId) + KEY_PHRASE))
	return summoner_info["accountId"]


def returnLastGame(summonerId, champs):

	print("Account ID: " + str(getAccountID(summonerId)))

	print(champs)

	match_game_info = json.loads(getData(STARTER + "lol/match/v3/matchlists/by-account/" + str(getAccountID(summonerId)) + KEY_PHRASE))

	print(match_game_info)

	last_match = match_game_info["matches"][0]
	lane = last_match["lane"]
	champ_id = last_match["champion"]
	queue = last_match["queue"]
	game_id = last_match["gameId"]

	print("GAME ID: " + str(game_id))

	last_match_info = json.loads(getData(STARTER + "lol/match/v3/matches/" + str(game_id) + KEY_PHRASE))

	position = 0
	won = ""

	for participant in last_match_info["participantIdentities"]:
		if getAccountID(summonerId) == participant["player"]["accountId"]:
			position = participant["participantId"]


	for part in last_match_info["participants"]:

		if position == part["participantId"]:

			win = part["stats"]["win"]
			kills = part["stats"]["kills"]
			deaths = part["stats"]["deaths"]
			assists = part["stats"]["assists"]

			if win:
				won = "WON"
			else:
				won = "LOST"

			print(lane)
			print(champ_id)
			print(queue)
			
			return {"LANE": lane, "CHAMP": champs[champ_id][1], "QUEUE": game_modes[queue], "WON": won, "KILLS": kills, "DEATHS": deaths, "ASSISTS": assists}

	return None


def main(summoner_name):

	spells = extractSpellsFromFile()
	champions = extractChampsFromFile()

	banned_champs = []

	user = json.loads(getData(STARTER + "lol/summoner/v3/summoners/by-name/" + summoner_name + KEY_PHRASE))

	if checkIfErrorCodesAreTrue(user)[0]:
		return checkIfErrorCodesAreTrue(user)

	game_data = json.loads(getData(STARTER + "lol/spectator/v3/active-games/by-summoner/" + str(user["id"]) + KEY_PHRASE))

	if checkIfErrorCodesAreTrue(game_data)[0]:
		return checkIfErrorCodesAreTrue(game_data)

	game_data_dic = {"MODE": game_data["gameMode"], "TYPE": game_data["gameType"], "CONFIG": game_modes[game_data["gameQueueConfigId"]]}

	for banned_champ in game_data["bannedChampions"]:
		banned_champs.append((champions[banned_champ["championId"]])[1])

	team1 = []
	team2 = []

	count = 1

	for par in game_data["participants"]:

		ranked_data = returnRankedInfo(par["summonerId"])
		last_game = returnLastGame(par["summonerId"], champions)

		summoner = {"NAME": par["summonerName"], "CHAMP": champions[par["championId"]][0], "SPELL1": (spells[par["spell1Id"]])[1], "SPELL2": (spells[par["spell2Id"]])[1], "RANKED": ranked_data, "LAST": last_game}

		if(count <= 5):
			team2.append(summoner)
		else:
			team1.append(summoner)

		count+=1


	game_data_dic["TEAM1"] = team1
	game_data_dic["TEAM2"] = team2
	game_data_dic["BANNED"] = banned_champs

	return (False, game_data_dic)
	

def checkIfErrorCodesAreTrue(game_data):

	if "status" not in game_data:
		return (False, "")

	elif game_data["status"]["status_code"] == 400:
		return (True, "Bad Request")

	elif game_data["status"]["status_code"] == 403:
		return (True, "Access Forbidden")

	elif game_data["status"]["status_code"] == 404:
		return (True, "User not in a game or can't be found")

	elif game_data["status"]["status_code"] == 429:
		return (True, "Rate limit exceeded")

	else:
		return (False, "")


