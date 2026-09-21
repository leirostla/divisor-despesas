from django.urls import path
from app_divide.views.HomeView import consultas_view, home_view, sumario_view, registrar_pagamento_view, registrar_despesa_view

urlpatterns = [
    path('', home_view, name='home'),
    path('sumario/', sumario_view, name='sumario'),
    path('consultas/', consultas_view),
    path('pagamentos/', registrar_pagamento_view, name='pagamentos'),
    path('registrar_despesa/', registrar_despesa_view, name='registrar_despesa'),
]
