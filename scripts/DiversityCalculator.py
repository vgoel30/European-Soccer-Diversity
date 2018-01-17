from pprint import pprint
import json

country = 'Spain'
team = 'real-madrid'

data_file = '../data/Leistungsdaten/' + str(country) + '/2016.json'
years = [year for year in range(2000, 2017)]

with open(data_file) as datafile:
	data = json.load(datafile)
	pprint(data['2016']['real-madrid'])