from bs4 import BeautifulSoup
from pprint import pprint
import requests
import json

country = 'Spain'
data_path = '../data/URLs/' + country
main_url = "https://www.transfermarkt.com"
out_file = '../data/Yearly teams/' + country + '.json'

years = [year for year in range(1995,2017)]

teams_dict = {}

for year in years:
	file_name = data_path + "/" + str(year) + ".txt"
	teams_dict[year] = {}

	with open(file_name, 'r') as data_file:
		for line in data_file:
			line = line.replace('\n','')
			url = main_url + line
			tokens = line.split('/')
			#print(tokens[1] + " " + tokens[-3])
			teams_dict[year][tokens[-3]] = tokens[1]
	#print()
	#exit()
pprint(teams_dict)

with open(out_file, 'w') as outfile:
    json.dump(teams_dict, outfile, sort_keys=True, indent=4)