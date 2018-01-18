from pprint import pprint
import json
import pandas as pd
from sklearn import preprocessing
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import math
from gini import gini

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
    ax.set_ylabel('Diversity Scores')
       
    ax.set_ylim(top=3)
    ax.set_ylim(bottom=0)

    plt.show()

def minutes_parser(minutes_string):
	if minutes_string == '-':
		return 0
	return int(minutes_string.replace('\'','').replace('.',''))

country = 'Spain'
team = 'athletic-bilbao'

data_file = '../data/Leistungsdaten/' + str(country) + '/2016.json'
years = [str(year) for year in range(2000, 2017)]

L_local = []
L_foreign = []

L_local_minutes = []
L_foreign_minutes = []

L_local_apps = []
L_foreign_apps = []

L_diversity_values = []

years_copy = [str(year) for year in range(2000, 2017)]

with open(data_file) as datafile:
	data = json.load(datafile)
	for year in years:
		L_countries = {}
		local = 0
		foreign = 0
		local_minutes = 0
		foreign_minutes = 0
		local_apps = 0
		foreign_apps = 0
		#data for a particular year
		try:
			year_data = data[year][team]

			#go through each player
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

			gini_value = gini(np.asarray(list(L_countries.values()), dtype=np.float))
			diversity = 1/gini_value
			pprint(diversity)
			L_diversity_values.append(diversity)

		except:
			years_copy.remove(year)
			pass


df = pd.DataFrame({'Diversity score': L_diversity_values,
					'Year': years_copy			})
df = df.set_index('Year')
#pprint(df)
plot_time_series(df, team)