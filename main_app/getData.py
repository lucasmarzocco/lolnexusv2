import requests
link = "http://ddragon.leagueoflegends.com/cdn/8.24.1/data/en_US/summoner.json"
def getData(url):
	content = requests.get(url).content
	return content

file = open("cached_spells.txt", "w")
file.write(getData(link))

#current version: 8.24.1 - Jan 8 2019