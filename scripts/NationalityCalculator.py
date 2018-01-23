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
    ax.set_ylim(top=50)
    ax.set_ylim(bottom=0)

    plt.show()

def minutes_parser(minutes_string):
	if minutes_string == '-':
		return 0
	return int(minutes_string.replace('\'','').replace('.',''))

def get_nationalities_df():
	years = [str(year) for year in range(1995, 2017)]
	countries = ['England', 'France', 'Germany', 'Italy', 'Spain']

	final_data = []

	for country in countries:
		final_data.append([])
		for year in years:
			final_data[-1].append(0)

	for year in years:
		total = 0

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
						if player_country in countries:
							final_data[countries.index(player_country)][int(year) - 1995] += 1
						total += 1

		for country in countries:
			final_data[countries.index(country)][int(year) - 1995] /= total
			final_data[countries.index(country)][int(year) - 1995] *= 100

	L_all_data = final_data

	df = pd.DataFrame({'England': L_all_data[0],
						'France': L_all_data[1],
						'Germany': L_all_data[2],
						'Italy' : L_all_data[3],
						'Spain' : L_all_data[4],
						'Year': years			})
	df = df.set_index('Year')
	return df

df = get_nationalities_df()
pprint(df)
plot_time_series(df, 'Percentage of nationalies')