from django.db import models
from django.conf import settings



# Create your models here.

class Grupo(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    criado_por = models.ForeignKey(settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="grupos_criados",)
    criado_em = models.DateTimeField(auto_now_add=True)
    ativo = models.BooleanField(default=True)


class ParticipanteGrupo(models.Model):
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE, related_name='participantes')

    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,null=True,
                                blank=True,
                                related_name="participacoes_em_grupos")
    nome = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    ativo = models.BooleanField(default=True)
    data_entrada = models.DateTimeField(auto_now_add=True)

