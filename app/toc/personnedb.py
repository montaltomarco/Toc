__author__ = 'Amine'
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
        new_personne = Personne()
        new_personne.nom = 'Montalto'
        new_personne.prenom = 'Marco'
        new_personne.email = 'parco.dontalto@insa-lyon.fr'
        new_personne.mot_de_pass = 'marcopd'
        new_personne.save()
refresh_database()