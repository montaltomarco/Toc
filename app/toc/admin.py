from django.contrib import admin

# Register your models here.
from .models import Itineraire,Personne,Data_velo,Lieu,Portion_de_route,Profil

admin.site.register(Itineraire)
admin.site.register(Lieu)
admin.site.register(Portion_de_route)
admin.site.register(Profil)
admin.site.register(Personne)
admin.site.register(Data_velo)