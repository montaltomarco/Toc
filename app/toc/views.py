# -*- coding: utf-8 -*-
# coding: utf-8

from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from models import *
import requests
import json
import re

#Utils
from utils import getCoordByNames
from models import *
from inscription import InscriptionForm, CreatePerson

# Create your views here.

def index(request):
    return HttpResponse("Index Page")

@require_http_methods(["GET", "POST"])
@csrf_exempt
def inscription(request):

    response={}

    if request.method == 'GET':
        response[u'status'] = u'error'
        response[u'message'] = u'Error - Inscription Requires POST DATA'
        return JsonResponse(response)

    elif request.method == 'POST':
        inscriptionForm = InscriptionForm()
        inscriptionForm.email = request.POST.get('email', '')
        inscriptionForm.password = request.POST.get('password', '')
        inscriptionForm.confirmezMdp = request.POST.get('confirmezMdp', '')
        inscriptionForm.nom = request.POST.get('nom', '')
        inscriptionForm.prenom = request.POST.get('prenom', '')
        inscriptionForm.civilite = request.POST.get('civilite', '')
        inscriptionForm.adresse = request.POST.get('adresse', '')
        inscriptionForm.age = request.POST.get('age', '')

        if not re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", inscriptionForm.email) or inscriptionForm.email=='' :
            response[u'status'] = u'error'
            response[u'message'] = u'Error - email - ' + inscriptionForm.email + u" doesn't respect the required format"
            return JsonResponse(response)

        if inscriptionForm.password!=inscriptionForm.confirmezMdp or inscriptionForm.password=='':
            print inscriptionForm.password
            print inscriptionForm.confirmezMdp
            response[u'status'] = u'error'
            response[u'message'] = u'Error - les deux mot de passe ne correspondent pas.'
            return JsonResponse(response)

        if inscriptionForm.civilite:
            if inscriptionForm.civilite!='Madame' and inscriptionForm.civilite!='Monsieur':
                response[u'status'] = u'error'
                response[u'message'] = u'Error - vous pouvez seulement etre un monsieur ou une madame.'
                return JsonResponse(response)

        CreatePerson(form=inscriptionForm)

        response[u'status'] = u'ok'
        response[u'message'] = inscriptionForm.email
        return JsonResponse(response)

@require_http_methods(["GET", "POST"])
@csrf_exempt
def login(request):
    if request.method == 'GET':
        return HttpResponse(" Error : Login Page Requires POST DATA <br>  ")
    elif request.method == 'POST':
        mail = request.POST.get('mail', '')
        password = request.POST.get('password', '')
        p = Personne.objects.get(email=mail)
        if p.mot_de_pass == password :
            return HttpResponse("Login page <br> email is : "+ mail + ", Password is : " + password)
        else:
            return HttpResponse("email invalid ou mot de passe erroné")

@require_http_methods(["GET"])
def getRoute(request):
    lieu_dep = Lieu()
    lieu_arr = Lieu()

    lieu_dep.lon = float(request.GET.get('fromX', ''))
    lieu_dep.lat = float(request.GET.get('fromY', ''))
    lieu_arr.lon = float(request.GET.get('toX', ''))
    lieu_arr.lat = float(request.GET.get('toY', ''))
    #TODO:Recuperer une liste (cette ligne est suffisante?)
    transports = request.GET.get('transports', '')
    print transports
    lieu_dep.save()
    lieu_arr.save()
    transports = ["VLV"]
    trajet = Trajet()
    trajet.start_pos = lieu_dep
    trajet.end_pos = lieu_arr

    #TODO:Remplacer le faux user par celui de la session
    user = Personne()

    obtenir_propositions(trajet,transports,user)


    #r = (requests.get('http://open.mapquestapi.com/directions/v2/route?key=Fmjtd%7Cluur290anu%2Crl%3Do5-908a0y&from=45.7695736,4.8534248&to=49.46223865,3.82243905078971&routeType=bicycle&manMaps=false&shapeFormat=raw&generalize=0&unit=k').text)
    response_data = {}

    #response_data = {}

    #return JsonResponse(r)
    return HttpResponse("FE")

@require_http_methods(["GET"])
def getCoordByAddressNames(request):
    firstAddress = request.GET.get('firstAddress', '')
    secondAddress = request.GET.get('secondAddress', '')

    response_data = getCoordByNames(firstAddress=firstAddress, secondAddress=secondAddress)

    print response_data

    return HttpResponse(response_data, content_type='application/json; charset=utf-8')

@require_http_methods(["GET"])
def setSelectedRoute(request):
    idroute = request.GET.get('idroute', '')
    return HttpResponse("Set Selected Route page <br> idroute is : "+idroute)

@require_http_methods(["GET"])
def getRoutesPerso(request):
    return HttpResponse("Show infos personal routes page <br> NO params ")

@require_http_methods(["GET"])
def getInfosRoute(request):
    idroute = request.GET.get('idroute', '')
    return HttpResponse("Show infos one personal route page <br> idroute is : "+idroute)

@require_http_methods(["GET"])
def getProfile(request):
    return HttpResponse("Show personal infos page<br> NO params")


def tests_dams(request):
    lieu1 = Lieu()
    lieu2 = Lieu()
    lieu1.lon = 4.842812
    lieu1.lat = 45.752029
    lieu2.lon = 4.8550066229888000
    lieu2.lat = 45.7629790120815000
    lieu1.save()
    lieu2.save()
    trajet = Trajet()

    moyen_transports_demande = "VLV"
    trajet.start_pos = lieu1
    trajet.end_pos = lieu2
    user = Personne()

    selectionner_stations_velov(trajet,user)

    return HttpResponse("E")
