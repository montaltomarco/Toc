from django.db import models
from math import *
from collections import *
import requests
import json
import time
# Create your models here.

def calculerDistance(depart,arrivee):
    deltaT = coordY_to_metres(abs(arrivee.lat - depart.lat))
    deltaL = coordX_to_metres(abs(arrivee.lon - depart.lon))
    distance = sqrt(deltaT**2+deltaL**2)
    return distance

#coordX etant une coordonnee GPS sens W/E en degres decimaux
def coordX_to_metres(deltaX):
    return deltaX*75750

#coordX etant une coordonnee GPS sens N/S en degres decimaux
def coordY_to_metres(deltaY):
    return deltaY*111120

def metres_to_coordX(distance):
    return distance/75750

def metres_to_coordY(distance):
    return distance/111120

#Definit un reseau de stations et de lignes
# comme le reseau d'arret TCL ou le reseau de velov
def getStationVelov(zoneRecherche,station_depart):
    querySet = Station_velov.objects.filter(lat__range = (zoneRecherche.begY,zoneRecherche.endY)
    ).filter(lon__range = (zoneRecherche.begX,zoneRecherche.endX))
    if station_depart:
        querySet.filter(nb_velos__gt = 2)
    else:
        querySet.filter(nb_places__gt = 2)
    return querySet

def getStationBluely(zoneRecherche,station_depart):
    querySet = Station_autopartage.objects.filter(lat__range = (zoneRecherche.begY,zoneRecherche.endY)
    ).filter(lon__range = (zoneRecherche.begX,zoneRecherche.endX))
    return querySet

def getBorneVelo(zoneRecherche,station_depart):
    querySet = Borne_velo.objects.filter(lat__range = (zoneRecherche.begY,zoneRecherche.endY)
    ).filter(lon__range = (zoneRecherche.begX,zoneRecherche.endX))
    if station_depart:
        querySet.filter(nb_velos__gt = 2)
    else:
        querySet.filter(nb_places__gt = 2)
    return querySet

class Lieu(models.Model):
    lat = models.FloatField('Latitude')
    lon = models.FloatField('Longitude')
    adresse = models.CharField(max_length=200)
    def __str__(self):
        return self.adresse.encode('utf-8', errors='replace')

class Parcours_temporel():
    #approx_dep = Lieu()# = models.ForeignKey(Lieu,related_name="approx_dep")
    #approx_arr = Lieu()# = models.ForeignKey(Lieu,related_name="approx_arr")
    #exact_dep = Lieu()# = models.ForeignKey(Lieu,related_name="exact_dep")
    #exact_arr = Lieu()# = models.ForeignKey(Lieu,related_name="exact_arr")

    exact_calc = False
    approx_calc = False

    #current_time = models.IntegerField()

    def get_temps_exact(self,user):
        return 0

    def get_temps_approx(self,user):
        return 0

    def calcul(self,user):
        return 0

def Parcours_compare(v1, v2):
    if v1.current_time<v2.current_time:
        return -1
    elif v1.current_time>v2.current_time:
        return 1
    else:
        return 0

class Parcours_inter_station(Parcours_temporel):
    def get_temps_approx(self,user):
        user_speed = user.vitesse_velo
        dist = calculerDistance(self.approx_dep,self.approx_arr)
        temps_approx = dist/user_speed+user.temps_start+user.temps_stop
        self.temps = temps_approx
        return temps_approx

    def get_temps_exact(self,user):
        self.approx_dep = self.exact_dep
        self.approx_arr = self.exact_arr
        #TODO: integeration user
        return self.get_temps_approx(user)

class Parcours_pied(Parcours_temporel):
    def get_temps_approx(self,user):
        user_speed = user.vitesse_pied
        dist = calculerDistance(self.approx_dep,self.approx_arr)
        temps_approx = dist/user_speed
        self.temps = temps_approx
        return temps_approx

    def get_temps_exact(self,user):
        #self.approx_dep = self.exact_dep
        #self.approx_arr = self.exact_arr
        #TODO: integeration user
        user_speed = 1
        if self.exact_calc:
            return self.current_time
        else:
            return self.get_temps_approx(user)


class Section(models.Model):
    moyen_transport = models.CharField(max_length=30)
    en_cours = models.BooleanField('en_cours')
    temps = models.IntegerField()
    taux_pollution = models.FloatField('Pollution')
    trajet = models.ForeignKey("Trajet")

class Personne(models.Model):
    nom = models.CharField(max_length=200)
    prenom = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    mot_de_pass = models.CharField(max_length=200)
    vitesse_pied = models.FloatField(default=1.0)
    vitesse_velo = models.FloatField(default=5.0)
    temps_start = models.IntegerField(default=100)
    temps_stop = models.IntegerField(default=100)

    def __str__(self):
        return self.nom + ' ' + self.prenom

class Itineraire(models.Model):
    start_pos = models.ForeignKey(Lieu,related_name="start_pos")
    end_pos = models.ForeignKey(Lieu,related_name="end_pos")
    duree = models.FloatField()
    sections = models.ManyToManyField(Section)
    personnes = models.ManyToManyField(Personne)

    def __str__(self):
        return self.start_pos.name

class Profil(models.Model):
    type_personne = models.CharField(max_length=200)

class Data_velo(models.Model):
    number = models.IntegerField()
    contract_name = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    lat = models.FloatField()
    lon = models.FloatField()
    adresse = models.CharField(max_length=200)
    banking = models.BooleanField('banking')
    bonus = models.BooleanField('bonus')
    status = models.CharField(max_length=200)
    bike_stands = models.IntegerField()
    available_bike_stands = models.IntegerField()
    available_bikes = models.IntegerField()
    last_update = models.IntegerField()
    def __str__(self):
        return self.name.encode('utf-8', errors='replace')

class Data_meteo(models.Model):
    timestamps = models.IntegerField()
    pluie = models.FloatField()
    pluie_convective = models.FloatField()
    def __str__(self):
        return 'Timestamps = ' + str(self.timestamps) + ' Pluie = ' + str(self.pluie) + ' Pluie Convective= ' + str(self.pluie_convective)

class Station_velov(Lieu):
    number_station = models.IntegerField()
    nb_velos = models.IntegerField()
    nb_places = models.IntegerField()

    def __str__(self):
        return self.adresse.encode('utf-8', errors='replace')+" "+str(self.number_station)

class Borne_velo(Lieu):
    nbarceaux = models.IntegerField()

class Station_autopartage(Lieu):
    nom = models.CharField(max_length=200)
    identifiantstation = models.CharField(max_length=200)
    commune = models.CharField(max_length=200)
    typeautopartage = models.CharField(max_length=200)

    def __str__(self):
        return self.identifiantstation.encode('utf-8', errors='replace')+" : "+self.nom.encode('utf-8', errors='replace')+" "+str(self.lon)+" "+str(self.lat)



class Ligne_TCL(models.Model):
    #reseau = models.ForeignKey(Reseau)
    codeTitan = models.CharField(max_length = 20)
    ligne = models.CharField(max_length = 20)
    sens = models.CharField(max_length = 20)
    indice = models.CharField(max_length = 100)
    infos = models.CharField(max_length = 100)
    libelle = models.CharField(max_length=20)
    arrets = models.ManyToManyField('Arret_TCL')
    stations_velov = models.ManyToManyField(Station_velov)

    def __str__(self):
        return self.codeTitan+" "+self.libelle

class Arret_TCL(Lieu):
    #reseau = models.ForeignKey(Reseau)
    #id = models.IntegerField()
    id_station = models.IntegerField()
    nom = models.CharField(max_length = 100)
    #lignes = models.ManyToManyField(Ligne_TCL)
    pmr = models.BooleanField()
    escalator = models.BooleanField()
    stations_velov_proches = models.ManyToManyField(Station_velov)

    def __str__(self):
        return self.nom+" "+super(Arret_TCL,self).__str__()

#Definit un carre autour d'un point d'origine afin de fournir des coordonnees
#de polygone en vue d'une recherche (stations Velov environnantes par exemple)
class Carre_recherche():
    origine = Lieu()# = models.ForeignKey(Lieu)
    #rayon en metres
    rayon = 0.0# = models.IntegerField()
    #offset POSITIF exprimant un decalage vers l'EST en metres
    offsetX = 0.0 #models.IntegerField()
    #offset POSITIF exprimant le decalage vers le NORD en metres
    offsetY = 0.0 #models.IntegerField()

    #begX : extreme OUEST en coord
    begX = 0.0 # models.FloatField()
    #begY : extreme SUD en coord
    begY = 0.0 # models.FloatField()

    #endX : extreme EST en coord
    endX = 0.0 # models.FloatField()
    #endY : extreme NORD en coord
    endY = 0.0 # models.FloatField()

    def calculerCarre(self):
        oX = self.origine.lon
        oY = self.origine.lat
        #delta POSITIF entre l'origine et
        #le bord Nord, Sud, Est ou Ouest du carre
        o_to_N = metres_to_coordY(self.rayon + self.offsetY)
        o_to_S = metres_to_coordY(self.rayon - self.offsetY)
        o_to_E = metres_to_coordX(self.rayon + self.offsetX)
        o_to_W = metres_to_coordX(self.rayon - self.offsetX)
        self.begX = oX - o_to_W
        self.begY = oY - o_to_S
        self.endX = oX + o_to_E
        self.endY = oY + o_to_N


class Vecteur(models.Model):
    depart = models.ManyToManyField(Lieu,related_name="depart")
    arrivee = models.ManyToManyField(Lieu,related_name="arrivee")
    distance = models.FloatField()

    def __str__(self):
        return self.depart+" "+self.arrivee

    def calculer_distance(self):
        deltaT = coordY_to_metres(abs(self.depart.lat - self.depart.lat))
        deltaL = coordX_to_metres(abs(self.arrivee.lon - self.depart.lon))
        self.distance = sqrt(deltaT**2+deltaL**2)
        return self.distance

#@param[itineraire] est de type trajet
def selectionner_stations_velov(itineraire,user):
    stations_dep = getStationsZone(itineraire,user,True,"velov")
    stations_arr = getStationsZone(itineraire,user,False,"velov")
    if len(stations_dep)==0 or len(stations_arr)==0 :
        raise Exception("Pas de station dans la zone")
    temps_stat_dep = {}
    for station in stations_dep:
        #Creation trajets pied entre dep et stat dep
        new_trajet = Parcours_pied()
        new_trajet.approx_dep = itineraire.start_pos
        new_trajet.approx_arr = station
        temps_pied = new_trajet.get_temps_approx(user)


        #Creation trajets velo entre stat dep et arr
        new_trajet2 = Parcours_inter_station()
        new_trajet2.approx_dep = station
        new_trajet2.approx_arr = itineraire.end_pos
        new_trajet2.get_temps_approx(user)

        temps_velo = new_trajet2.get_temps_approx(user)

        temps_stat_dep[temps_pied+temps_velo] = (station,new_trajet,new_trajet2)

    ordered_temps_stat_dep = sorted(temps_stat_dep.iterkeys())

    #On recupere la meilleure station
    best_start_station = temps_stat_dep[ordered_temps_stat_dep[0]][0]
    trajet_pied_best_start_stat = temps_stat_dep[ordered_temps_stat_dep[0]][1]

    temps_stat_arr = {}
    for station in stations_arr:
        #Creation trajets pied entre dep et stat dep
        new_trajet = Parcours_pied()
        new_trajet.approx_dep = station
        new_trajet.approx_arr = itineraire.end_pos
        temps_pied = new_trajet.get_temps_approx(user)

        new_trajet2 = Parcours_inter_station()
        new_trajet2.exact_dep = best_start_station
        new_trajet2.exact_arr = station
        temps_velo = new_trajet2.get_temps_exact(user)

        temps_pied_dep = trajet_pied_best_start_stat.get_temps_approx(user)

        temps_total = temps_pied + temps_velo + temps_pied_dep

        temps_stat_arr[temps_total] = (station,new_trajet,new_trajet2)

    ordered_temps_stat_arr = sorted(temps_stat_arr.iterkeys())

    tempsStatPiedDep = []
    tempsStatPiedArr = []

    nb_recherche_stat_dep = 3
    nb_recherche_stat_arr = 3
    if len(stations_dep)<3:
        nb_recherche_stat_dep = len(stations_dep)
    if len(stations_arr)<3:
        nb_recherche_stat_arr = len(stations_arr)

    #pour les 3 premieres stations de DEPART
    for i in range(0,nb_recherche_stat_dep):
        tempsStatPiedDep.append(temps_stat_dep[ordered_temps_stat_dep[i]][1].get_temps_exact(user))
    #3 premieres stations d'ARRIVEE
    for j in range(0,nb_recherche_stat_arr):
        tempsStatPiedArr.append(temps_stat_arr[ordered_temps_stat_arr[j]][1].get_temps_exact(user))

    temps_totaux = {}
    for i in range(0,nb_recherche_stat_dep):
        for j in range(0,nb_recherche_stat_arr):
            new_trajet = Parcours_inter_station()
            new_trajet.exact_dep = temps_stat_dep[ordered_temps_stat_dep[i]][0]
            new_trajet.exact_arr = temps_stat_arr[ordered_temps_stat_arr[j]][0]
            temps_total = new_trajet.get_temps_exact(user)+tempsStatPiedDep[i]+tempsStatPiedArr[j]
            temps_totaux[temps_total] = (new_trajet.exact_dep,new_trajet.exact_arr)

    ordered_total_times = sorted(temps_totaux.iterkeys())
    stat_dep = temps_totaux[ordered_total_times[0]][0]
    stat_arr = temps_totaux[ordered_total_times[0]][1]

    return (stat_dep,stat_arr,ordered_total_times[0])

def getStationsZone(itineraire,user,depart,type,recherche_large=True):
    stations_libres_trouvees = False
    step = 0
    zone_rech = Carre_recherche()
    if depart:
        zone_rech.origine = itineraire.start_pos
    else:
        zone_rech.origine = itineraire.end_pos

    vPied = user.vitesse_pied
    vVelo = user.vitesse_velo

    if type=="velov" and recherche_large:
        rayon_recherche_beg = [0,500,1000,1500]
        rayon_recherche_end = [300,1000,1500,3000]
    elif type=="velov" and not(recherche_large):
        rayon_recherche_end = [200]
    elif type=="blue":
        rayon_recherche_end = [1000,1500,3000,4000]
        vVelo = 12
    elif type=="velo":
        rayon_recherche_end = [300,1000,1500,3000]

    dX = (itineraire.end_pos.lon - itineraire.start_pos.lon)
    dY = (itineraire.end_pos.lat - itineraire.start_pos.lat)
    if not(depart):
        dX = -dX
        dY = -dY

    dX_norme = dX / sqrt(dX**2+dY**2)
    dY_norme = dY / sqrt(dX**2+dY**2)

    #TODO

    while not(stations_libres_trouvees) and step<len(rayon_recherche_end):
        zone_rech.rayon = rayon_recherche_end[step]
        zone_rech.offsetX = dX_norme*itineraire.distance_directe*(vVelo-vPied)/(vVelo+vPied)
        zone_rech.offsetY = dY_norme*itineraire.distance_directe*(vVelo-vPied)/(vVelo+vPied)
        step = step + 1

        zone_rech.calculerCarre()
        if type=="velov":
            stations_proches = getStationVelov(zone_rech,True)
        elif type=="blue":
            stations_proches = getStationBluely(zone_rech,True)
        elif type=="velo":
            stations_proches = getBorneVelo(zone_rech,True)

        if len(stations_proches)>0:
            stations_libres_trouvees = True

    return stations_proches



def calculerItineraire_TCL_optimise(trajet,itineraire_TCL,itineraire_velov,user):
    sections_contigues = False
    sections_retenues = []
    trajets_velov = []
    # trajet_velov_courant = section_velov.trajet.start_pos
    # trajet_velov.start_pos = section_velov
    # for section in itineraire_TCL.troncon:
    #     trajet_equivalent = Trajet()
    #     trajet_equivalent.start_pos = section.trajet.start_pos
    #     trajet_equivalent.end_pos = section.trajet.end_pos
    #     (stat_dep,stat_arr,duree) = Moyen_velov.calculerItineraire(trajet_equivalent,user)
    #     if section.duree > itineraire.duree:
    #         sections_retenues.append()


class DistanceInterStation(models.Model):
    stationDepart = models.ForeignKey(Station_velov,related_name="stationDepart")
    stationArrivee = models.ForeignKey(Station_velov,related_name="stationArrivee")
    distance = models.IntegerField(default=0)

#Exprime la vitesse de l'utilisateur dans un moyen de transport donne
#les vitesses sont exprimees en metres par seconde
# class VitesseUtilisateur(models.Model):
#     moyen_transport = models.ForeignKey(MoyenTransport)
#     personne = models.ForeignKey(Personne)
#     temps_demarrage = models.IntegerField()
#     temps_arret = models.IntegerField()
#     vitesse = models.IntegerField()
#     vitesseMin = models.IntegerField(default=1)
#     vitesseMax = models.IntegerField(default=2)
#
#     #Retourne la duree en seconde en focntion de la distance en metres
#     def calcul_duree(self,distance):
#         duree = distance/self.vitesse + self.temps_demarrage + self.temps_arret
#         return duree
#
#     def calcul_dureeMin(self,distance):
#         duree = distance/self.vitesseMax + self.temps_demarrage*0.9 + self.temps_arret*0.9
#
#     def set_vitesse(self,vitesseKMH,vitesseMaxKMH=1,vitesseMinKMH=2):
#         self.vitesse = vitesseKMH/3.6
#         self.vitesseMax = vitesseMaxKMH/3.6
#         self.vitesseMin = vitesseMinKMH/3.6
#         return self.vitesse

class Trajet(models.Model):
    start_pos = models.ForeignKey(Lieu,related_name="start_trajet_pos")
    end_pos = models.ForeignKey(Lieu,related_name="end_trajet_pos")
    #moyens_transports_demande =[]# models.ManyToManyField(MoyenTransport)
    distance_directe = models.IntegerField(default=0)

    def est_non_nul(self):
        if abs(self.start_pos.lon-self.end_pos.lon)<0.000001 and abs(self.start_pos.lat-self.end_pos.lat)<0.000001:
            return False
        return True

    def calculer_distance_directe(self):
        #self.personne.getVitesse(Moyen_pied())
        self.distance_directe = sqrt(coordX_to_metres(self.start_pos.lon-self.end_pos.lon)**2+coordY_to_metres(self.start_pos.lat-self.end_pos.lat)**2)
        return self.distance_directe

def get_stations_velov_bluely_combine(trajet,user):
    stations_blue_dep = getStationsZone(trajet,user,True,"blue")
    stations_blue_arr = getStationsZone(trajet,user,False,"blue")
    print "Requete"
    print "--- DEP >>>>"
    print stations_blue_dep
    print "--- ARR >>>>"
    print stations_blue_arr

    dico_trajet_debut_bluely = {}
    dico_trajets = {}
    for station_dep in stations_blue_dep:
        print "---- Calcul velo dep -----"
        print "TO"
        print station_dep
        current_trajet = Trajet()
        current_trajet.start_pos = trajet.start_pos
        current_trajet.end_pos = station_dep
        temps_pied = float(current_trajet.calculer_distance_directe()/user.vitesse_pied)
        temps_velov_min = float(current_trajet.calculer_distance_directe()/user.vitesse_velo+user.temps_start+user.temps_stop)

        if temps_velov_min<temps_pied:
            try:
                dico_trajet_debut_bluely[station_dep] = selectionner_stations_velov(current_trajet,user)
            except:
                print "Erreur calcul trajet velov"
                pass
            print "ooooooooooooooooooooooooooo"
            print "UTILE"
            print "ooooooooooooooooooooooooooo"
        else:
            print "+++++++++++++++++++++++++++"
            print "INUTILE"
            (a,b,temps) = selectionner_stations_velov(current_trajet,user)
            print temps
            print temps_velov_min
            dico_trajet_debut_bluely[station_dep] = (None,None,temps_pied)
            print temps_pied
            print "++++++++++++++++++++++++++++"

    print dico_trajet_debut_bluely
    print "XXXXXXXXXXXXXXXXXXXXXXX"
    for station_arr in stations_blue_arr:
        print "---- Calcul velo arr -----"
        print "TO"
        print station_arr
        current_trajet = Trajet()
        current_trajet.start_pos = station_arr
        current_trajet.end_pos = trajet.end_pos
        temps_pied = 1.2*current_trajet.calculer_distance_directe()/(user.vitesse_pied)
        temps_velov_min = current_trajet.calculer_distance_directe()/user.vitesse_velo+user.temps_start+user.temps_stop
        try:
            if temps_velov_min<temps_pied:
                (velov_fin_stat_dep,velov_fin_stat_arr,velov_fin_duree) = selectionner_stations_velov(current_trajet,user)
                trajet_fin = (velov_fin_stat_dep,velov_fin_stat_arr,velov_fin_duree)
            else :
                velov_fin_duree = temps_pied
                trajet_fin = (None,None,temps_pied)

        except Exception as e:
            print e
            pass
            continue

        for station_dep in stations_blue_dep:
            trajet_en_blue = Trajet()
            trajet_en_blue.start_pos = station_dep
            trajet_en_blue.end_pos = station_arr
            temps_blue = trajet_en_blue.calculer_distance_directe()/12
            dico_trajets[temps_blue+velov_fin_duree+dico_trajet_debut_bluely[station_dep][2]] = (dico_trajet_debut_bluely[station_dep],(trajet_en_blue.start_pos,trajet_en_blue.end_pos,temps_blue),trajet_fin)

    ordered_total_times = sorted(dico_trajets.iterkeys())
    for i in range(5):
        print "porposition1"+str(i)
        print dico_trajets[ordered_total_times[i]]
    return ordered_total_times



def get_directions(fromCoordX,fromCoordY,toCoordX,toCoordY,route_type = "bicycle"):
    #route_type = "bicycle" ou "pedestrian"
    key = "Fmjtd%7Cluur290anu%2Crl%3Do5-908a0y"
    r = requests.get('http://open.mapquestapi.com/directions/v2/route?key=%s&outFormat=json&routeType=%s&timeType=1&enhancedNarrative=true&locale=fr_FR&unit=k&from=%s,%s&to=%s,%s&drivingStyle=2&highwayEfficiency=21.0' %(key,route_type,fromCoordX,fromCoordY,toCoordX,toCoordY)).text
    json_obj = json.loads(r)
    liste_sections = []
    for man in json_obj['route']['legs'][0]['maneuvers']:
        s = Section()
        s.index = man['index']
        s.direction = man['direction']
        s.streets = man['streets']
        #s.maneuverNotes = man['maneuverNotes
        print man['maneuverNotes']
        s.distance = man['distance']
        s.moyen_transport = man['transportMode']
        s.signs = man['signs']
        s.iconUrl = man['iconUrl']
        s.directionName = man['directionName']
        s.temps = man['time']
        s.narrative = man['narrative']
        l = Lieu()
        l.lat = man['startPoint']['lat']
        l.lon = man['startPoint']['lng']
        l.adresse = man['streets']
        l.save()
        t = Trajet()
        t.start_pos = l
        #TODO:Debug this
        t.end_pos = l
        t.save()
        s.trajet = t
        s.turnType = man['turnType']
        s.en_cours = False
        s.taux_pollution = 0
        s.save()
        liste_sections.append(s)
    return liste_sections


#Classe utilisee pour le calcul d'un itineraire
#la classe doit etre remplie avec les donnees de la
#requete itineraire client
def obtenir_propositions(trajet,transports_demandes,personne):
    #Le trajet est nul
    if not(trajet.est_non_nul()):
        return False
    for moyen_transport in transports_demandes:
        #TODO:Uniformiser
        if moyen_transport == "VLV":
            try:
                (stat_dep,stat_arr,duree) = selectionner_stations_velov(trajet,personne)
            except Exception as error:
                print "ERROR"
                pass
            print "--------"
            print "Station dep "+str(stat_dep.lon)+" "+str(stat_dep.lat)
            print "Station arr "+str(stat_arr.lon)+" "+str(stat_arr.lat)
            sectionPiedD = get_directions(trajet.start_pos.lat,trajet.start_pos.lon,stat_dep.lat,stat_dep.lon,"pedestrian")
            sectionVelov = get_directions(stat_dep.lat,stat_dep.lon,stat_arr.lat,stat_arr.lon)

            #Cas de la Pluie pendant le trajet avec des précipitations supérieures à 2mm
            tempsServeur = int(time.time()) + (5*60) #on ajoute 5 minutes car on concidère qu'on part 5 minutes après avoir lancé l'application
            tempsMarchePied = sectionPiedD[0]
            tempsVelov = sectionVelov[0]

            timestampVelovDepart = (tempsServeur + tempsMarchePied) - ((tempsServeur + tempsMarchePied)%600) #on veut tomber sur un bon timestamp en BD

            i = 0
            velovPluie = False
            idFinVelov = 0

            while(i < tempsVelov):
                temps = timestampVelovDepart + i
                meteo = Data_meteo().objects.get(timestamps = temps)

                if meteo.pluie >= 2.0:
                    velovPluie = True
                    break

                i += 600
                idFinVelov += 1

            #Mise à jour des Temps de Trajet pour le Velov et on supprime le reste
           # if velovPluie == True:
                #i = 0
                #while i < idFinVelov:
                    #sectionVelov[i].time -=  sectionVelov[idFinVelov]
                    #i += 1
                #On ne garde que la sous liste qui nous intéresse
                #sectionVelov = sectionVelov[0:idFinVelov]

                #Calcul de la station de velov la plus proche car il pleut
                #stat_arr.lat = sectionVelov[idFinVelov]
                #stat_arr.lon = sectionVelov[idFinVelov]
                #sectionVelov = get_directions(stat_dep.lat,stat_dep.lon,stat_arr.lat,stat_arr.lon)

            sectionPiedF = get_directions(stat_arr.lat,stat_arr.lon,trajet.end_pos.lat,trajet.end_pos.lon,"pedestrian")
            print sectionVelov
            for section in sectionVelov:
                print "VLV X"+str(section.trajet.start_pos.lon)+" Y"+str(section.trajet.start_pos.lat)
            for section in sectionPiedD:
                print "PDD"+section.narrative+" "+str(section.temps)
            for section in sectionPiedF:
                print "PDF"+section.narrative+" "+str(section.temps)

        if moyen_transport == "FOT":
            toto = False
    return True


# def getTransportInstances(transport):
#     if transport=="VLV":
#         return Moyen_velov()
#
#     elif transport=="TCL":
#         return Moyen_TCL()
#
#     elif transport=="BLU":
#         return False
#
#     elif transport=="FOT":
#         return Moyen_pied()
#
#     elif transport=="VLO":
#         return Moyen_velo()
#     else:
#         return False