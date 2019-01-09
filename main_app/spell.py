import json
import requests

spell_dict = {}

def extractSpellsFromFile():

	file = json.load(open("/Users/lucasmarzocco/Desktop/lolnexusv2/main_app/cached_spells.txt", "r"))

	for item in file["data"]:

		spell_name = item
		rename = file["data"]
		spell_data = rename[spell_name]
		spell_id = spell_data["key"]
		image_full = spell_data["image"]["full"]

		spell_dict[int(spell_id)] = (spell_name, image_full)

	return spell_dict

'''def getData():
	link = "https://na1.api.riotgames.com/lol/static-data/v3/summoner-spells?locale=en_US&dataById=false&tags=all&api_key=RGAPI-9409948e-b9b5-4253-8fd7-5506e4c0f2bd"
	content = requests.get(url).content
	file = open("cached_spells.txt", "w")
	file.write(content)
'''

extractSpellsFromFile()