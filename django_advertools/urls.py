"""
URL configuration for django_advertools project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View


def index(request):

    return render(request, "home.html")

def reset_cookie(request):
    response = redirect("home")
    # Delete the existing cookie
    print(request.COOKIES)
    if 'socket_id' in request.COOKIES:
        del request.COOKIES['socket_id']
        response.delete_cookie(key='socket_id')
    
    # Set a new cookie with desired parameters
    # response.set_cookie('cookie_name', 'new_value', max_age=3600)
    
    return response


def serveReport(request):
    return render(request, "reportMain.html")


def getReport(request):
    return render(request, "report.html")


urlpatterns = [
    path("", index, name="home"),
    path("report/get/", getReport, name="getReport"),
    path("report/", serveReport, name="report"),
    path("reset/cookie/",reset_cookie,name="reset-cookie"),
    path("select2/", include("django_select2.urls")),
    path("analyse/", include("analyse.urls")),
    path("seo/", include("seo.urls")),
    path("api/", include("api.urls")),
    path("generate/", include("generateAds.urls")),
    path("admin/", admin.site.urls),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
