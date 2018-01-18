from pprint import pprint
import json
import pandas as pd
from sklearn import preprocessing
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import math

def plot_time_series(df, title):
    #plot graph
    ax = df.plot(figsize=(12,8),marker='o')
       
    #set title
    plt.title(title, fontsize=13)
    
    #set ticks roatation
    plt.xticks(rotation=50)
    
    #keep colors for next graph
    colors = [x.get_color() for x in ax.get_lines()]
    #colors_mapping = dict(zip(seasons,colors))
    
    #remove x label
    ax.set_ylabel('Percentages')
       
    ax.set_ylim(top=100)
    ax.set_ylim(bottom=0)

    plt.show()

def minutes_parser(minutes_string):
	if minutes_string == '-':
		return 0
	return int(minutes_string.replace('\'','').replace('.',''))

country = 'France'

data_file = '../data/Leistungsdaten/' + str(country) + '/2016.json'
years = [str(year) for year in range(2000, 2017)]


L_countries = {}

countries = ['England', 'France', 'Germany', 'Italy', 'Spain']

L_all_data = []


for country in countries:
	data_file = data_file = '../data/Leistungsdaten/' + str(country) + '/2016.json'

	L_local = []
	L_foreign = []

	L_local_minutes = []
	L_foreign_minutes = []

	L_local_apps = []
	L_foreign_apps = []

	with open(data_file) as datafile:
		data = json.load(datafile)
		for year in years:
			local = 0
			foreign = 0
			local_minutes = 0
			foreign_minutes = 0
			local_apps = 0
			foreign_apps = 0

			#data for a particular year
			league_year_data = data[year]
			#go trhough each team in the year
			for team in league_year_data:
				year_data = data[year][team]

				for key in year_data:
					player = year_data[key]
					player_country = player['nationality']
					if(player_country == country):
						local += 1
						local_minutes += minutes_parser(player['minutes'])
						local_apps += player['appearances']
					else:
						foreign += 1
						foreign_minutes += minutes_parser(player['minutes'])
						foreign_apps += player['appearances']
					if player_country not in L_countries.keys():
						L_countries[player_country] = 0
					L_countries[player_country] = L_countries[player_country] + 1

			total = local + foreign
			L_local.append((local/total)*100)
			L_foreign.append((foreign/total)*100)

			total = local_apps + foreign_apps
			L_local_apps.append((local_apps/total) * 100)
			L_foreign_apps.append((foreign_apps/total) * 100)

			total = local_minutes + foreign_minutes
			L_local_minutes.append((local_minutes/total)*100)
			L_foreign_minutes.append((foreign_minutes/total)*100)

		L_all_data.append(L_foreign_minutes)

pprint(len(L_all_data))
# L_all_data = np.asarray(L_all_data).T.tolist()

#pprint(L_countries)
df = pd.DataFrame({'England': L_all_data[0],
					'France': L_all_data[1],
					'Germany': L_all_data[2],
					'Italy' : L_all_data[3],
					'Spain' : L_all_data[4],
					'Year': years			})
df = df.set_index('Year')
pprint(df)
plot_time_series(df, 'League comparisons of percentage of playing time given to foreigners')