from django.db import models

# Create your models here.
class Itineraire(models.Model):
	type_transport = models.CharField(max_length=200)
	pub_date = models.DateTimeField('date published')
	def __str__(self):
		return self.type_transport