from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .grupo import Grupo
from .despesa import Despesa
from .pagamento import Pagamento
from .participacao_despesa import ParticipacaoDespesa
from .participante_grupo import ParticipanteGrupo
from .amizades import Amizade