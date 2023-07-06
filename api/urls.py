from django.urls import path, include
from . import views

urlpatterns = [
    path("result/<str:task_id>/", views.getMainTaskResponse, name="task-result"),
    path(
        "analysis/<str:task_id>/", views.getAnalysisTaskResponse, name="analysis-result"
    ),
    path(
        "keywords/<str:task_id>/", views.getKeywords, name="keywords-result"
    ),
    path(
        "file/<int:pid>/", views.getCsvColumns, name="csv-columns"
    ),
]
