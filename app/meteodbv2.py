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

def minTimestampKey(dictMeteo):
    minimum = -1;
    for keyMeteo, valueMeteo in dictMeteo.iteritems():
        if minimum > keyMeteo or minimum  == -1:
            minimum = keyMeteo
    return minimum

def refresh_meteodb():
    #threading.Timer(3600.0, refresh_meteodb).start()
    print("Refresh Météo (Each 3600 seconds) : ")
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
                dictMeteo[int(timestamp)] = [abs(float(vMeteo["pluie"])), abs(float(vMeteo["pluie_convective"]))]
        i = 0
        dictMeteoOriginal = dictMeteo.copy()
        print("Size Original = ", len(dictMeteoOriginal))
        print("Size Normal = ", len(dictMeteoOriginal))
        while(i<len(dictMeteoOriginal)):
            #On va rajouter des valeurs pour avoir des valeur toutes les heures au lieu de 3 heures
            if i < (len(dictMeteoOriginal)-1):
                minimum = minTimestampKey(dictMeteo)
                currentMeteo = dictMeteo.get(minimum)
                nextMeteo = dictMeteo.get(minimum+(3*3600))
                deltaPluie = nextMeteo[0]  - currentMeteo[0]
                deltaPluieConvective = nextMeteo[1]  - currentMeteo[1]
                #print ("Delta Pluie = ", deltaPluie)
                #print ("Delta Pluie Convective = ", deltaPluieConvective)
                #print((1/3)*0.1)
                firstNewMeteo = [currentMeteo[0] + ((1/3)* deltaPluie), currentMeteo[1] + ((1/3)* deltaPluieConvective)]
                secondNewMeteo = [currentMeteo[0] + ((2/3)* deltaPluie), currentMeteo[1] + ((2/3)* deltaPluieConvective)]
                cur.execute("INSERT INTO toc_data_meteo(timestamps, pluie, pluie_convective) VALUES(%s,%s,%s)", (int(minimum),float(currentMeteo[0]),float(currentMeteo[1])))
                cur.execute("INSERT INTO toc_data_meteo(timestamps, pluie, pluie_convective) VALUES(%s,%s,%s)", (int(minimum+3600),float(firstNewMeteo[0]),float(firstNewMeteo[1])))
                cur.execute("INSERT INTO toc_data_meteo(timestamps, pluie, pluie_convective) VALUES(%s,%s,%s)", (int(minimum+(2*3600)),float(secondNewMeteo[0]),float(secondNewMeteo[1])))
                print("Size  = ", len(dictMeteo))
                dictMeteo.pop(minimum)
                print("New Size  = ", len(dictMeteo))
            else: #on incère le timestamp manimum en base de donnée
                cur.execute("INSERT INTO toc_data_meteo(timestamps, pluie, pluie_convective) VALUES(%s,%s,%s)", (int(dictMeteo.keys()[0]),float(dictMeteo.values()[0][1]),float(dictMeteo.values()[0][1])))
            i = i + 1
refresh_meteodb()