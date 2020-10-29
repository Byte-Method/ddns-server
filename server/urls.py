from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    path('<str:ip>', csrf_exempt(views.index)),
]