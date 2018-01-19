import json
import requests

champion_dict = {}

def extractInfoFromFile():

	file = json.load(open("cached_champs.txt", "r"))

	for item in file["keys"]:

		champ_id = item #champ id
		rephrase = file["keys"]
		champ_name = rephrase[item] #champ name
		image_full = file["data"][rephrase[item]]["image"]["full"]

		champion_dict[champ_id] = (champ_name, image_full)

	return champion_dict

'''def getData():
	link = "https://na1.api.riotgames.com/lol/static-data/v3/champions?locale=en_US&dataById=false&tags=all&api_key=RGAPI-9409948e-b9b5-4253-8fd7-5506e4c0f2bd"
	content = requests.get(url).content
	file = open("cached_champions.txt", "w")
	file.write(content)
'''

extractInfoFromFile()
