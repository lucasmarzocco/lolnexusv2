import json
import requests

spell_dict = {}

def extractInfoFromFile():

	file = json.load(open("cached_spells.txt", "r"))

	for item in file["data"]:

		rephrase = file["data"]
		spell_id = rephrase[item]["id"]
		spell_name = rephrase[item]["name"]
		image_full = rephrase[item]["image"]["full"]

		spell_dict[spell_id] = (spell_name, image_full)

	return spell_dict

'''def getData():
	link = "https://na1.api.riotgames.com/lol/static-data/v3/summoner-spells?locale=en_US&dataById=false&tags=all&api_key=RGAPI-9409948e-b9b5-4253-8fd7-5506e4c0f2bd"
	content = requests.get(url).content
	file = open("cached_spells.txt", "w")
	file.write(content)
'''

extractInfoFromFile()