from django.db import models
from math import *
from collections import *

# Create your models here.

#coordX etant une coordonnee GPS sens W/E en degres decimaux
def coordX_to_metres(deltaX):
    return deltaX*75750

#coordX etant une coordonnee GPS sens N/S en degres decimaux
def coordY_to_metres(deltaY):
    return deltaY*111120

def metres_to_coordX(distance):
    return distance/7575

def metres_to_coordY(distance):
    return distance/111120

#Definit un reseau de stations et de lignes
# comme le reseau d'arret TCL ou le reseau de velov
class Reseau(models.Model):
    nombreDeStation = models.IntegerField()

    def getStation(self,zoneRecherche,station_depart):

        stations = [Station_velov(), Station_velov(), Station_velov()]
        return stations

reseau_velov = Reseau()
reseau_TCL = Reseau()

class Parcours_temporel(models.Model):
    approx_dep = models.ForeignKey(Lieu,"approx_dep")
    approx_arr = models.ForeignKey(Lieu,"approx_arr")
    exact_dep = models.ForeignKey(Lieu,"exact_dep")
    exact_arr = models.ForeignKey(Lieu,"exact_arr")

    exact_calc = models.BooleanField()
    approx_calc = models.BooleanField()

    current_time = models.IntegerField()

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
        #TODO: integration user
        user_speed = 5
        vecteur = Vecteur()
        vecteur.depart = self.approx_dep
        vecteur.arrivee = self.approx_arr
        temps_approx = vecteur.calculer_distance()/user_speed
        self.temps = temps_approx
        return temps_approx

    def get_temps_exact(self,user):
        #TODO: integeration user
        user_speed = 5
        return self.get_temps_approx(user)

class Parcours_pied(Parcours_temporel):
    def get_temps_approx(self,user):
        #TODO: integration user
        user_speed = 1
        vecteur = Vecteur()
        vecteur.depart = self.approx_dep
        vecteur.arrivee = self.approx_arr
        temps_approx = vecteur.calculer_distance()/user_speed
        self.temps = temps_approx
        return temps_approx

    def get_temps_exact(self,user):
        #TODO: integeration user
        user_speed = 1
        if self.exact_calc:
            return self.current_time
        else:
            return self.get_temps_approx(user)

class Lieu(models.Model):
	lat = models.FloatField('Latitude')
	lon = models.FloatField('Longitude')
	adresse = models.CharField(max_length=200)
	def __str__(self):
		return self.adresse.encode('utf-8', errors='replace')

class Section(models.Model):
	moyen_transport = models.ForeignKey("MoyenTransport")
	en_cours = models.BooleanField('en_cours')
	distance = models.IntegerField()
	taux_pollution = models.FloatField('Pollution')

class Personne(models.Model):
	nom = models.CharField(max_length=200)
	prenom = models.CharField(max_length=200)
	email = models.CharField(max_length=200)
	mot_de_pass = models.CharField(max_length=200)
	def __str__(self):
		return self.nom + ' ' + self.prenom

class Itineraire(models.Model):
    start_pos = models.ForeignKey(Lieu,related_name="start_pos")
    end_pos = models.ForeignKey(Lieu,related_name="end_pos")
    sections = models.ManyToManyField(Section)
    personnes = models.ManyToManyField(Personne)
    distance_directe = models.IntegerField(default=0)

    def calculer_distance_directe(self):
        #self.personne.getVitesse(Moyen_pied())
        return sqrt(coordX_to_metres(self.trajet.depart_traj.lon-self.trajet.arrivee_traj.lon)**2+coordY_to_metres(self.trajet.depart_traj.lat-self.trajet.arrivee_traj.lat)**2)

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

class Ligne_TCL(models.Model):
    reseau = models.ForeignKey(Reseau)
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
    reseau = models.ForeignKey(Reseau)
    #id = models.IntegerField()
    nom = models.CharField(max_length = 100)
    lignes = models.ManyToManyField(Ligne_TCL)
    pmr = models.BooleanField()
    escalator = models.BooleanField()

    def __str__(self):
        return self.nom+" "+super(Arret_TCL,self).__str__()

#Definit un carre autour d'un point d'origine afin de fournir des coordonnees
#de polygone en vue d'une recherche (stations Velov environnantes par exemple)
class Carre_recherche(models.Model):
    origine = models.ForeignKey(Lieu)
    #rayon en metres
    rayon = models.IntegerField()
    #offset POSITIF exprimant un decalage vers l'EST en metres
    offsetX = models.IntegerField()
    #offset POSITIF exprimant le decalage vers le NORD en metres
    offsetY = models.IntegerField()

    #begX : extreme OUEST en coord
    begX = models.FloatField()
    #begY : extreme SUD en coord
    begY = models.FloatField()

    #endX : extreme EST en coord
    endX = models.FloatField()
    #endY : extreme NORD en coord
    endY = models.FloatField()

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

    def __init__(self, departP, arriveeP):
        self.depart = departP
        self.arrivee = arriveeP
        self.calculer_distance()

    def calculer_distance(self):
        deltaT = coordY_to_metres(abs(self.depart.lat - self.depart.lat))
        deltaL = coordX_to_metres(abs(self.arrivee.lon - self.depart.lon))
        self.distance = sqrt(deltaT**2+deltaL**2)
        return self.distance

class MoyenTransport(models.Model):
    nom = models.CharField(max_length=30)
    code = models.CharField(max_length=20)
    parent = models.ForeignKey('self')
    #enfant = models.ManyToOneField(MoyenTransport)

    def __init__(self, nomP, codeP, parentP):
        self.nom = nomP
        self.code = codeP
        self.parent = parentP

    def calculerItineraire(self,itineraire):
        return False

class Moyen_velov(MoyenTransport):
    rayon_recherche_beg = [0,500,1000,1500]
    rayon_recherche_end = [500,1000,1500,3000]

    def calculerItineraire(self,itineraire,user):
        stations_dep = self.getStationsZone(itineraire,user,True)
        stations_arr = self.getStationsZone(itineraire,user,False)
        if len(stations_dep)==0 or len(stations_arr)==0 :
            return False

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

        ordered_temps_stat_dep = sorted(temps_stat_dep.iterkeys()).items()

        #On recupere la meilleure station
        best_start_station = ordered_temps_stat_dep[1][0]
        trajet_pied_best_start_stat = ordered_temps_stat_dep[1][1]

        temps_stat_arr = {}
        for station in stations_arr:
            #Creation trajets pied entre dep et stat dep
            new_trajet = Parcours_pied()
            new_trajet.approx_dep = station
            new_trajet.approx_arr = itineraire.end_pos
            temps_pied = new_trajet.get_temps_approx(user)

            new_trajet2 = Parcours_inter_station()
            new_trajet2.approx_dep = best_start_station
            new_trajet2.approx_arr = station
            temps_velo = new_trajet2.get_temps_exact(user)

            temps_pied_dep = trajet_pied_best_start_stat

            temps_total = temps_pied + temps_velo + temps_pied_dep

            temps_stat_arr[temps_total] = (station,new_trajet,new_trajet2)

        ordered_temps_stat_arr = sorted(temps_stat_arr.iterkeys()).items()

        tempsStatPiedDep = []
        tempsStatPiedArr = []
        #pour les 3 premieres stations de DEPART
        for i in range(0,2):
            tempsStatPiedDep[i] = ordered_temps_stat_dep[1][1].get_temps_exact(user)
        #3 premieres stations d'ARRIVEE
        for j in range(0,2):
            tempsStatPiedArr[j] = ordered_temps_stat_arr[1][1].get_temps_exact(user)

        temps_totaux = {}
        for i in range(0,2):
            for j in range(0,2):
                new_trajet = Parcours_inter_station()
                new_trajet.exact_dep = ordered_temps_stat_dep[1][i]
                new_trajet.exact_arr = ordered_temps_stat_arr[1][j]
                temps_total = new_trajet.get_temps_exact(user)+tempsStatPiedDep[i]+tempsStatPiedArr[j]
                temps_totaux[(i,j)] = temps_total

        ordered_total_times = sorted(temps_totaux.iteritems()).items()
        stat_dep = ordered_temps_stat_dep[ordered_total_times[0][0][0]]
        stat_arr = ordered_temps_stat_arr[ordered_total_times[0][0][1]]

        return (stat_dep,stat_arr)

    def getStationsZone(self,itineraire,user,depart):
        stations_libres_trouvees = False
        step = 0;
        zone_rech = Carre_recherche()
        zone_rech.origine = itineraire.start_pos
        dX = (itineraire.end_pos.lon - itineraire.start_pos.lon)
        dY = (itineraire.end_pos.lat - itineraire.start_pos.lat)
        if not(depart):
            dX = -dX
            dY = -dY

        dX_norme = dX / sqrt(dX**2+dY**2)
        dY_norme = dY / sqrt(dX**2+dY**2)

        #TODO
        vPied = 1
        vVelo = 5

        while not(stations_libres_trouvees and step<len(self.rayon_recherche_end)):
            zone_rech.rayon = self.rayon_recherche_end[step]
            zone_rech.offsetX = dX_norme*itineraire.distance_directe*(vVelo-vPied)/(vVelo+vPied)
            zone_rech.offsetY = dY_norme*itineraire.distance_directe*(vVelo-vPied)/(vVelo+vPied)

            zone_rech.calculerCarre()
            stations_proches = reseau_velov.getStation(zone_rech,True)

        return stations_proches


class Moyen_pied(MoyenTransport):
    def calculerItineraire(self,itineraire):
        return True

class Moyen_TCL(MoyenTransport):
    def calculerItineraire(self,itineraire):
        return True

class DistanceInterStation(models.Model):
    stationDepart = models.ForeignKey(Station_velov,related_name="stationDepart")
    stationArrivee = models.ForeignKey(Station_velov,related_name="stationArrivee")
    distance = models.IntegerField(default=0)

#Exprime la vitesse de l'utilisateur dans un moyen de transport donne
#les vitesses sont exprimees en metres par seconde
class VitesseUtilisateur(models.Model):
    moyen_transport = models.ForeignKey(MoyenTransport)
    personne = models.ForeignKey(Personne)
    temps_demarrage = models.IntegerField()
    temps_arret = models.IntegerField()
    vitesse = models.IntegerField()
    vitesseMin = models.IntegerField(default=1)
    vitesseMax = models.IntegerField(default=2)

    #Retourne la duree en seconde en focntion de la distance en metres
    def calcul_duree(self,distance):
        duree = distance/self.vitesse + self.temps_demarrage + self.temps_arret
        return duree

    def calcul_dureeMin(self,distance):
        duree = distance/self.vitesseMax + self.temps_demarrage*0.9 + self.temps_arret*0.9

    def set_vitesse(self,vitesseKMH,vitesseMaxKMH=1,vitesseMinKMH=2):
        self.vitesse = vitesseKMH/3.6
        self.vitesseMax = vitesseMaxKMH/3.6
        self.vitesseMin = vitesseMinKMH/3.6
        return self.vitesse

class TrajetSection(models.Model):
    consomation_co2 = models.FloatField('CO2')
    moyen = models.ForeignKey(MoyenTransport)
    distance = models.IntegerField()


class PropositionItineraire(models.Model):
    #parent = models.ForeignKey(DemandeItineraire)
    moyen = models.ManyToManyField(MoyenTransport)
    itineraire = models.ForeignKey(Itineraire)

    def update_moyen(self):
        for section in self.itineraire.sections:
            self.add(section.moyen_transport)

class Trajet(models.Model):
    depart_traj = models.ManyToManyField(Lieu,related_name="departTraj")
    arrivee_traj = models.ManyToManyField(Lieu,related_name="arriveeTraj")
    moyens_transports_demande = models.ManyToManyField(MoyenTransport)

    def est_non_nul(self):
        if abs(self.depart_traj.lon-self.arrivee_traj.lon)<0.000001 and abs(self.depart_traj.lat-self.arrivee_traj.lat)<0.000001:
            return False
        return True

#Classe utilisee pour le calcul d'un itineraire
#la classe doit etre remplie avec les donnees de la
#requete itineraire client
class DemandeItineraire(models.Model):
    trajet = models.ForeignKey(Trajet)
    listeProposition = models.ManyToManyField(PropositionItineraire)
    personne = models.ForeignKey(Personne)

    def obtenir_propositions(self):
        #Le trajet est nul
        if not(self.trajet.est_non_nul()):
            return False
        return True

