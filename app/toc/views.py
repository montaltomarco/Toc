# -*- coding: utf-8 -*-
# coding: utf-8

from django.shortcuts import render
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
    lieu1 = Lieu()
    lieu2 = Lieu()
    lieu1.lon = 4.874211
    lieu1.lat = 45.7765506
    lieu2.lon = 4.848370
    lieu2.lat = 45.743943
    lieu1.save()
    lieu2.save()
    itineraire = Itineraire()
    itineraire.start_pos = lieu1
    itineraire.end_pos = lieu2
    user = Personne()
    moyen_velov = Moyen_velov()
    moyen_velov.nom = "Velov"
    moyen_velov.code = "VLV"
    moyen_velov.save()
    moyen_velov.calculerItineraire(itineraire,user)


    return HttpResponse("e")

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