from decimal import Decimal, ROUND_HALF_UP

from django.db.models import QuerySet, Sum

from app_divide.models.despesa import Despesa
from app_divide.models.grupo import Grupo
from app_divide.models.pagamento import Pagamento
from app_divide.models.participacao_despesa import ParticipacaoDespesa
from app_divide.models.participante_grupo import ParticipanteGrupo

from app_divide.service.calculo_cotas import CalcularDivisao


def calcular_divisao(pagamentos: dict[str, Decimal]):
    total = sum(pagamentos.values())
    quantidade = len(pagamentos)

    if quantidade == 0:
        return {
            "total": total,
            "valor_individual": Decimal("0.00"),
            "saldos": {},
            "transferencias": [],
        }

    valor_individual = (
        (total / Decimal(quantidade)).quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP,
        )
    )

    saldos = {
        pessoa: (valor_pago - valor_individual).quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP,
        )
        for pessoa, valor_pago in pagamentos.items()
    }

    credores = [
        [pessoa, saldo]
        for pessoa, saldo in saldos.items()
        if saldo > 0
    ]

    devedores = [
        [pessoa, -saldo]
        for pessoa, saldo in saldos.items()
        if saldo < 0
    ]

    credores.sort(key=lambda item: item[1], reverse=True)
    devedores.sort(key=lambda item: item[1], reverse=True)

    transferencias = []
    indice_credor = 0
    indice_devedor = 0

    while (
        indice_credor < len(credores)
        and indice_devedor < len(devedores)
    ):
        credor, valor_a_receber = credores[indice_credor]
        devedor, valor_a_pagar = devedores[indice_devedor]

        valor_transferencia = min(
            valor_a_receber,
            valor_a_pagar,
        )

        transferencias.append(
            {
                "de": devedor,
                "para": credor,
                "valor": valor_transferencia,
            }
        )

        credores[indice_credor][1] -= valor_transferencia
        devedores[indice_devedor][1] -= valor_transferencia

        if credores[indice_credor][1] == 0:
            indice_credor += 1

        if devedores[indice_devedor][1] == 0:
            indice_devedor += 1

    return {
        "total": total,
        "valor_individual": valor_individual,
        "saldos": saldos,
        "transferencias": transferencias,
    }


def main():
    pagamentos = {
        "Ana": Decimal("130.00"),
        "Bruno": Decimal("0.00"),
        "Carlos": Decimal("0.00"),
    }

    resultado = calcular_divisao(pagamentos)

    print(f"Total: R$ {resultado['total']}")
    print(f"Parte individual: R$ {resultado['valor_individual']}")

    print("\nSaldos:")
    for pessoa, saldo in resultado["saldos"].items():
        print(f"{pessoa}: R$ {saldo}")

    print("\nTransferências:")
    for transferencia in resultado["transferencias"]:
        print(
            f"{transferencia['de']} paga "
            f"R$ {transferencia['valor']} para "
            f"{transferencia['para']}"
        )


class Rateio:

    def __init__(self, grupo_selecionado: Grupo):
        self.grupo = grupo_selecionado
        self.pagamentos = {}
        self.resultado = {}

    def get_pagamentos(self):
        despesas = self.grupo.grupo_despesa.all()
        self.pagamentos = {}

        for despesa in despesas:
            valor_total = despesa.valor_total
            pagamentos_model = despesa.despesa_paga.all()

            for pagamento_model in pagamentos_model:
                participante_username = pagamento_model.pagador.usuario.username
                self.pagamentos[participante_username] = (self.pagamentos.get(participante_username, Decimal("0.00"))
                    + valor_total
                )

            participantes_despesa = ParticipacaoDespesa.objects.filter(
                despesa=despesa,
            ).select_related("participante", "participante__usuario")

            for participante_despesa in participantes_despesa:
                participante = participante_despesa.participante.usuario.username
                valor_devido = participante_despesa.valor_devido
                self.pagamentos[participante] = (
                    self.pagamentos.get(participante, Decimal("0.00"))
                    - valor_devido
                )

        self.resultado = calcular_divisao(self.pagamentos)
        print(f"Pagamentos: {self.pagamentos}")
        return self.pagamentos

    def get_total(self):
        return self.resultado.get("total")

    def get_valor_individual(self):
        return self.resultado.get("valor_individual")

    def get_saldos(self):
        return self.resultado.get("saldos")

    def get_transferencias(self):
        return self.resultado.get("transferencias")



        


if __name__ == "__main__":
    main()