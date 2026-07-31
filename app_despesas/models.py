from django.db import models
from django.conf import settings

from app_grupos.models import Grupo, ParticipanteGrupo

# Create your models here.
class Despesa(models.Model):
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE, related_name="despesas")
    descricao = models.CharField(max_length=200)
    valor_total = models.DecimalField(max_digits=12, decimal_places=2)
    data_despesa = models.DateField()
    categoria = models.CharField(max_length=100, blank=True)
    observacao = models.TextField(blank=True)
    pagador = models.ForeignKey(
        ParticipanteGrupo,
        on_delete=models.PROTECT,
        related_name="despesas_pagas",
    )
    criado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="despesas_criadas",
    )
    criado_em = models.DateTimeField(auto_now_add=True)


class ParticipacaoDespesa(models.Model):
    despesa = models.ForeignKey(
        Despesa,
        on_delete=models.CASCADE,
        related_name="participacoes",
    )
    participante = models.ForeignKey(
        ParticipanteGrupo,
        on_delete=models.PROTECT,
        related_name="despesas_participadas",
    )
    valor_devido = models.DecimalField(max_digits=12, decimal_places=2)
