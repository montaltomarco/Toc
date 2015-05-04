__author__ = 'marcomontalto'

import requests
import json

def getCoordByNames(firstAddress, secondAddress):
    dict = {}
    dict2={}
    dict3 = {}
    dict4={}
    temp = []
    temp2 = []

    r = json.loads((requests.get("http://nominatim.openstreetmap.org/search/?q=%s&format=json" %firstAddress)).text.encode('utf-8', errors='replace'))
    for o in r:
        dict2={}
        dict2["lon"]= o["lon"]
        dict2["lat"]= o["lat"]
        dict2["name"]= o["display_name"].encode('utf8')
        temp.append(dict2)
    dict['firstAdress']= temp
    print(dict)

    r2 = json.loads((requests.get("http://nominatim.openstreetmap.org/search/?q=%s&format=json" %secondAddress)).text.encode('utf-8', errors='replace'))
    for o in r2:
        dict4={}
        dict4["lon"]= o["lon"]
        dict4["lat"]= o["lat"]
        dict4["name"]= o["display_name"].encode('utf8')
        temp2.append(dict4)
    dict3['secondAdress']= temp2
    print(dict3)
    return r