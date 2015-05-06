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
        dbExist = False

        json_objs = json.loads(ur.urlopen('https://download.data.grandlyon.com/wfs/grandlyon?SERVICE=WFS&VERSION=2.0.0&outputformat=GEOJSON&maxfeatures=30&request=GetFeature&typename=pvo_patrimoine_voirie.pvostationautopartage&SRSNAME=urn:ogc:def:crs:EPSG::4326').read())
        for obj in json_objs["features"]:
            if(len(list(Station_autopartage.objects.all().filter(nom = obj["properties"]["nom"]))) == 0):
                new_station = Station_autopartage()
                new_station.adresse = obj["properties"]["adresse"]
                new_station.lat = float(obj["geometry"]["coordinates"][1])
                new_station.lon = float(obj["geometry"]["coordinates"][0])
                new_station.nom = obj["properties"]["nom"]
                new_station.identifiantstation = obj["properties"]["identifiantstation"]
                new_station.commune = obj["properties"]["commune"]
                new_station.typeautopartage = obj["properties"]["typeautopartage"]
                new_station.save()




def set_prox_velov_tcl():
    query_tcl = Arret_TCL.objects.all()
    for arret in query_station:
        arret = Arret_TCL()
        carre = Carre_recherche()
        carre.origine = arret
        carre.rayon = 200
        carre.calculerCarre()

        query_station = Station_velov.objects.filter(lat__range = (carre.begY,carre.endY)
        ).filter(lon__range = (carre.begX,carre.endX))

        for station in query_station:
            arret.station_velov_proches.add(station)

    return False

refresh_database()
