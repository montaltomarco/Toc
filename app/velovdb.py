# -*- coding: utf-8 -*-
import urllib as ur
import sqlite3
import json
import threading
import datetime
import psycopg2

def refresh_database():
  	#threading.Timer(600.0, refresh_database).start()
  	print "Refreshed"
	connexion = psycopg2.connect(dbname = 'db_data', user = 'postgres', password = 'postgres')
	with connexion:
		cur = connexion.cursor()

		#cur.execute("DELETE FROM toc_lieu")
		cur.execute("DELETE FROM toc_data_velo")
		i = 0
		#cur.execute("CREATE TABLE toc_data_velo(id INTEGER PRIMARY KEY,number INT,contract_name TEXT,name TEXT,banking bonus|status|bike_stands|available_bike_stands|available_bikes|last_update|adresse|lat|lon
		json_objs = json.loads(ur.urlopen('https://api.jcdecaux.com/vls/v1/stations?contract=Lyon&apiKey=fce6b56320ad1cd5e2fb0dcc38e793bded329a53').read())
		for obj in json_objs:
			a = str((obj["address"]).encode('utf-8', errors='replace'))
			if len(a) <1:
				i = i+1
				a = (obj["name"])
				if len(a) <1:
					a = str(i)
			cur.execute("INSERT INTO toc_lieu(lat,lon,adresse) VALUES(%s,%s,%s)", (float(obj['position']['lat']),float(obj['position']['lng']),a))
			cur.execute('INSERT INTO toc_data_velo(number,contract_name,name,banking,bonus,status,bike_stands,available_bike_stands,available_bikes,last_update,lat,lon,adresse) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)', (int(obj["number"]), (obj["contract_name"]), (obj["name"]), obj["banking"], obj["bonus"], obj["status"], obj["bike_stands"], obj["available_bike_stands"], obj["available_bikes"], int(obj["last_update"]/1000),float(obj['position']['lat']),float(obj['position']['lng']),a))
		connexion.commit()
refresh_database()