from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import requests
import json

#Utils
from utils import getCoordByNames

# Create your views here.

def index(request):
    return HttpResponse("Index Page. Welcome to Shifty")

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

    response_data = getCoordByNames(firstAddress=firstAddress, secondAddress=secondAddress)

    return HttpResponse(response_data)

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