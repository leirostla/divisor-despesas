from decimal import Decimal, ROUND_HALF_UP


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
        "Bruno": Decimal("200.00"),
        "Carlos": Decimal("100.00"),
        "Thiago": Decimal("500.00"),
        "Lara": Decimal("50.00"),
        "Licia": Decimal("10.00")
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


if __name__ == "__main__":
    main()