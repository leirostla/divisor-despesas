from django.contrib import admin

from app_divide.models.despesa import Despesa
from app_divide.models.grupo import Grupo
from app_divide.models.pagamento import Pagamento
from app_divide.models.participacao_despesa import ParticipacaoDespesa
from app_divide.models.participante_grupo import ParticipanteGrupo

# Register your models here.
admin.site.register(ParticipanteGrupo)
admin.site.register(Despesa)
admin.site.register(Grupo)
admin.site.register(Pagamento)
admin.site.register(ParticipacaoDespesa)

