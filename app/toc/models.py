from django.db import models

# Create your models here.
class Lieu(models.Model):
	lat = models.FloatField('Latitude')
	lon = models.FloatField('Longitude')
	adresse = models.CharField(max_length=200)
	def __str__(self):
		return self.adresse.encode('utf-8', errors='replace')

class Portion_de_route(models.Model):
	type_transport = models.CharField(max_length=200)
	en_cours = models.BooleanField('en_cours')
	consomation_co2 = models.FloatField('CO2')
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
	portion = models.ManyToManyField(Portion_de_route)
	persones = models.ManyToManyField(Personne)
	def __str__(self):
		return self.portion.type_transport


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

