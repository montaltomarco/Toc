from django.db import models
from math import sqrt

# Create your models here.
class Lieu(models.Model):
	lat = models.FloatField('Latitude')
	lon = models.FloatField('Longitude')
	adresse = models.CharField(max_length=200)
	def __str__(self):
		return self.adresse.encode('utf-8', errors='replace')

class Section(models.Model):
	type_transport = models.CharField(max_length=200)
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
    #sections = models.ManyToOneField(Section)
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

class Ligne_TCL(models.Model):
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
    #id = models.IntegerField()
    nom = models.CharField(max_length = 100)
    lignes = models.ManyToManyField(Ligne_TCL)
    pmr = models.BooleanField()
    escalator = models.BooleanField()

    def __str__(self):
        return self.nom+" "+super(Arret_TCL,self).__str__()

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
        deltaT = abs(self.depart.lat - self.depart.lat)*111.120
        deltaL = abs(self.arrivee.lon - self.depart.lon)*75.75
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

class Section(models.Model):
    consomation_co2 = models.FloatField('CO2')
    moyen = models.ForeignKey(MoyenTransport)
    distance = models.IntegerField()


class PropositionItineraire(models.Model):
    #parent = models.ForeignKey(DemandeItineraire)
    moyen = models.ManyToManyField(MoyenTransport)
    itineraire = models.ForeignKey(Itineraire)

class Trajet(models.Model):
    departTraj = models.ManyToManyField(Lieu,related_name="departTraj")
    arriveeTraj = models.ManyToManyField(Lieu,related_name="arriveeTraj")
    moyens_transports_demande = models.ManyToManyField(MoyenTransport)

#Classe utilisee pour le calcul d'un itineraire
#la classe doit etre remplie avec les donnees de la
#requete itineraire client
class DemandeItineraire(models.Model):
    trajet = models.ForeignKey(Trajet)
    #listeProposition = models.OneToMany(PropositionItineraire)

