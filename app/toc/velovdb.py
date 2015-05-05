# -*- coding: utf-8 -*-
import os
import sys
import urllib as ur
import sqlite3
import json
import threading
import datetime
import psycopg2
sys.path.append('/app/')
os.environ["DJANGO_SETTINGS_MODULE"] = "app.settings"
from toc.models import *
import django
django.setup()

def refresh_database():
    #threading.Timer(600.0, refresh_database).start()
    print "Refreshed"
    connexion = psycopg2.connect(dbname = 'db_data', user = 'postgres', password = 'postgres')
    with connexion:
        cur = connexion.cursor()

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

            if len(Station_velov.objects.all().filter(number_station  = int(obj["number"]))) == 0:
                new_station = Station_velov()
                new_station.adresse = a
                new_station.lat = float(obj['position']['lat'])
                new_station.lon = float(obj['position']['lng'])
                new_station.nb_velos = int(obj["available_bike_stands"])
                new_station.nb_places = int(obj["available_bikes"])
                new_station.number_station = int(obj["number"])
                new_station.save()
            else:
                station = Station_velov.objects.get(number_station  = int(obj["number"]))
                station.nb_velos = int(obj["available_bike_stands"])
                station.nb_places = int(obj["available_bikes"])
                station.save()

refresh_database()