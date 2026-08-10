from app_divide.models import *
from django.conf import settings

class ParticipanteGrupo(models.Model):
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE, related_name='participantes')
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='participacoes')
    nome = models.CharField(max_length=100, blank=True, null=True)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return '{} - {}'.format(self.grupo.nome, self.usuario.username)