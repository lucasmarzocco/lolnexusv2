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


def returnRankedInfo(summonerId, key, version):
	return_string = ""
	ranked_info = getData("https://na1.api.riotgames.com/lol/league/" + version + "/positions/by-summoner/" + str(summonerId) + key)

	for queue in json.loads(ranked_info):

		if game_dict[queue["queueType"]] == "Solo/Duo":
			return {"TIER": queue["tier"], "RANK": queue["rank"], "LP": queue["leaguePoints"], "WINS": queue["wins"], "LOSSES": queue["losses"]}

	return "Unranked"

def getAccountID(summonerId, key, version):

	summoner_info = json.loads(getData("https://na1.api.riotgames.com/lol/summoner/" + version + "/summoners/" + str(summonerId) + key))
	return summoner_info["accountId"]


def returnLastGame(summonerId, champs, key, version):

	match_game_info = json.loads(getData("https://na1.api.riotgames.com/lol/match/" + version + "/matchlists/by-account/" + str(getAccountID(summonerId, key, version)) + key))

	last_match = match_game_info["matches"][0]
	lane = last_match["lane"]
	champ_id = last_match["champion"]
	queue = last_match["queue"]
	game_id = last_match["gameId"]

	last_match_info = json.loads(getData("https://na1.api.riotgames.com/lol/match/" + version + "/matches/" + str(game_id) + key))

	position = 0
	won = ""

	for participant in last_match_info["participantIdentities"]:
		if getAccountID(summonerId, key, version) == participant["player"]["accountId"]:
			position = participant["participantId"]


	for part in last_match_info["participants"]:

		if position == part["participantId"]:

			win = part["stats"]["win"]
			kills = part["stats"]["kills"]
			deaths = part["stats"]["deaths"]
			assists = part["stats"]["assists"]

			if win:
				won = "Won"
			else:
				won = "Lost"
			
			return {"LANE": lane, "CHAMP": champs[champ_id][1], "QUEUE": game_modes[queue], "WON": won, "KILLS": kills, "DEATHS": deaths, "ASSISTS": assists}

	return None


def main(summoner_name):

	spells = extractSpellsFromFile()
	champions = extractChampsFromFile()

	KEY_PHRASE = ""
	VERSION = ""

	with open('/Users/lmarzocc/Desktop/lolnexusv2/main_app/config.json') as json_file:  
		data = json.load(json_file)
		KEY_PHRASE = data["API_KEY"]
		VERSION = data["VERSION"]

	banned_champs = []

	user = json.loads(getData("https://na1.api.riotgames.com/lol/summoner/" + VERSION + "/summoners/by-name/" + summoner_name + KEY_PHRASE))

	if checkIfErrorCodesAreTrue(user)[0]:
		return checkIfErrorCodesAreTrue(user)

	game_data = json.loads(getData("https://na1.api.riotgames.com/lol/spectator/" + VERSION + "/active-games/by-summoner/" + str(user["id"]) + KEY_PHRASE))

	if checkIfErrorCodesAreTrue(game_data)[0]:
		return checkIfErrorCodesAreTrue(game_data)

	game_data_dic = {"MODE": game_data["gameMode"], "TYPE": game_data["gameType"], "CONFIG": game_modes[game_data["gameQueueConfigId"]]}

	for banned_champ in game_data["bannedChampions"]:
		if banned_champ["championId"] != (-1):
			banned_champs.append((champions[banned_champ["championId"]])[1])

	team1 = []
	team2 = []

	count = 1

	for par in game_data["participants"]:

		ranked_data = returnRankedInfo(par["summonerId"], KEY_PHRASE, VERSION)
		last_game = returnLastGame(par["summonerId"], champions, KEY_PHRASE, VERSION)

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


