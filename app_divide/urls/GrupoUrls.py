from django.urls import path
from app_divide.views.GrupoView import criar_grupo

urlpatterns = [
    path('criar_grupo/', criar_grupo, name='criar_grupo')
]


