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
    ax.set_ylabel('Percentages')
       
    ax.set_ylim(top=100)
    ax.set_ylim(bottom=0)

    plt.show()

def minutes_parser(minutes_string):
	if minutes_string == '-':
		return 0
	return int(minutes_string.replace('\'','').replace('.',''))

def get_team_percentages_df(country, team):
	data_file = '../data/Leistungsdaten/' + str(country) + '/2016.json'
	years = [str(year) for year in range(1995, 2017)]

	L_local = []
	L_foreign = []

	L_local_minutes = []
	L_foreign_minutes = []

	L_local_apps = []
	L_foreign_apps = []



	years_copy = [str(year) for year in range(1995, 2017)]

	with open(data_file) as datafile:
		data = json.load(datafile)
		for year in years:
			local = 0
			foreign = 0
			local_minutes = 0
			foreign_minutes = 0
			local_apps = 0
			foreign_apps = 0
			L_countries = {}
			#data for a particular year
			try:
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
			except:
				years_copy.remove(year)
				pass
			#pprint(L_countries)

	df = pd.DataFrame({#'Local': L_local,
						'Foreign': L_foreign,
						#'Local minutes': L_local_minutes,
						'Foreign minutes': L_foreign_minutes,
						'Foreign appearances': L_foreign_apps,
						'Year': years_copy			})
	df = df.set_index('Year')
	pprint(df)
	return df

country = 'Spain'
team = 'real-madrid'
df = get_team_percentages_df(country, team)
plot_time_series(df, team)