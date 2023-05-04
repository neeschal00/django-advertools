from django.urls import path,include
from . import views

urlpatterns = [
    
    path("robots/",views.robotsToDf, name='robotsdf'),
    path("sitemap/",views.sitemapToDf, name='sitemapdf'),

]