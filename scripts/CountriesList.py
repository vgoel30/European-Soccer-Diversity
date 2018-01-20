import json
from pprint import pprint

years = [str(year) for year in range(2000, 2017)]
countries = ['England', 'France', 'Germany', 'Italy', 'Spain']

all_countries = []

out_path = '../data/Nations.txt'

with open(out_path, 'w') as textfile:
	for year in years:

		for country in countries:
			data_file = '../data/Leistungsdaten/' + str(country) + '/2016.json'

			with open(data_file) as datafile:
				data = json.load(datafile)

				#data for a particular year
				league_year_data = data[year]
				#go trhough each team in the year
				for team in league_year_data:
					year_data = data[year][team]
					#each player
					for key in year_data:
						player = year_data[key]
						player_country = player['nationality']
						if player_country not in all_countries and player_country != 'N/A':
							all_countries.append(player_country)
							textfile.write(player_country + '\n')

pprint(all_countries)