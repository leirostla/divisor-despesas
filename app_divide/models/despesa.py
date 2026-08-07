from app_divide.models import *
from django.conf import settings

class Despesa(models.Model):
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE, related_name='despesas')
    descricao = models.CharField(max_length=255)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)
    data_despesa = models.DateField(auto_now_add=True)
    criador = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='despesas_criadas')
    pagador = models.ForeignKey("ParticipanteGrupo", on_delete=models.CASCADE, related_name='despesas_pagas')
    

    def __str__(self):
        return '{} - {}'.format(self.descricao, self.valor_total)