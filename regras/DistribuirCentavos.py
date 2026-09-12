from decimal import Decimal

valor = Decimal("97.59")
quantidade = 4

total_centavos = int(valor * 100)
cota_base, centavos_restantes = divmod(total_centavos, quantidade)

cotas_centavos = [
    cota_base + (1 if indice < centavos_restantes else 0)
    for indice in range(quantidade)
]

cotas = [Decimal(centavos) / 100 for centavos in cotas_centavos]
print(cotas)

print(f"Total: {sum(cotas)}")  # Verifica se a soma das cotas é igual ao valor original

print(f"Transferências: {(valor - cotas[0]) - sum(cotas[1:])}")  # Verifica se a diferença entre o valor original e a soma das cotas é zero