from django.urls import path

from app_divide.views.AmizadesView import convidar_destinatario

urlpatterns = [
    path('convidar_destinatario/', convidar_destinatario, name='convidar_destinatario')
]