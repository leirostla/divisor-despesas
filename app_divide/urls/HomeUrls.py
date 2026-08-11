from django.urls import path
from app_divide.views.HomeView import home_view

urlpatterns = [
    path('', home_view, name='home'),
]