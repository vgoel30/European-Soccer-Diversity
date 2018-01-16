from bs4 import BeautifulSoup
from pprint import pprint
import requests

main_url = "https://www.transfermarkt.com"
base_url = "https://www.transfermarkt.com/premier-league/startseite/wettbewerb/GB1/plus/?saison_id="
teams = 20
years = [year for year in range(2000,2017)]

for year in years:
	url = base_url + str(year)
	headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}
	request = requests.get(url, headers=headers)
	print(url)
	data = request.text
	soup = BeautifulSoup(data, 'lxml')

	odd = soup.findAll("tr", {"class": "odd"})
	odd = odd[0:10]
	even = soup.findAll("tr", {"class": "even"})
	even = even[0:10]

	file_name = "../data/URLs/England/" + str(year) + ".txt"

	with open(file_name, 'w') as out_file:

		for team in odd:
			team_url = team.find("a", {"class": "vereinprofil_tooltip"})['href']
			out_file.write(team_url + '\n')
			pprint(main_url + team_url)

		for team in even:
			team_url = team.find("a", {"class": "vereinprofil_tooltip"})['href']
			out_file.write(team_url + '\n')
			pprint(main_url + team_url)