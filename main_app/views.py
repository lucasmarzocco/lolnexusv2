from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import NameForm
from django.template import loader

import requests
import json

KEY_PHRASE = "?api_key=RGAPI-dd25a015-e140-4f33-8551-385d62e85808"
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

def championSetUp():

	champ_dict = {}

	champ_data = getData(STARTER + "lol/static-data/v3/champions" + KEY_PHRASE)

	for data_item in json.loads(champ_data)["data"]:

		champs = json.loads(champ_data)["data"]
		champ_dict[champs[data_item]["id"]] = champs[data_item]["name"]

	return champ_dict

def spellSetUp():

	spell_dict = {}

	spell_data = getData(STARTER + "/lol/static-data/v3/summoner-spells" + KEY_PHRASE)

	for data_item in json.loads(spell_data)["data"]:

		spells = json.loads(spell_data)["data"]
		spell_dict[spells[data_item]["id"]] = spells[data_item]["name"]

	return spell_dict

def returnRankedInfo(summonerId):

	return_string = ""
	ranked_info = getData(STARTER + "lol/league/v3/positions/by-summoner/" + str(summonerId) + KEY_PHRASE)

	for queue in json.loads(ranked_info):
		return_string += game_dict[queue["queueType"]] + " " + queue["tier"] + " " + queue["rank"] + " (" + str(queue["leaguePoints"]) + " LP) " + str(queue["wins"]) + "-" + str(queue["losses"]) + "\n"

	return return_string

def main(summoner_name):

	spells = spellSetUp()
	champions = championSetUp()

	url = STARTER + "lol/summoner/v3/summoners/by-name/" + summoner_name + KEY_PHRASE
	data = getData(url)
	dic = json.loads(data)
	game_data = json.loads(getData(STARTER + "lol/spectator/v3/active-games/by-summoner/" + str(dic["id"]) + KEY_PHRASE))

	game_data_dic = {"MODE": game_data["gameMode"], "TYPE": game_data["gameType"], "CONFIG": game_modes[game_data["gameQueueConfigId"]]}

	team1 = []
	team2 = []

	count = 1

	for par in game_data["participants"]:

		spell1 = ""
		spell2 = ""

		if spells[par["spell1Id"]] == "Ignite":
			spell1 = "Dot"
		else:
			spell1 = spells[par["spell1Id"]]

		if spells[par["spell2Id"]] == "Ignite":
			spell2 = "Dot"
		else:
			spell2 = spells[par["spell2Id"]]


		summoner = {"NAME": par["summonerName"], "CHAMP": champions[par["championId"]], "SPELL1": spell1, "SPELL2": spell2}

		if(count <= 5):
			team2.append(summoner)
		else:
			team1.append(summoner)

		count+=1

		#returnRankedInfo(par["summonerId"])

	game_data_dic["TEAM1"] = team1
	game_data_dic["TEAM2"] = team2

	return game_data_dic









