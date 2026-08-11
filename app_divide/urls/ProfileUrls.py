from django.urls import path
from app_divide.views.ProfileView import list_profile_view

urlpatterns = [
    path('', list_profile_view),
    path('<int:id>/', list_profile_view),
]