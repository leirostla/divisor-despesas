from app_divide.models import *
from django.conf import settings

class Grupo(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    membros = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='grupos')
    criador = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='criado_por')

    def __str__(self):
        return '{}'.format(self.nome)


