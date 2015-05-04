from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [

    url(r'^$', 'toc.views.index', name='index'),
    url(r'^login/', 'toc.views.login', name='login'),
    url(r'^route/', 'toc.views.getRoute', name='getRoute'),
    url(r'^coordonnes/', 'toc.views.getCoordByAddressNames', name='getCoordByAddressNames'),
    url(r'^routeSelected/', 'toc.views.setSelectedRoute', name='setSelectedRoute'),
    url(r'^routesPerso/', 'toc.views.getRoutesPerso', name='getRoutesPerso'),
    url(r'^infosRoute/', 'toc.views.getInfosRoute', name='getInfosRoute'),
    url(r'^profile/', 'toc.views.getProfile', name='getProfile'),

]