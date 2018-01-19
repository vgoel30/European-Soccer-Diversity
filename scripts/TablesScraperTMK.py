from bs4 import BeautifulSoup
from pprint import pprint
import requests
import json

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}
url = 'https://www.transfermarkt.com/premier-league/tabelle/wettbewerb/GB1/saison_id/2000'

request = requests.get(url, headers=headers)
html_data = request.text
soup = BeautifulSoup(html_data, 'lxml')

table_div = soup.find("div", { "class" : "responsive-table" })
table = table_div.find("table").find("tbody")

rows = []

for row in table.findAll('tr'):
	row_vals = []
	cells = row.findAll('td')
	if len(cells) > 0:
		#name
		name_url = (cells[2].find("a", {"class" : "vereinprofil_tooltip"}))['href']
		name = name_url.split('/')[1]
		pprint(name)

		#matches played
		matches = int(cells[3].getText())
		pprint(matches)

		#matches won
		won = int(cells[4].getText())
		pprint(won)

		#matches drawn
		draw = int(cells[5].getText())
		pprint(draw)

		#mathces lost
		lost = int(cells[6].getText())
		pprint(lost)

		#goals
		goals = cells[7].getText()
		goals_for = int(goals.split(':')[0])
		goals_against = int(goals.split(':')[1])
		
		#points
		points = int(cells[9].getText())
		pprint(points)

		row_vals.append(name)
		row_vals.append(won)
		row_vals.append(lost)
		row_vals.append(draw)
		row_vals.append(goals_for)
		row_vals.append(goals_against)
		row_vals.append(points)
		row_vals.append(points/matches)

		rows.append(row_vals)

		pprint(row_vals)

#pprint(table)