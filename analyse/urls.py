from django.urls import path,include
from . import views

urlpatterns = [
    path("urls/",views.analyseUrl, name='anUrl'),
    path("emoji/search/",views.searchEmoji, name='searchEmoji'),
    path("emoji/extract/",views.extractEmoji, name='extractEmoji'),
    path("stopwords/",views.getStopWords, name='stopwords'),
    path("text/overview/",views.overviewText, name='overviewT'),
    path("text/analyze/",views.dataSetAnalysis, name='datasetT'),
    path("extract/",views.getDataset, name='upload'),

]

