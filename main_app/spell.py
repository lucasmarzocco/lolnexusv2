import json
import requests

spell_dict = {}

def extractSpellsFromFile():

	file = json.load(open("/Users/lmarzocc/Desktop/lolnexusv2/main_app/cached_spells.txt", "r"))

	for item in file["data"]:

		spell_name = item
		rename = file["data"]
		spell_data = rename[spell_name]
		spell_id = spell_data["key"]
		image_full = spell_data["image"]["full"]

		spell_dict[int(spell_id)] = (spell_name, image_full)

	return spell_dict

extractSpellsFromFile()