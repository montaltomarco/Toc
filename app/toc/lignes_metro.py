# -*- coding: utf-8 -*-
from xml.dom import minidom
import os
import json
import sys
import psycopg2
sys.path.append('/app/')
os.environ["DJANGO_SETTINGS_MODULE"] = "app.settings"
from toc.models import *
import django
django.setup()

def refresh_lignes_metro():
    #Requête sur http://overpass-turbo.eu/ : network=TCL and station=subway

    #Récupération des numéros des lignes à partir des fichiers XML
    lignes = {}
    for ligneFile in os.listdir('/app/toc/metro_data'):
        ligne = []
        if ligneFile.endswith('.xml'):
            doc = minidom.parse('/app/toc/metro_data/%s' %ligneFile)
            root = doc.documentElement
            for element in root.getElementsByTagName('relation'):
                for member in element.getElementsByTagName('member'):
                    if member.getAttribute('type') == "node":
                        ligne.append(member.getAttribute('ref'))
            nom = ligneFile.split('.')
            lignes[nom[0]] = ligne

    #Création des lignes à partir de la liste "lignes
    with open('/app/toc/metro_data/stations_metro.json') as data_file:
        json_metro = json.loads(data_file.read())
        listeStations = {}
        print "coucou"
        for kJson, vJson in json_metro.iteritems():
            print vJson
refresh_lignes_metro()