from django.contrib import admin

# Register your models here.
from .models import Grupo, ParticipanteGrupo

admin.site.register(Grupo)
admin.site.register(ParticipanteGrupo)