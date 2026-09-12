from decimal import Decimal

valor = Decimal("100")
quantidade = 3

total_centavos = int(valor * 100)
cota_base, centavos_restantes = divmod(total_centavos, quantidade)

cotas_centavos = [
    cota_base + (1 if indice < centavos_restantes else 0)
    for indice in range(quantidade)
]

cotas = [Decimal(centavos) / 100 for centavos in cotas_centavos]
print(cotas)


# [Decimal('24.38'), Decimal('24.38'),
#  Decimal('24.37'), Decimal('24.37')]