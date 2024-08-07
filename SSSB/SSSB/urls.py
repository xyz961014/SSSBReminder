"""SSSB URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path, re_path, include
from rest_framework.routers import DefaultRouter
#from .views import MyModelViewSet

router = DefaultRouter()
#router.register(r'mymodel', MyModelViewSet)

from . import views

urlpatterns = [
    path('', views.index),
    path('available_apartments', views.available_apartments),
    path('apartment_status', views.apartment_status),
    path('search_apartments', views.search_apartments),
    path('new_filter', views.new_filter),
    path('filter', views.filter_info),
    path('unsubscribe', views.unsubscribe_filter),
    # RESTful API
    path('', include('web.urls')),
]
