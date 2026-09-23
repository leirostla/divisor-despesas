
dados = {"Zeca": 30, "Ana": 25, "Maria": 22}

curioso = sorted(dados.items())

# Cria um novo dicionário ordenado alfabeticamente pelas chaves
dados = dict(sorted(dados.items()))

print(dados)
print(curioso)
print(type(curioso[0]))
# Saída: {'Ana': 25, 'Maria': 22, 'Zeca': 30}



# [Decimal('24.38'), Decimal('24.38'),
#  Decimal('24.37'), Decimal('24.37')]