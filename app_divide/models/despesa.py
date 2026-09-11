#from app_divide.models import *
from django.db import models
from .grupo import Grupo
from .participante_grupo import ParticipanteGrupo
from django.conf import settings

class Despesa(models.Model):
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE, related_name='despesas')
    descricao = models.CharField(max_length=255)
    observacao = models.TextField(blank=True, null=True)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)
    data_despesa = models.DateField(auto_now_add=True)
    criador = models.ForeignKey(ParticipanteGrupo, on_delete=models.CASCADE, related_name='criador_despesas')
    
    

    def __str__(self):
        return '{} - {}'.format(self.descricao, self.valor_total)