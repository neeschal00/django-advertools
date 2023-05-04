from django.urls import path,include
from . import views

urlpatterns = [
    path("urls/",views.analyseUrl, name='anUrl'),
    path("emoji/search/",views.searchEmoji, name='searchEmoji'),
    path("emoji/extract/",views.extractEmoji, name='extractEmoji'),
    path("stopwords/",views.getStopWords, name='stopwords'),
    path("text/",views.analyzeText, name='analyzeT'),
]

