from django.contrib import admin

# Register your models here.
from .models import Despesa, ParticipacaoDespesa

admin.site.register(Despesa)
admin.site.register(ParticipacaoDespesa)
