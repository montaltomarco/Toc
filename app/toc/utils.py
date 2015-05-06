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
    i = 0
    resp1 = requests.get(u"http://nominatim.openstreetmap.org/search/?q=lyon+%s&format=json" %firstAddress).json()
    print resp1
    for o in resp1:
        i = i+1
        if i<5:
            dict2={}
            dict2[u'lon']= o['lon']
            dict2[u'lat']= o['lat']
            dict2[u'name']= ','.join(o['display_name'].split(",")[:3])
            temp.append(dict2)
        else:
            pass
    i=0

    r2 = requests.get(u"http://nominatim.openstreetmap.org/search/?q=lyon+%s&format=json" %secondAddress).json()
    for o in r2:
        i=i+1
        if i<5:
            dict4={}
            dict4[u'lon']= o['lon']
            dict4[u'lat']= o['lat']
            dict4[u'name']= ','.join(o['display_name'].split(",")[:3])
            temp2.append(dict4)
        else:
            pass
    
    response_data['secondAddress'] = temp2
    response_data['firstAddress'] = temp
    return json.dumps(response_data)