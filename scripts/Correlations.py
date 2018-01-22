import json
import csv
from pprint import pprint
import pandas as pd
import seaborn as sns
import math
import numpy as np; np.random.seed(0)
from gini import gini

def csv_writer(params, values_lists, path):
    with open(path, "w") as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
              
        writer.writerow(params)
        
        for line in values_lists:
            writer.writerow(line)

def minutes_parser(minutes_string):
	if minutes_string == '-':
		return 0
	return int(minutes_string.replace('\'','').replace('.',''))

L_countries = {}
nations_path = '../data/Nations.txt'
with open(nations_path) as nations_file:
	for nation in nations_file:
		L_countries[nation.replace('\n','')] = 0

def get_team_percentage(data, year, team):
	age = 0
	local = 0
	foreign = 0
	local_minutes = 0
	foreign_minutes = 0
	local_apps = 0
	foreign_apps = 0

	for nation in L_countries:
			L_countries[nation] = 0 

	
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
		age += (player['age'] * player['appearances'])
		#increase the country count
		if player_country != 'N/A':
			L_countries[player_country] = L_countries[player_country] + player['appearances']
	

	gini_value = gini(np.asarray(list(L_countries.values()), dtype=np.float))
	diversity = 1/gini_value
	average_age = age/(local + foreign)
	total = local_minutes + foreign_minutes
	return [(foreign_minutes/total)*100, average_age, diversity]

def csv_dict_reader(file_obj):
    """
    Read a CSV file using csv.DictReader
    """
    reader = csv.DictReader(file_obj, delimiter=',')
    for line in reader:
        print(line["Name"])
        #print(line["Matches"])

def csv_reader(file_obj):
    """
    Read a csv file
    """
    reader = csv.reader(file_obj)
    for row in reader:
        print(" ".join(row))

years = [year for year in range(1995, 2017)]

rows = []
params = ['Won', 'Lost', 'Draw', 'GF', 'GA',  'PPM', 'Foreign playing time %', 'Average age', 'diversity']

country = 'Germany'
data_file = '../data/Leistungsdaten/' + str(country) + '/2016.json'

for year in years:
	path = '../data/Standings/' + country + '/' + str(year) + '.csv'

	with open(path, "r") as file_obj:
		reader = csv.DictReader(file_obj, delimiter=',')

		with open(data_file) as datafile:
			data = json.load(datafile)
			for line in reader:

				#new row data for each team
				row = []
				team_name = line['Name']
				# pprint(team_name + ':  ' + str(get_team_percentage(data, '2001', team_name)))
				# pprint(line)
				row.append(int(line['Won']))
				row.append(int(line['Lost']))
				row.append(int(line['Draw']))
				row.append(int(line['GF']))
				row.append(int(line['GA']))
				#row.append(int(line['Points']))
				row.append(float(line['PPM']))

				vals = get_team_percentage(data, str(year), team_name)

				row.append(vals[0])
				row.append(vals[1])
				row.append(vals[2])

				rows.append(row)

csv_writer(params, rows, 'lol.csv')

df = pd.read_csv('lol.csv')    
corr = df.corr()
sns.set(font_scale=0.8)
sns.heatmap(corr, cmap="YlGnBu", annot=True, annot_kws={"size": 13})
sns.plt.yticks(rotation=0)
sns.plt.xticks(rotation=90) 
sns.plt.show()