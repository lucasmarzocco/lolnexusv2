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

	return champion_dict

extractChampsFromFile()
