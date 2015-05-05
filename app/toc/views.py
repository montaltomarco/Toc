# -*- coding: utf-8 -*-
# coding: utf-8

from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from models import *
import requests
import json

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
    if request.method == 'POST':
        return HttpResponse(" Error : Inscription Page Requires POST DATA <br>  ")
    elif request.method == 'GET':

        inscriptionForm = InscriptionForm()
        inscriptionForm.email = request.GET.get('email', '')
        inscriptionForm.password = request.POST.get('password', '')
        inscriptionForm.confirmezMdp = request.POST.get('confirmezMdp', '')
        inscriptionForm.nom = request.POST.get('nom', '')
        inscriptionForm.prenom = request.POST.get('prenom', '')
        inscriptionForm.civilite = request.POST.get('civilite', '')
        inscriptionForm.adresse = request.POST.get('adresse', '')
        inscriptionForm.age = request.POST.get('age', '')

        CreatePerson(InscriptionForm=inscriptionForm)

        return HttpResponse(inscriptionForm.email)

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

    def get_directions(fromCoordX,fromCoordY,toCoordX,toCoordY,route_type = "bicycle"):
        #route_type = "bicycle" ou "pedestrian"
        key = "Fmjtd%7Cluur290anu%2Crl%3Do5-908a0y"
        r = requests.get('http://open.mapquestapi.com/directions/v2/route?key=%s&outFormat=json&routeType=%s&timeType=1&enhancedNarrative=true&locale=fr_FR&unit=k&from=%s,%s&to=%s,%s&drivingStyle=2&highwayEfficiency=21.0' %(key,route_type,fromCoordX,fromCoordY,toCoordX,toCoordY)).text
        json_obj = json.loads(r)
        liste_sections = []
        for man in json_obj['route']['legs'][0]['maneuvers']:
            s = Section()
            s.index = man['index']
            s.direction = man['direction']
            s.streets = man['streets']
            #s.maneuverNotes = man['maneuverNotes
            print man['maneuverNotes']
            s.distance = man['distance']
            s.transportMode = man['transportMode']
            s.signs = man['signs']
            s.iconUrl = man['iconUrl']
            s.directionName = man['directionName']
            s.time = man['time']
            s.narrative = man['narrative']
            l = Lieu()
            l.lat = man['startPoint']['lat']
            l.lon = man['startPoint']['lng']
            l.adresse = man['streets']
            l.save()
            s.startPoint = l
            s.turnType = man['turnType']
            s.encours = False
            s.save()
            liste_sections.append(s)
        return liste_sections
    
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