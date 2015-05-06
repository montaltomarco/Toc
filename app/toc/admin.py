from django.contrib import admin

# Register your models here.
from .models import Itineraire,Personne,Data_velo,Lieu, Profil,Data_meteo,Station_velov,Station_autopartage
    #Portion_de_route,

admin.site.register(Itineraire)
admin.site.register(Lieu)
#admin.site.register(Portion_de_route)
admin.site.register(Profil)
admin.site.register(Personne)
admin.site.register(Data_velo)
admin.site.register(Data_meteo)
admin.site.register(Station_velov)
admin.site.register(Station_autopartage)