# -*- coding: utf-8 -*-
import urllib as ur
import sqlite3
import json
import threading
import datetime
import psycopg2
import re
from datetime import datetime
import time
import math
import sys
import os
sys.path.append('/app/')
os.environ["DJANGO_SETTINGS_MODULE"] = "app.settings"
from toc.models import *
import django
django.setup()

def minTimestampKey(dictMeteo):
    minimum = -1;
    for keyMeteo, valueMeteo in dictMeteo.iteritems():
        if minimum > keyMeteo or minimum  == -1:
            minimum = keyMeteo
    return minimum

def getCurrentMeteo():
    currentTimeStamp = int(time.time())
    timestampDB = currentTimeStamp - (currentTimeStamp%600)
    return Data_meteo.objects.get(timestamps=timestampDB)

def refresh_meteodb():
    nbValeurSMeteoParHeure = 6

    #threading.Timer(3600.0, refresh_meteodb).start()
    print("Refresh Météo (Each 3600 seconds)")
    connexion = psycopg2.connect(dbname = 'db_data', user = 'postgres', password = 'postgres')

    with connexion:
        cur = connexion.cursor()
        cur.execute("DELETE FROM toc_data_meteo")
        json_meteos = json.loads(ur.urlopen('http://www.infoclimat.fr/public-api/gfs/json?_ll=45.74846,4.84671&_auth=ARsDFAR6UHJRfFBnBXMCK1I6UmcKfAAnUS0BYlszAH0FYV8%2FBm0GYAduA34BLldnU34AaAswVWsAZFUzCnhVKQFgA24EblA0UTdQNgUxAilSflIvCjQAJ1EtAW9bNgB9BWdfPwZ7BmYHaANlAS9XalNiAH8LK1VsAGdVMQpnVTIBYgNiBGZQOlE%2FUC0FKgIzUmRSNgo3ADxRMgFlW2IAMgVgXz4GYAZnB2gDfwE5V2RTYwBiCzBVagBmVTsKeFUpARsDFAR6UHJRfFBnBXMCK1I0UmwKYQ%3D%3D&_c=52d2db86d6583cfb968e7bb3f3ac7e12').read())
        dictMeteo = {}
        for kMeteo, vMeteo in  json_meteos.iteritems():
            dateSplit = re.split('-| |:', kMeteo)
            if len(dateSplit) == 6: #On veut être sûr que ce qu'on récupère est bien une date
                dt = datetime(year=int(dateSplit[0]), month=int(dateSplit[1]), day=int(dateSplit[2]), hour=int(dateSplit[3]), minute=int(dateSplit[4]), second=int(dateSplit[5]))
                timestamp = time.mktime(dt.timetuple())
                temperature = float(vMeteo["temperature"]["2m"])
                dictMeteo[int(timestamp)] = [abs(float(vMeteo["pluie"])), abs(float(vMeteo["pluie_convective"])), temperature]

        i = 0
        dictMeteoOriginal = dictMeteo.copy()

        while(i<len(dictMeteoOriginal)):
            #On va rajouter des valeurs pour avoir des valeur toutes les heures au lieu de 3 heures
            if i < (len(dictMeteoOriginal)-1):
                minimum = minTimestampKey(dictMeteo)
                currentMeteo = dictMeteo.get(minimum)
                nextMeteo = dictMeteo.get(minimum+(3*3600))
                deltaPluie = nextMeteo[0]  - currentMeteo[0]
                deltaPluieConvective = nextMeteo[1]  - currentMeteo[1]
                deltaTemperature = nextMeteo[2]  - currentMeteo[2]

                j = 0
                while(j < nbValeurSMeteoParHeure):
                    meteo = Data_meteo()
                    meteo.timestamps = int(minimum + (j*(3600/nbValeurSMeteoParHeure)))
                    meteo.pluie = float(currentMeteo[0]) + ((float(j)/float(nbValeurSMeteoParHeure))* float(deltaPluie))
                    meteo.pluie_convective =  float(currentMeteo[1]) + ((float(j)/float(nbValeurSMeteoParHeure))* float(deltaPluieConvective))
                    meteo.temperature =  float(currentMeteo[2]) + ((float(j)/float(nbValeurSMeteoParHeure))* float(deltaTemperature)) -273.15
                    meteo.save()
                    j = j + 1

                dictMeteo.pop(minimum)
            else: #on incère le timestamp manimum en base de donnée
                meteo = Data_meteo()
                meteo.timestamps = int(dictMeteo.keys()[0])
                meteo.pluie = float(dictMeteo.values()[0][0])
                meteo.pluie_convective = float(dictMeteo.values()[0][1])
                meteo.temperature = float(dictMeteo.values()[0][2])-273.15
                meteo.save()
            i += 1
refresh_meteodb()