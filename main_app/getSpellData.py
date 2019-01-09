import requests
import json

url = "http://ddragon.leagueoflegends.com/cdn/8.24.1/data/en_US/summoner.json"

def getData(url):
	file = open("cached_spells.txt", "w")
	content = requests.get(url).content
	file.write(content)

getData(url)
#current version: 8.24.1 - Jan 8 2019
#champion/summoner  = champs / spells