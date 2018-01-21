from bs4 import BeautifulSoup
from pprint import pprint
import requests
import json
import csv

def csv_writer(params, values_lists, path):
    with open(path, "w") as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
              
        writer.writerow(params)
        
        for line in values_lists:
            writer.writerow(line)

country = 'Spain'
years = [year for year in range(1995, 2017)]
column_names = ['Name', 'Matches' ,'Won', 'Lost', 'Draw', 'GF', 'GA', 'Points', 'PPM']


headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}
base_url = 'https://www.transfermarkt.com/laliga/tabelle/wettbewerb/ES1?saison_id='

for year in years:
	rows = []
	url = base_url + str(year)
	outfile = '../data/Standings/' + country + '/' + str(year) + '.csv'

	request = requests.get(url, headers=headers)
	html_data = request.text
	soup = BeautifulSoup(html_data, 'lxml')

	table_div = soup.find("div", { "class" : "responsive-table" })
	table = table_div.find("table").find("tbody")

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

			row_vals.append(name)
			row_vals.append(matches)
			row_vals.append(won)
			row_vals.append(lost)
			row_vals.append(draw)
			row_vals.append(goals_for)
			row_vals.append(goals_against)
			row_vals.append(points)
			row_vals.append(points/matches)

			rows.append(row_vals)

	csv_writer(column_names, rows, outfile)