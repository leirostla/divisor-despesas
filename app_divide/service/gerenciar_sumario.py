from decimal import Decimal

from django.db.models.aggregates import Sum

from app_divide.models.despesa import Despesa
from app_divide.models.grupo import Grupo
from app_divide.models.pagamento import Pagamento
from app_divide.models.participacao_despesa import ParticipacaoDespesa
from app_divide.models.participante_grupo import ParticipanteGrupo
from app_divide.service.calculo_cotas import CalcularDivisao

from django.contrib.auth import get_user_model

from app_divide.service.services import distribuir_centavos

class GerenciarSumario:

    def __init__(self, grupo_selecionado: Grupo, 
                despesa: Despesa=None,            
                pagador: ParticipanteGrupo = None,
            ):

        self.grupo_selecionado = grupo_selecionado
        self.despesa = despesa
        self.pagador = pagador
                

    def distribuir_centavos(self, valor: Decimal, quantidade: int) -> list[Decimal]:
        return distribuir_centavos(valor,quantidade)


    def calcular_valores_individuais(self):
        dic_pagamentos = {}
        resp = {}
        total_valor_dividas = ParticipacaoDespesa.objects.filter(participante__grupo__id=self.grupo_selecionado.id).aggregate(total=Sum("valor_devido"))["total"]

        print(f"Total Valor da Dívida: {total_valor_dividas}")

        if total_valor_dividas:

            q_participantes_despesa = ParticipacaoDespesa.objects.filter(
                participante__grupo__id=self.grupo_selecionado.id)

            q_pagamentos = Pagamento.objects.filter(pagador__grupo__id=self.grupo_selecionado.id)

            for pagamento in q_pagamentos:
                user_name = pagamento.pagador.usuario.username
                dic_pagamentos[user_name] = dic_pagamentos.get(user_name, Decimal("0.00")) + pagamento.valor_pago

            for q_participante in q_participantes_despesa:

                username = q_participante.participante.usuario.username
                if username not in dic_pagamentos:
                    dic_pagamentos[username] = Decimal("0.00")

            

            calculadora = CalcularDivisao(dic_pagamentos, total_valor_dividas)

            resp = calculadora.calcular_saldos()

            print(resp)

        return resp
            
        


#   pagamentos = {
#           "Lícia": Decimal("77.50"),
#           "Remelento": Decimal("10.00"),
#           "Skywalker": Decimal("0.00"),
#           "jose": Decimal("0.00"),
#       }
