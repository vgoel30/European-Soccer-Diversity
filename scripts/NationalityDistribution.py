from pprint import pprint
import json
import pandas as pd
from sklearn import preprocessing
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import math

def plot_time_series(df, title):
	fig, ax = plt.subplots()
	#plot graph
	#ax = df.plot(figsize=(12,8),marker='o', ax=ax)
	ax = df.plot(figsize = (12,8), marker='o', ax=ax)
	   
	#set title
	plt.title(title, fontsize=13)

	#set ticks roatation
	#plt.xticks(rotation=50)
	ax.set_ylabel('Percentages')
	   
	ax.set_ylim(top=100)
	ax.set_ylim(bottom=0)
	plt.show()

def minutes_parser(minutes_string):
	if minutes_string == '-':
		return 0
	return int(minutes_string.replace('\'','').replace('.',''))

def get_nationality_distribution_df(target_country):
	countries = ['England', 'France', 'Germany', 'Italy', 'Spain']
	years = [str(year) for year in range(1995, 2017)]

	values = {}

	for country in countries:
		country_info = {}
		data_file = '../data/Leistungsdaten/' + str(country) + '/2016.json'
		with open(data_file) as datafile:
			data = json.load(datafile)

			for year in years:
				count = 0
				#print('Data file : ' + str(data_file) + '   ' + str(year))
				year_data = data[year]

				for key in year_data:
					players = year_data[key]
					for player in players:
						player_info = players[player]
						player_country = player_info['nationality']
						if(player_country == target_country):
							count += 1

				country_info[year] = count
		values[country] = country_info
	
	pprint(values)
	for year in years:
		year_sum = 0
		for country in countries:
			year_sum += values[country][year]
		for country in countries:
			values[country][year] /= year_sum
			values[country][year] *= 100
	
	df = pd.DataFrame({'England': list(values['England'].values()),
						'France': list(values['France'].values()),
						'Germany': list(values['Germany'].values()),
						'Italy' : list(values['Italy'].values()),
						'Spain' : list(values['Spain'].values()),
						'Year': years			})
	df = df.set_index('Year')
	return df

target_country = 'Italy'
df = get_nationality_distribution_df(target_country)
pprint(df)
plot_time_series(df, target_country)