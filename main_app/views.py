from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import NameForm
from django.template import loader

import requests
import json
import sys
import os
from .champion import extractChampsFromFile
from .spell import extractSpellsFromFile

KEY_PHRASE = "?api_key=RGAPI-718bdc21-2ff6-4678-9d8a-81a2cc0eed83"
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

			print(data)

			return HttpResponse(template.render(data, request))
	else:

		form = NameForm()
		return render(request, 'main_app/detail.html', {'form':form})


def getData(url):
	content = requests.get(url).content
	return content


def returnRankedInfo(summonerId):

	return_string = ""
	ranked_info = getData(STARTER + "lol/league/v3/positions/by-summoner/" + str(summonerId) + KEY_PHRASE)

	print(ranked_info)

	for queue in json.loads(ranked_info):

		if game_dict[queue["queueType"]] == "Solo/Duo":
			return {"TIER": queue["tier"], "RANK": queue["rank"], "LP": queue["leaguePoints"], "WINS": queue["wins"], "LOSSES": queue["losses"]}

	return None

def main(summoner_name):

	spells = extractSpellsFromFile()
	champions = extractChampsFromFile()

	banned_champs = []

	url = STARTER + "lol/summoner/v3/summoners/by-name/" + summoner_name + KEY_PHRASE
	data = getData(url)
	dic = json.loads(data)
	game_data = json.loads(getData(STARTER + "lol/spectator/v3/active-games/by-summoner/" + str(dic["id"]) + KEY_PHRASE))

	game_data_dic = {"MODE": game_data["gameMode"], "TYPE": game_data["gameType"], "CONFIG": game_modes[game_data["gameQueueConfigId"]]}

	for banned_champ in game_data["bannedChampions"]:
		banned_champs.append((champions[banned_champ["championId"]])[1])

	team1 = []
	team2 = []

	count = 1

	for par in game_data["participants"]:

		ranked_data = returnRankedInfo(par["summonerId"])

		summoner = {"NAME": par["summonerName"], "CHAMP": champions[par["championId"]][0], "SPELL1": (spells[par["spell1Id"]])[1], "SPELL2": (spells[par["spell2Id"]])[1], "RANKED": ranked_data}

		if(count <= 5):
			team2.append(summoner)
		else:
			team1.append(summoner)

		count+=1


	game_data_dic["TEAM1"] = team1
	game_data_dic["TEAM2"] = team2
	game_data_dic["BANNED"] = banned_champs

	return game_data_dic



