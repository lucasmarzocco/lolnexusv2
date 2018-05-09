import requests
import json
from keys import return_key

KEY_PHRASE = "?api_key=" + return_key()
STARTER = "https://na1.api.riotgames.com/"
champ_dict = {}
spell_dict = {}
game_dict = {"RANKED_SOLO_5x5": "Solo/Duo", "RANKED_FLEX_SR": "Flex SR", "RANKED_FLEX_TT": "Flex TT"}
game_modes = {400: "5v5 Draft", 420: "5v5 Ranked Solo/Duo", 430: "5v5 Blind", 440: "5v5 Ranked Flex", 450: "5v5 ARAM"}

def getData(url):
	content = requests.get(url).content
	return content

def championSetUp():

	global champ_dict

	champ_data = getData(STARTER + "lol/static-data/v3/champions" + KEY_PHRASE)

	for data_item in json.loads(champ_data)["data"]:

		champs = json.loads(champ_data)["data"]
		champ_dict[champs[data_item]["id"]] = champs[data_item]["name"]

def spellSetUp():

	global spell_dict

	spell_data = getData(STARTER + "/lol/static-data/v3/summoner-spells" + KEY_PHRASE)

	for data_item in json.loads(spell_data)["data"]:

		spells = json.loads(spell_data)["data"]
		spell_dict[spells[data_item]["id"]] = spells[data_item]["name"]

def returnRankedInfo(summonerId):

	global game_dict
	return_string = ""
	ranked_info = getData(STARTER + "lol/league/v3/positions/by-summoner/" + str(summonerId) + KEY_PHRASE)

	for queue in json.loads(ranked_info):
		return_string += game_dict[queue["queueType"]] + " " + queue["tier"] + " " + queue["rank"] + " (" + str(queue["leaguePoints"]) + " LP) " + str(queue["wins"]) + "-" + str(queue["losses"]) + "\n"

	return return_string

def main():

	global champ_dict
	global spell_dict
	global game_modes

	return_string = ""

	spellSetUp()
	championSetUp()
	#user_name = str(raw_input("What is your username?\n"))
	url = STARTER + "lol/summoner/v3/summoners/by-name/" + sys.argv[1] + KEY_PHRASE
	data = getData(url)
	dic = json.loads(data)
	game_data = json.loads(getData(STARTER + "lol/spectator/v3/active-games/by-summoner/" + str(dic["id"]) + KEY_PHRASE))

	return_string += "GAME MODE: " + game_data["gameMode"] + "\n"
	return_string += "GAME TYPE: " + game_data["gameType"] + "\n"
	return_string += "GAME CONFIG: " + game_modes[game_data["gameQueueConfigId"]] + "\n"

	count = 0
	team = 1

	for par in game_data["participants"]:

		if count == 0: return_string += "TEAM: " + str(team) + "\n"
		return_string += par["summonerName"] + " |  " + champ_dict[par["championId"]] + " |  " + spell_dict[par["spell1Id"]] + "/" + spell_dict[par["spell2Id"]] + "\n"
		return_string += returnRankedInfo(par["summonerId"])

		count+=1

		if count == 5:
			team +=1
			count = 0

			if team == 2:
				return_string += "-----------------------------------------------------------------------------------------------------------\n"


main()