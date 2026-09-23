# Modelo de amizades no Django

Este material descreve uma implementação de amizade entre usuários com solicitação, aceite ou recusa. Um único registro representa toda a relação entre duas pessoas.

## Modelo completo

```python
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
```

## Significado dos campos

- `solicitante`: usuário que enviou o convite. Seus convites podem ser consultados com `usuario.solicitacoes_enviadas.all()`.
- `destinatario`: usuário que recebeu o convite. Seus convites recebidos podem ser consultados com `usuario.solicitacoes_recebidas.all()`.
- `status`: armazena `"P"`, `"A"` ou `"R"`, correspondendo a pendente, aceita ou recusada.
- `criado_em`: data e hora da criação.
- `atualizado_em`: data e hora da última alteração.

Prefira as constantes do modelo:

```python
Amizade.Status.PENDENTE
Amizade.Status.ACEITA
Amizade.Status.RECUSADA
```

Para obter o texto amigável do status:

```python
solicitacao.get_status_display()
```

## Fluxo

Um único registro representa o relacionamento:

```text
solicitante | destinatario | status
José        | Maria        | A
```

José envia o convite, o registro começa como pendente e Maria pode aceitá-lo ou recusá-lo. Quando aceito, a única linha passa a representar uma amizade bilateral; não é necessário criar outra linha no sentido contrário.

## Enviar convite

```python
from django.core.exceptions import ValidationError
from django.db.models import Q


def enviar_convite(solicitante, destinatario):
    if solicitante == destinatario:
        raise ValidationError(
            "Você não pode enviar um convite para si mesmo."
        )

    relacionamento_existente = Amizade.objects.filter(
        Q(solicitante=solicitante, destinatario=destinatario)
        | Q(solicitante=destinatario, destinatario=solicitante)
    ).first()

    if relacionamento_existente:
        raise ValidationError(
            "Já existe uma solicitação ou amizade entre esses usuários."
        )

    return Amizade.objects.create(
        solicitante=solicitante,
        destinatario=destinatario,
    )
```

A consulta considera as duas direções e impede que coexistam `José → Maria` e `Maria → José`. A `UniqueConstraint` do modelo, sozinha, impede apenas duplicidade na mesma direção.

## Aceitar convite

```python
from django.core.exceptions import PermissionDenied, ValidationError


def aceitar_convite(solicitacao, usuario):
    if solicitacao.destinatario != usuario:
        raise PermissionDenied(
            "Somente o destinatário pode aceitar este convite."
        )

    if solicitacao.status != Amizade.Status.PENDENTE:
        raise ValidationError("Esta solicitação não está pendente.")

    solicitacao.status = Amizade.Status.ACEITA
    solicitacao.save(update_fields=["status", "atualizado_em"])
    return solicitacao
```

## Recusar convite

```python
def recusar_convite(solicitacao, usuario):
    if solicitacao.destinatario != usuario:
        raise PermissionDenied(
            "Somente o destinatário pode recusar este convite."
        )

    if solicitacao.status != Amizade.Status.PENDENTE:
        raise ValidationError("Esta solicitação não está pendente.")

    solicitacao.status = Amizade.Status.RECUSADA
    solicitacao.save(update_fields=["status", "atualizado_em"])
    return solicitacao
```

## Consultar convites recebidos

```python
convites_recebidos = (
    request.user
    .solicitacoes_recebidas
    .filter(status=Amizade.Status.PENDENTE)
    .select_related("solicitante")
    .order_by("-criado_em")
)
```

## Consultar convites enviados

```python
convites_enviados = (
    request.user
    .solicitacoes_enviadas
    .filter(status=Amizade.Status.PENDENTE)
    .select_related("destinatario")
    .order_by("-criado_em")
)
```

## Consultar todos os amigos

Como o usuário pode aparecer em qualquer um dos lados, a consulta considera tanto solicitações enviadas quanto recebidas:

```python
from django.contrib.auth import get_user_model
from django.db.models import Q


User = get_user_model()

amigos = (
    User.objects
    .filter(
        Q(
            solicitacoes_recebidas__solicitante=request.user,
            solicitacoes_recebidas__status=Amizade.Status.ACEITA,
        )
        | Q(
            solicitacoes_enviadas__destinatario=request.user,
            solicitacoes_enviadas__status=Amizade.Status.ACEITA,
        )
    )
    .distinct()
    .order_by("first_name", "username")
)
```

## Remover amizade

Qualquer uma das duas pessoas pode localizar e excluir a relação aceita:

```python
amizade = Amizade.objects.filter(
    Q(solicitante=request.user, destinatario=outro_usuario)
    | Q(solicitante=outro_usuario, destinatario=request.user),
    status=Amizade.Status.ACEITA,
).first()

if amizade:
    amizade.delete()
```

## Restrições importantes

- `UniqueConstraint` impede duas solicitações iguais na mesma direção.
- `CheckConstraint` impede que o solicitante envie convite a si próprio no banco de dados.
- `clean()` fornece a mesma validação no nível da aplicação, com mensagem mais clara.
- As funções de serviço verificam quem tem permissão para aceitar ou recusar.
- A verificação nas duas direções deve ser mantida ao criar o convite.

Após criar o modelo, gere e aplique a migração:

```powershell
python manage.py makemigrations
python manage.py migrate
```
