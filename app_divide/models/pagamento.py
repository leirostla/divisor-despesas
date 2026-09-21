from app_divide.models import *

class Pagamento(models.Model):
    despesa = models.ForeignKey(Despesa, on_delete=models.CASCADE, related_name='despesa_paga', null=True, blank=True)
    pagador = models.ForeignKey("ParticipanteGrupo", on_delete=models.PROTECT, related_name='participante_grupo')
    valor_pago = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    data_pagamento = models.DateField(auto_now_add=True)