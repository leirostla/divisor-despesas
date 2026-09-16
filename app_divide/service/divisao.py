from decimal import Decimal, ROUND_HALF_UP

from django.db.models import QuerySet

from app_divide.models.despesa import Despesa
from app_divide.models.grupo import Grupo
from app_divide.models.participacao_despesa import ParticipacaoDespesa
from app_divide.models.participante_grupo import ParticipanteGrupo



def calcular_divisao(pagamentos: dict[str, Decimal]):
    total = sum(pagamentos.values())
    quantidade = len(pagamentos)

    valor_individual = (
        total / Decimal(quantidade)
    ).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

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


class Divisao:

    def __init__(self, grupo_selecionado: Grupo):
        self.grupo = grupo_selecionado

        despesas = self.grupo.grupo_despesa.all()

        self.pagamentos = {}
        for despesa in despesas:
            valor_total = despesa.valor_total
            pagador = despesa.despesa_paga.first().pagador.usuario.username if despesa.despesa_paga.exists() else 'Nulo'
            self.pagamentos[pagador] = self.pagamentos.get(pagador, Decimal("0.00")) + valor_total

        participantes_despesa = ParticipacaoDespesa.objects.filter(despesa__in=despesas).select_related('participante', 'participante__usuario')

        for participantes in participantes_despesa:
            participante = participantes.participante.usuario.username
            valor_devido = participantes.valor_devido
            self.pagamentos[participante] = self.pagamentos.get(participante, Decimal("0.00")) - valor_devido





    def get_pagamentos(self):
        return self.pagamentos
        

    def get_total(self):
        return self.resultado["total"]

    def get_valor_individual(self):
        return self.resultado["valor_individual"]

    def get_saldos(self):
        return self.resultado["saldos"]

    def get_transferencias(self):
        return self.resultado["transferencias"]


class CalcularPartesDespesa:

    def calcular_partes_despesa(self, despesa: Despesa, grupo_selecionado: Grupo, pagador: ParticipanteGrupo, pessoas: list):
        # Calcular o valor devido por cada participante
        valor_devido = despesa.valor_total / (len(pessoas) + 1)

        participantes_despesa = list(pessoas)
        participantes_despesa.append(pagador.usuario)

        # Distribuir centavos de forma equitativa
        cotas = self.distribuir_centavos(despesa.valor_total, len(participantes_despesa))

        # Criar ParticipacaoDespesa para cada participante
        for pessoa, cota in zip(participantes_despesa, cotas):

            participante_grupo = ParticipanteGrupo.objects.get(
                grupo=grupo_selecionado,
                usuario=pessoa,
                ativo=True,
            )

            ParticipacaoDespesa.objects.create(
                despesa=despesa,
                participante=participante_grupo,
                valor_devido=cota,
            )

            # Atualizar o valor pago pelo criador da despesa
            despesa.despesa_paga.create(
                pagador=pagador,
                valor_pago=despesa.valor_total,
            )            


    def distribuir_centavos(self, valor: Decimal, quantidade: int) -> list[Decimal]:
        total_centavos = int(valor * 100)
        cota_base, centavos_restantes = divmod(total_centavos, quantidade)

        cotas_centavos = [
            cota_base + (1 if indice < centavos_restantes else 0)
            for indice in range(quantidade)
        ]

        cotas = [Decimal(centavos) / 100 for centavos in cotas_centavos]
        return cotas


if __name__ == "__main__":
    main()