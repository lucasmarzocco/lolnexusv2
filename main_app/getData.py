import requests
link = "https://na1.api.riotgames.com/lol/static-data/v3/summoner-spells?locale=en_US&dataById=false&tags=all&api_key=RGAPI-9409948e-b9b5-4253-8fd7-5506e4c0f2bd"

def getData(url):
	content = requests.get(url).content
	return content

file = open("cached_spells.txt", "w")
file.write(getData(link))