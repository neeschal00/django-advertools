from django.urls import path,include
from . import views

urlpatterns = [
    path('advertisement/large/',views.generateLarge,name='largeAds'),
    path("advertisement/",views.generateDescription, name='advertisement'),
    path("keywords/",views.generateKeywords, name='keywords'),


]