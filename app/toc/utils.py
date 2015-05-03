__author__ = 'marcomontalto'

from models import Lieu

def getCoordByNames(firstAddress, secondAddress):

    lieux = {}

    lieu1 = Lieu()
    lieu1.adresse = "address"
    lieu1.lat = "lat"
    lieu1.lon = "lon"

    lieu2 = Lieu()
    lieu2.adresse = ""
    lieu2.lat = ""
    lieu2.lon = ""

    lieux['firstAdress'] = lieu1
    #lieux.pop(lieu2)

    return lieux

def getRouteByCoord():
    return True

