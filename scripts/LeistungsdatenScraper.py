from bs4 import BeautifulSoup
from pprint import pprint
import requests
import json


headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}
main_url = "https://www.transfermarkt.com/"
'''
https://www.transfermarkt.com/paris-saint-germain/leistungsdaten/verein/583/plus/0?reldata=FR1%262016
'''
country = 'Spain'
directory = '../data/Leistungsdaten/' + country + '/'
file_name = '../data/Yearly teams/' + country + '.json'


years = [year for year in range(1995,2017)]
players_dict = {}


with open(file_name) as data_file:    
        data = json.load(data_file)

        for year in years:
        	
        	players_dict[year] = {}
        	year_data = data[str(year)]

        	for team_id in year_data.keys():
        		i = 0

        		team_name = year_data[team_id]
        		players_dict[year][team_name] = {}

        		url = main_url + team_name + "/leistungsdaten/verein/" + team_id + "/plus/0?reldata=ES1%26" + str(year)
        		print(url)
        		request = requests.get(url, headers=headers)

        		html_data = request.text
        		soup = BeautifulSoup(html_data, 'lxml')
        		table = soup.find("table", { "class" : "items" })

        		for row in table.findAll("tr"):
        			cells = row.findAll('td')

        			if len(cells) > 0:

	        			try:
	        				#name
	        				name = cells[3].find("a", {"class" : "spielprofil_tooltip"})['title']
	        				#pprint(name)
	        				#age
	        				age = cells[5].getText()
	        				#pprint(age)
	        				#nationality
	        				nationality = cells[6].find("img", {"class" : "flaggenrahmen"})['title']
	        				#pprint(nationality)
	        				#appearances
	        				appearances = cells[8].getText()
	        				if not appearances.isdigit():
	        					appearances = 0
	        				#pprint(appearances)
	        				#minutes
	        				minutes = cells[10].getText()
	        				# if not minutes.isdigit():
	        				# 	minutes = 0
	        				#pprint(minutes)

	        				players_dict[year][team_name][i] = {'name':name, 'age':int(age), 'nationality':nationality, 'appearances':int(appearances), 'minutes':minutes}
	        				i += 1

	        			except:
	        				pass

	        pprint(players_dict)	
	        out_file = directory + str(year) + '.json'

	        with open(out_file, 'w') as outfile:
	        	json.dump(players_dict, outfile, sort_keys=True, indent=4)		

	        #exit()