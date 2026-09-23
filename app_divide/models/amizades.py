from django.db import models
from django.conf import settings

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import F, Q


class Amizade(models.Model):

    class Status(models.TextChoices):
        PENDENTE = "P", "Pendente"
        ACEITA = "A", "Aceita"
        RECUSADA = "R", "Recusada"

    solicitante = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="solicitacoes_enviadas",
    )

    destinatario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="solicitacoes_recebidas",
    )

    status = models.CharField(
        max_length=1,
        choices=Status.choices,
        default=Status.PENDENTE,
    )

    criado_em = models.DateTimeField(auto_now_add=True)

    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["solicitante", "destinatario"],
                name="solicitacao_amizade_unica",
            ),
            models.CheckConstraint(
                condition=~Q(solicitante=F("destinatario")),
                name="nao_permitir_convite_para_si_mesmo",
            ),
        ]

    def clean(self):
        if self.solicitante_id == self.destinatario_id:
            raise ValidationError(
                "Um usuário não pode enviar um convite para si mesmo."
            )

    def __str__(self):
        return (
            f"{self.solicitante.username} → "
            f"{self.destinatario.username} "
            f"({self.get_status_display()})"
        )
