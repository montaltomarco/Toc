# -*- coding: utf-8 -*-
# coding: utf-8

from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from models import *
#from stations_metrodb import refresh_database
import requests
import json

#Utils
from utils import getCoordByNames
from models import *

# Create your views here.

def index(request):
    lieu1 = Lieu()
    lieu2 = Lieu()
    lieu1.lon = 4.874211
    lieu1.lat = 45.7765506
    lieu2.lon = 4.848370
    lieu2.lat = 45.743943
    lieu1.save()
    lieu2.save()
    itineraire = Trajet()

    station1 = Arret_TCL()
    station1.lat = lieu1.lat
    station1.lon = lieu1.lon
    station1.escalator = True
    station1.id_station = 1
    station1.pmr = True
    station2 = Arret_TCL()
    station2.lat = lieu1.lat
    station2.lon = lieu1.lon
    station2.pmr = True
    station2.id_station = 1
    station2.escalator = True
    station1.save()
    station2.save()

    arret1 = Station_velov()
    arret1.lat = lieu1.lat
    arret1.lon = lieu1.lon
    arret1.number_station = 1
    arret1.nb_velos = 0
    arret1.nb_places = 0
    arret2 = Station_velov()
    arret2.lat = lieu2.lat
    arret2.lon = lieu2.lon
    arret2.number_station = 1
    arret2.nb_velos = 0
    arret2.nb_places = 0
    arret1.save()
    arret2.save()

    station1.stations_velov_proches.add(arret1)
    station1.stations_velov_proches.add(arret2)
    station1.save()

    print "-------------------------------"
    toto = station1.stations_velov_proches.all()
    print toto.count()
    for stat in toto:
        print stat.lat
    print "wwwwwwwwwwwwwwwwwwwwwwwwwwwwwww"

    moyen_velov = Moyen_velov()
    moyen_velov.nom = "Velov"
    moyen_velov.code = "VLV"
    moyen_velov.save()

    itineraire.moyen_transports_demande = moyen_velov
    itineraire.start_pos = lieu1
    itineraire.end_pos = lieu2
    user = Personne()

    moyen_velov.calculerItineraire(itineraire,user)


    return HttpResponse("e")

@require_http_methods(["GET", "POST"])
@csrf_exempt
def login(request):
    if request.method == 'GET':
        return HttpResponse(" Error : Login Page Requires POST DATA <br>  ")
    elif request.method == 'POST':
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        return HttpResponse("Login page <br> Nickname is : "+ email + ", Password is : " + password)

@require_http_methods(["GET"])
def getRoute(request):
    fromCoordX = request.GET.get('fromX', '')
    fromCoordY = request.GET.get('fromY', '')
    toCoordX = request.GET.get('toX', '')
    toCoordY = request.GET.get('toY', '')
    transports = request.GET.get('transports', '')
    transports = getTransportInstance("TOTO")
    lieu_dep = Lieu()
    lieu_dep.lat = fromCoordY
    lieu_dep.lon = fromCoordX
    lieu_arr = Lieu()
    lieu_dep.lat = toCoordX
    lieu_dep.lon = toCoordY
    trajet = Trajet()
    trajet.start_pos = lieu_dep
    trajet.end_pos = lieu_arr
    for transport in transports :
        trajet.moyens_transports_demande.add()
    demande_courante = DemandeItineraire()


    r = (requests.get('http://open.mapquestapi.com/directions/v2/route?key=Fmjtd%7Cluur290anu%2Crl%3Do5-908a0y&from=45.7695736,4.8534248&to=49.46223865,3.82243905078971&routeType=bicycle&manMaps=false&shapeFormat=raw&generalize=0&unit=k').text)

    response_data = {}

    return JsonResponse(r)

@require_http_methods(["GET"])
def getCoordByAddressNames(request):
    firstAddress = request.GET.get('firstAddress', '')
    secondAddress = request.GET.get('secondAddress', '')

    response_data = getCoordByNames(firstAddress=firstAddress, secondAddress=secondAddress)

    #print response_data["firstAddress"]

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