from app_divide.models import *
from app_divide.models.despesa import Despesa

class ParticipacaoDespesa(models.Model):
    despesa = models.ForeignKey(Despesa, on_delete=models.CASCADE, related_name='despesa_a_pagar')
    participante = models.ForeignKey("ParticipanteGrupo", on_delete=models.CASCADE, related_name='participantes_despesa')
    
    valor_devido = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return '{} - {}'.format(self.despesa.descricao, self.participante.usuario.username)