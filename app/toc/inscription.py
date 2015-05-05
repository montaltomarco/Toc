__author__ = 'marcomontalto'

from django import forms
from models import Personne

class InscriptionForm(forms.Form):
    email = forms.EmailField(required=True, max_length=100, min_length=5)
    password = forms.CharField(required=True)
    confirmezMdp = forms.CharField(required=True)
    nom = forms.CharField(required=False)
    prenom = forms.CharField(required=False)
    civilite = forms.CharField(required=False)
    adresse = forms.CharField(required=False)
    age = forms.IntegerField(required=False)

class CreatePerson(InscriptionForm):
    connexion = psycopg2.connect(dbname = 'db_data', user = 'postgres', password = 'postgres')

    cur = connexion.cursor()
    new_personne = Personne()
    new_personne.email = InscriptionForm.email
    new_personne.mot_de_pass = InscriptionForm.password
    new_personne.nom = InscriptionForm.nom
    new_personne.prenom = InscriptionForm.prenom

    new_personne.save()
