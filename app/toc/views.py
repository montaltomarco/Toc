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
from django.core import serializers
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

        print request.POST.get('email', '')
        print request.POST.get('password', '')
        print request.POST.get('confirmezMdp', '')
        print request.POST.get('nom', '')
        print request.POST.get('prenom', '')
        print request.POST.get('civilite', '')
        print request.POST.get('adresse', '')
        print request.POST.get('age', '')

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

        CreatePerson(form=inscriptionForm)

        response[u'status'] = u'ok'
        response[u'message'] = inscriptionForm.email
        response[u'prenom'] = inscriptionForm.prenom

        return JsonResponse(response)

@require_http_methods(["GET", "POST"])
@csrf_exempt
def login(request):

    response={}

    if request.method == 'GET':
        return HttpResponse(" Error : Login Page Requires POST DATA <br>  ")
    elif request.method == 'POST':
        mail = request.POST.get('email', '')
        password = request.POST.get('password', '')

        try:
            p = Personne.objects.get(email=mail)
        except:
            response[u'status'] = u'error'
            return JsonResponse(response)
        if p:
            if p.mot_de_pass == password :
                response[u'status'] = u'ok'
                response[u'prenom'] = p.prenom

                return JsonResponse(response)
            else:
                response[u'status'] = u'error'
                return JsonResponse(response)
        else:
                response[u'status'] = u'error'
                return JsonResponse(response)

@require_http_methods(["GET"])
def getRoute(request):
    def __get_transport(obj) :
        if type(obj) == "toc.Station_velov":
            return "bicycle"
        else:
            return "fastest"

    def getCurrentMeteo():
        currentTimeStamp = int(time.time())
        timestampDB = currentTimeStamp - (currentTimeStamp%600)
        print timestampDB
        """
        try:
            return Data_meteo.objects.get(timestamps=timestampDB)
        except:
            return  None"""

    def __get_nom_transport(obj) :
        if type(obj) == "toc.Station_velov":
            return "Velo'V"
        else:
            return "BlueLY"

    lieu_dep = Lieu()
    lieu_arr = Lieu()

    lieu_dep.lon = float(request.GET.get('fromX', ''))
    lieu_dep.lat = float(request.GET.get('fromY', ''))
    lieu_arr.lon = float(request.GET.get('toX', ''))
    lieu_arr.lat = float(request.GET.get('toY', ''))
    #TODO:Recuperer une liste (cette ligne est suffisante?)
    transports = request.GET.get('transports', '')
    #print transports
    lieu_dep.save()
    lieu_arr.save()
    transports = ["VLV","BLU"]

    trajet = Trajet()
    trajet.start_pos = lieu_dep
    trajet.end_pos = lieu_arr


    #TODO:Remplacer le faux user par celui de la session
    user = Personne()
    try:
        resp = get_stations_velov_bluely_combine(trajet,user)
    except:
        resp=""
    data = []
    def __get_pluie():
        meteo = getCurrentMeteo()
        if meteo.pluie>2.5:
            return "Pluie"
        else:
            return "Soleil"

    def __get_temperature():
        return getCurrentMeteo().temperature
    getCurrentMeteo()
    data.append("Soleil")
    data.append("18C")
    print "-----------------------------------------------------------------------------------------------------"
    #obtenir_propositions(trajet,transports,user)
    #data = serializers.serialize("json", resp)
    try:
        temp = get_directions(lieu_dep.lat,lieu_dep.lon,resp[0][0].lat,resp[0][0].lon,"pedestrian")
        for t in temp:
            data.append("A Pied")
            data.append(t.narrative)
    except:pass
    print data
    i = 0
    for r in resp:
        try:
            temp = get_directions(r[0].lat,r[0].lon,r[1].lat,r[1].lon,__get_transport(r[0]))
            i = i+1
            print r[0].lat,r[0].lon,r[1].lat,r[1].lon
            for t in temp:
                data.append(__get_nom_transport(r[0]))
                data.append(t.narrative)
        except:
            print "exception. I:"
            print i
            continue
    try:
        temp = get_directions(resp[i][1].lat,resp[i][1].lon,lieu_arr.lat,lieu_arr.lon,"pedestrian")
        for t in temp:
            data.append("A Pied")
            data.append(t.narrative)
    except:pass

    """for r in resp:
        try:
            temp = get_directions(lieu_dep.lat,lieu_dep.lon,r[0].lat,r[0].lon,"pedestrian")

           

    try:
        temp = get_directions(lieu_dep.lat,lieu_dep.lon,resp[0][0].lat,resp[0][0].lon,"pedestrian")
        for t in temp:
            data.append(t.moyen_transport)
            data.append(t.narrative)
    except:
        pass
    try:
        temp = get_directions(resp[0][0].lat,resp[0][0].lon, resp[1][0].lat,resp[1][0].lon,"bicycle")
        data.append("BICYCLE")
        data.append("Vous devez Prendre Le velo ici")
        for t in temp:
            data.append(t.moyen_transport)
            data.append(t.narrative)
    except:
        pass
    try:
        temp = get_directions(resp[1][0].lat,resp[1][0].lon, resp[2][0].lat,resp[2][0].lon,"fastest")
        data.append("AUTO")
        data.append("Vous devez Prendre La voiture ici")
        for t in temp:
            data.append(t.moyen_transport)
            data.append(t.narrative)
    except:
        temp = get_directions(resp[1][0].lat,resp[1][0].lon, lieu_dep.lat,lieu_dep.lon,"pedestrian")
        for t in temp:
            data.append("WALKING")
            data.append(t.narrative)
        pass
    try:
        temp = get_directions(resp[2][0].lat,resp[2][0].lon, lieu_dep.lat,lieu_dep.lon,"pedestrian")
        for t in temp:
            data.append("WALKING")
            data.append(t.narrative)
    except:
        pass
         """
    #r = (requests.get('http://open.mapquestapi.com/directions/v2/route?key=Fmjtd%7Cluur290anu%2Crl%3Do5-908a0y&from=45.7695736,4.8534248&to=49.46223865,3.82243905078971&routeType=bicycle&manMaps=false&shapeFormat=raw&generalize=0&unit=k').text)
    response_data = {}
    #response_data = {}
        #print type(r[0])
    #return JsonResponse(resp)
    print data
    return HttpResponse(json.dumps(data))

@require_http_methods(["GET"])
def getCoordByAddressNames(request):
    firstAddress = request.GET.get('firstAddress', '')
    secondAddress = request.GET.get('secondAddress', '')
    print firstAddress
    print secondAddress
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

    ((velovDO,velovDD,d1),(blueStatO,blueStatD,d2),(velovFO,velovFD,d3))= get_stations_velov_bluely_combine(trajet,user)
    print "VV1"+str(velovDD.lon)
    print "VV2"+str(velovFD.lat)
    print "VV3"+str(blueStatD.lon)
    print "VV4"+str(blueStatO.lat)
    return HttpResponse("E")
