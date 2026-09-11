from decimal import Decimal, ROUND_HALF_UP

from app_divide.models.grupo import Grupo


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
        "Ana": Decimal("500.00"),
        "Bruno": Decimal("0.00"),
        "Carlos": Decimal("0.00"),
        "Thiago": Decimal("0.00"),
        "Lara": Decimal("0.00"),
        "Licia": Decimal("0.00")
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

    # def __init__(self, pagamentos: dict[str, Decimal]):
    #     self.pagamentos = pagamentos
    #     self.resultado = calcular_divisao(pagamentos)

    def __init__(self, grupo_selecionado: Grupo):
        self.grupo = grupo_selecionado
        self.participantes_grupo = self.grupo.participantes.filter(ativo=True)
        self.despesas_grupo = self.grupo.despesas.all()
        self.pagamentos = self._obter_pagamentos()
        self.resultado = calcular_divisao(self.pagamentos)

    def get_total(self):
        return self.resultado["total"]

    def get_valor_individual(self):
        return self.resultado["valor_individual"]

    def get_saldos(self):
        return self.resultado["saldos"]

    def get_transferencias(self):
        return self.resultado["transferencias"]


if __name__ == "__main__":
    main()