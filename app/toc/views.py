# -*- coding: utf-8 -*-
# coding: utf-8

from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from models import *
import requests
import sys
import os
import json

sys.path.append('/app/')
os.environ["DJANGO_SETTINGS_MODULE"] = "app.settings"
from toc.models import *
import django
django.setup()

#Utils
from utils import getCoordByNames
from models import *

# Create your views here.

def index(request):
    return HttpResponse("Index Page")

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