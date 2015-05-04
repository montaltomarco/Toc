from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from models import *

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
        nickname = request.POST.get('nickname', '')
        password = request.POST.get('password', '')
        return HttpResponse("Login page <br> Nickname is : "+ nickname + ", Password is : " + password)

@require_http_methods(["GET"])
def getRoute(request):
    fromCoord = request.GET.get('from', '')
    toCoord = request.GET.get('to', '')
    transports = request.GET.get('transports', '')

    response_data = {}



    return JsonResponse(response_data)

@require_http_methods(["GET"])
def getCoordByAddressNames(request):
    firstAddress = request.GET.get('firstAddress', '')
    secondAddress = request.GET.get('secondAddress', '')

    response_data = {}

    response_data = getCoordByNames(firstAddress=firstAddress, secondAddress=secondAddress)

    return JsonResponse(response_data)
    #return HttpResponse("Get Coord By Address Names page<br> firstAddress is : "+ firstAddress + ", secondAddress is : " + secondAddress)

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