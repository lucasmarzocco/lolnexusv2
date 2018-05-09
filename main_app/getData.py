import requests
from keys import return_key

link = "https://na1.api.riotgames.com/lol/static-data/v3/summoner-spells?locale=en_US&dataById=false&tags=all&api_key=" + return_key()

#summoner-spells
#champions

def getData(url):
	content = requests.get(url).content
	return content



file = open("cached_spells.txt", "w")
file.write(getData(link))