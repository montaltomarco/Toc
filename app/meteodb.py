# -*- coding: utf-8 -*-
import urllib as ur
import sqlite3
import json
import threading
import datetime
import psycopg2
import re

def refresh_database():
  	#threading.Timer(600.0, refresh_database).start()
  	print "Refreshed"
	connexion = psycopg2.connect(dbname = 'db_data', user = 'postgres', password = 'postgres')
	with connexion:
		cur = connexion.cursor()

		#cur.execute("DELETE FROM toc_data_velo")
		i = 0
		json_objs = json.loads(ur.urlopen('http://www.infoclimat.fr/public-api/gfs/json?_ll=45.74846,4.84671&_auth=ARsDFAR6UHJRfFBnBXMCK1I6UmcKfAAnUS0BYlszAH0FYV8%2FBm0GYAduA34BLldnU34AaAswVWsAZFUzCnhVKQFgA24EblA0UTdQNgUxAilSflIvCjQAJ1EtAW9bNgB9BWdfPwZ7BmYHaANlAS9XalNiAH8LK1VsAGdVMQpnVTIBYgNiBGZQOlE%2FUC0FKgIzUmRSNgo3ADxRMgFlW2IAMgVgXz4GYAZnB2gDfwE5V2RTYwBiCzBVagBmVTsKeFUpARsDFAR6UHJRfFBnBXMCK1I0UmwKYQ%3D%3D&_c=52d2db86d6583cfb968e7bb3f3ac7e12').read())
		for k,v in json_objs.iteritems():
			i = i+1
            print re.split('-| |:', k)
			#cur.execute('INSERT INTO toc_data_meteo(number,contract_name,name,banking,bonus,status,bike_stands,available_bike_stands,available_bikes,last_update,lat,lon,adresse) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)', (int(obj["number"]), (obj["contract_name"]), (obj["name"]), obj["banking"], obj["bonus"], obj["status"], obj["bike_stands"], obj["available_bike_stands"], obj["available_bikes"], int(obj["last_update"]/1000),float(obj['position']['lat']),float(obj['position']['lng']),a))
		connexion.commit()
refresh_database()