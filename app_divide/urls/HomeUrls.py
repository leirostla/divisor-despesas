from django.urls import path
from app_divide.views.HomeView import consultas_view, home_view, sumario_view

urlpatterns = [
    path('', home_view, name='home'),
    path('sumario/', sumario_view, name='sumario'),
    path('consultas/', consultas_view)
]
