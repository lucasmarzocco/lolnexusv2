import json
import requests

champion_dict = {}

def extractChampsFromFile():

	file = json.load(open("/Users/lucasmarzocco/Desktop/lolnexusv2/main_app/cached_champs.txt", "r"))

	for item in file["data"]:

		champ_name = item
		rename = file["data"]
		champ_data = rename[champ_name]
		champ_id = champ_data["key"]
		image_full = champ_data["image"]["full"]

		champion_dict[int(champ_id)] = (champ_name, image_full)

		print(champion_dict)

	return champion_dict


	'''def getData():
	link = "https://na1.api.riotgames.com/lol/static-data/v3/champions?locale=en_US&dataById=false&tags=all&api_key=RGAPI-f7094294-8236-4b26-a369-09089e9fcf7d"
	content = requests.get(link).text
	file = open("cached_champs.txt", "w")
	file.write(content)'''


extractChampsFromFile()
