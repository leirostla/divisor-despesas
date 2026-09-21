from decimal import Decimal


class CalcularDivisao:

    def __init__(self, pagamentos: dict[str, Decimal], divida: Decimal):

        self.pagamentos = pagamentos
        self.divida = divida
        self.valor_individual = self.divida / len(self.pagamentos) if self.pagamentos else Decimal("0.00")        
        self.cotas_quantidade = len(self.pagamentos)
        self.cotas_devedoras = self.distribuir_centavos() # valor que cada um deve
        self.cota_individual = {}




    def incluir_pagamentos(self, pagamentos: dict[str, Decimal]):
        for nome in pagamentos:
            self.cota_individual[nome] = pagamentos[nome] + self.cota_individual[nome]

            for c in self.cota_individual:
                if self.cota_individual[c] > 0:
                    self.cota_individual[c] -= pagamentos[nome]

    def calcular_saldos(self):

        credores = []
        devedores = []
        decimal_zero = Decimal("0.00")
        confere = Decimal('0.00')
        print(f"Pagamentos: {self.pagamentos}")
        print(f'Cotas individuais: {self.cota_individual}')
        print(f'Cotas Devedoras: {self.cotas_devedoras}')

        for nome, cota_devedora in zip(self.pagamentos.keys(), self.cotas_devedoras):
            self.cota_individual[nome] = self.pagamentos[nome] - cota_devedora
            confere += self.cota_individual[nome]

            if self.cota_individual[nome] > decimal_zero:
                credores.append(nome)
            elif self.cota_individual[nome] < decimal_zero:
                devedores.append(nome)

            

        print('   ')
        print(f"Confere: {confere}")

        if confere > decimal_zero:
            for nome in credores:
                if self.cota_individual[nome] >=  confere:
                    self.cota_individual[nome] -= confere
                    confere = 0

                elif self.cota_individual[nome] <  confere:
                    saldo = self.cota_individual[nome]
                    confere -= saldo
                    self.cota_individual[nome] = decimal_zero
                else:
                    print(f"Confere no laço: {confere}")

        elif confere < decimal_zero:            
            print(f"Erro: A soma das cotas individuais é menor que zero. Soma: {confere}")
            self.cota_individual = {}

        return self.cota_individual
        




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

    calcular_divisao = CalcularDivisao(pagamentos, Decimal("87.50"))
    calcular_divisao.calcular_cotas_individuais()
    
    print(f"Valor Individual: {calcular_divisao.valor_individual}")
    print(f"Pagamentos: {calcular_divisao.pagamentos}")
    print(f"Cotas individuais: {calcular_divisao.cota_individual}")
    calcular_divisao.incluir_pagamentos({'Remelento': Decimal("11.88")})
    print(f"Cotas individuais: {calcular_divisao.cota_individual}")

if __name__ == "__main__":
    main()