from app_divide.models import *
from django.conf import settings

class Grupo(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return '{}'.format(self.nome)


