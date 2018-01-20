import json
import csv
from pprint import pprint

def minutes_parser(minutes_string):
	if minutes_string == '-':
		return 0
	return int(minutes_string.replace('\'','').replace('.',''))

def get_team_percentage(data, year, team):

	local = 0
	foreign = 0
	local_minutes = 0
	foreign_minutes = 0
	local_apps = 0
	foreign_apps = 0

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

	# total = local + foreign
	# L_local.append((local/total)*100)
	# L_foreign.append((foreign/total)*100)

	# total = local_apps + foreign_apps
	# L_local_apps.append((local_apps/total) * 100)
	# L_foreign_apps.append((foreign_apps/total) * 100)

	total = local_minutes + foreign_minutes
	return (foreign_minutes/total)*100

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

country = 'England'

path = '../data/Standings/England/2001.csv'
data_file = '../data/Leistungsdaten/' + str(country) + '/2016.json'

with open(path, "r") as file_obj:
	reader = csv.DictReader(file_obj, delimiter=',')

	with open(data_file) as datafile:
		data = json.load(datafile)
		for line in reader:
			team_name = line['Name']
			pprint(team_name + ':  ' + str(get_team_percentage(data, '2001', team_name)))