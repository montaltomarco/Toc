__author__ = 'marcomontalto'

# -*- coding: utf-8 -*-
# coding: utf-8

import requests
import json

def getCoordByNames(firstAddress, secondAddress):
    dict = {}
    dict2={}
    dict3 = {}
    dict4={}
    temp = []
    temp2 = []
    response_data = {}

    resp1 = requests.get(u"http://nominatim.openstreetmap.org/search/?q=lyon+%s&format=json" %firstAddress).json()
    for o in resp1:
        dict2={}
        dict2[u'lon']= o['lon']
        dict2[u'lat']= o['lat']
        dict2[u'name']= o['display_name']
        temp.append(dict2)
    dict[u'firstAddress'] = temp

    r2 = requests.get(u"http://nominatim.openstreetmap.org/search/?q=lyon+%s&format=json" %secondAddress).json()
    for o in r2:
        dict4={}
        dict4[u'lon']= o['lon']
        dict4[u'lat']= o['lat']
        dict4[u'name']= o['display_name']
        temp2.append(dict4)
    response_data['firstAddress'] = temp
    response_data['secondAddress'] = temp2

    return json.dumps(response_data)