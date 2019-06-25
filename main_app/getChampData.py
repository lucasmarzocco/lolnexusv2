import requests
import json

url = "http://ddragon.leagueoflegends.com/cdn/9.11.1/data/en_US/champion.json"

def getData(url):
	file = open("cached_champs.txt", "w")
	content = requests.get(url).content
	file.write(content)

getData(url)

#current version: 9.11.1 - June 9 2019
#champion/summoner  = champs / spells


#https://ddragon.leagueoflegends.com/api/versions.json - CHECK THIS FOR NEW VERSIONS!!!!