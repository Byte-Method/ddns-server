from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    path('update/<str:ip>', csrf_exempt(views.index)),
    path('traefik-forwardedauth-acmeproxy', csrf_exempt(views.list_clients))
]