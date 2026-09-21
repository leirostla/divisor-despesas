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

class CalcularDivisao:

    def __init__(self, pagamentos: dict[str, Decimal], divida: Decimal):

        self.pagamentos = pagamentos
        self.divida = divida
        self.valor_individual = self.divida / len(self.pagamentos) if self.pagamentos else Decimal("0.00")        
        self.cotas_quantidade = len(self.pagamentos)
        self.cotas = self.distribuir_centavos()
        self.cotas_individuais = {}


    def incluir_pagamentos(self, pagamentos: dict[str, Decimal]):
        for nome in pagamentos:
            self.cotas_individuais[nome] = pagamentos[nome] + self.cotas_individuais[nome]

            for c in self.cotas_individuais:
                if self.cotas_individuais[c] > 0:
                    self.cotas_individuais[c] -= pagamentos[nome]

        
    def calcular_cotas_individuais(self):
        confere = Decimal('0.00')

        for nome, cota in zip(self.pagamentos.keys(), self.cotas):            
            self.cotas_individuais[nome] = self.pagamentos[nome] - cota
            confere += self.cotas_individuais[nome]

        if confere != Decimal('0.00'):
            print(f"Erro: A soma das cotas individuais não é igual a zero. Soma: {confere}")
            self.cotas_individuais = {}




    def distribuir_centavos(self) -> list[Decimal]:
            total_centavos = int(self.divida * 100)
            cota_base, centavos_restantes = divmod(total_centavos, self.cotas_quantidade)

            cotas_centavos = [
                cota_base + (1 if indice < centavos_restantes else 0)
                for indice in range(self.cotas_quantidade)
            ]

            cotas = [Decimal(centavos) / 100 for centavos in cotas_centavos]
            return cotas





def main():

    pagamentos = {
        "Lícia": Decimal("77.50"),
        "Remelento": Decimal("10.00"),
        "Skywalker": Decimal("0.00"),
        "jose": Decimal("0.00"),
    }

    # resultado = calcular_divisao(pagamentos)

    # print(f"Total: R$ {resultado['total']}")
    # print(f"Parte individual: R$ {resultado['valor_individual']}")

    # print("\nSaldos:")
    # for pessoa, saldo in resultado["saldos"].items():
    #     print(f"{pessoa}: R$ {saldo}")

    # print("\nTransferências:")
    # for transferencia in resultado["transferencias"]:
    #     print(
    #         f"{transferencia['de']} paga "
    #         f"R$ {transferencia['valor']} para "
    #         f"{transferencia['para']}"
    #     )


    calcular_divisao = CalcularDivisao(pagamentos, Decimal("87.50"))
    calcular_divisao.calcular_cotas_individuais()
    
    print(f"Valor Individual: {calcular_divisao.valor_individual}")
    #print(f"Cotas: R$ {calcular_divisao.cotas}")
    print(f"Pagamentos: {calcular_divisao.pagamentos}")
    print(f"Cotas individuais: {calcular_divisao.cotas_individuais}")
    calcular_divisao.incluir_pagamentos({'Remelento': Decimal("11.88")})
    print(f"Cotas individuais: {calcular_divisao.cotas_individuais}")



if __name__ == "__main__":
    main()