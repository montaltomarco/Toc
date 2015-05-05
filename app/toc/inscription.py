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

def CreatePerson(form):
    new_personne = Personne()
    new_personne.email = form.email
    new_personne.mot_de_pass = form.password
    new_personne.nom = form.nom
    new_personne.prenom = form.prenom
    new_personne.vitesse_pied = 0
    new_personne.vitesse_velo = 0

    new_personne.save()
