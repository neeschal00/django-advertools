from django.urls import path,include
from . import views

urlpatterns = [
    
    path("robots/",views.robotsToDf, name='robotsdf'),
    path("sitemap/",views.sitemapToDf, name='sitemapdf'),
    path("serp/",views.searchEngineResults, name='serp'),
    path("knowledge/",views.knowledgeGraph, name='know'),
    path("crawl/",views.crawl, name='crawl')

]