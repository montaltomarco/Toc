# -*- coding: utf-8 -*-
import urllib as ur
import sys,os
import sqlite3
import json
import threading
import datetime
import psycopg2
sys.path.append('/app/toc/')
os.environ["DJANGO_SETTINGS_MODULE"] = "app.settings"
from toc.models import Arret_TCL
import django
django.setup()


def refresh_database():
    #threading.Timer(3600.0, refresh_meteodb).start()
    print("Refresh Metro")
    connexion = psycopg2.connect(dbname = 'db_data', user = 'postgres', password = 'postgres')

    with connexion:
        cur = connexion.cursor()

        #Récupération des Ids des lieux à supprimer
        cur.execute("SELECT * FROM toc_arret_tcl")
        list = []

        for row in cur:
            list.append(int(row[0]))

        cur.execute("DELETE FROM toc_arret_tcl")

        #Suppression des lieux associés aux stations de métros qu'on doit supprimer
        for e in list:
            cur.execute("DELETE FROM toc_lieu WHERE id = %s" %e)

        json_metro = json.loads(ur.urlopen('https://download.data.grandlyon.com/wfs/rdata?SERVICE=WFS&VERSION=2.0.0&outputformat=GEOJSON&maxfeatures=30&request=GetFeature&typename=tcl_sytral.tclstation&SRSNAME=urn:ogc:def:crs:EPSG::4326').read())
        for kAllStations,vAllStations in json_metro.iteritems():
            if kAllStations == "features":
                for station in vAllStations:

                    properties = station["properties"];
                    geometry = station["geometry"]

                    nom = properties["nom"]
                    idStation = int(properties["id_station"])
                    latitude = float(geometry["coordinates"][1])
                    longitude = float(geometry["coordinates"][0])
                    arret = Arret_TCL()
                    arret.nom = nom
                    arret.id_station = idStation
                    arret.adresse = nom
                    arret.lat = latitude
                    arret.lon = longitude
                    arret.pmr = True
                    arret.escalator = True
                    arret.save()
refresh_database()