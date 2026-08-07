from app_divide.models import *

class Pagamento(models.Model):
    despesa_paga = models.ForeignKey(Despesa, on_delete=models.SET_NULL, null=True, blank=True, related_name='despesa_paga')
    participante_grupo = models.ForeignKey("ParticipanteGrupo", on_delete=models.SET_NULL, null=True, blank=True, related_name='participante_grupo')
    valor_pago = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)