from django.urls import path,include
from . import views

urlpatterns = [
    path("result/<str:task_id>/",views.getTaskResponse, name='task-result'),
]