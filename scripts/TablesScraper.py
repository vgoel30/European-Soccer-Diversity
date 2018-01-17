from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from pprint import pprint
import requests
import csv

def csv_writer(params, values_lists, path):
    with open(path, "w") as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
              
        writer.writerow(params)
        
        for line in values_lists:
            writer.writerow(line)


country = 'France'
seasons = ['{}_{}/'.format(year, year + 1) for year in range(2000, 2017)]
print(seasons)
base_url = 'https://www.fctables.com/france/ligue-1/'

for season in seasons:
	url = base_url + season
	print(url)
	request = requests.get(url)
	data = request.text
	soup = BeautifulSoup(data, 'lxml')
	stage_tables = soup.findAll('table', id=lambda x: x and x.startswith('table_stage'))
	table = stage_tables[0]
	headers = [header.text for header in table.find_all('th')]
	rows = []
	for row in table.find_all('tr'):
		rows.append([val.text.encode('utf8') for val in row.find_all('td')])
	'''
	0 -> Position
	1 -> Team name
	2 -> Games played
	3 -> Points
	4 -> Wins
	5 -> Draws 
	6 -> Losses
	7 -> Goals done
	8 -> Goals against
	'''

	column_names = ['Position','Team','Games','Points','Wins','Draws','Losses','GD','GA']
	values_rows = []

	for current_row in rows:
		if len(current_row) > 8:
			values_row = [current_row[i].decode("utf-8").strip() for i in range(0,9)]
			values_rows.append(values_row)

	out_path = '../data/Tables/' + country + '/' + season.replace("/","") + ".csv"
	print(out_path)
	csv_writer(column_names, values_rows, out_path)