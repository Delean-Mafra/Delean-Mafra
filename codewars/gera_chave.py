import random

def calcular_dv(key43):
    """
    Calculates the check digit (DV) for the first 43 digits of the access key.
    """
    weights = [5, 3, 2, 9, 8, 7, 6, 5]  # Repeating weights
    total = 0
    for i, digit in enumerate(key43):
        weight = weights[i % len(weights)]
        total += int(digit) * weight
    remainder = total % 11
    dv = 11 - remainder
    if dv >= 10:
        dv = 0
    return dv
print("Copyright ©2025 | Delean Mafra, todos os direitos reservados.")


def preencher_com_zeros(valor_c, total_digitos):
    return valor_c + '0' * (total_digitos - len(valor_c))

def gerar_chave():
    serie = str(random.randint(100, 999))
    cnpj = str(random.randint(10000000000000, 99999999999999))
    uf = str(random.randint(10, 99))
    aamm = str(random.randint(1000, 9999))
    mod = str(random.randint(10, 99))
    numero = str(random.randint(1000, 9999))
    fem = str(random.randint(10, 99))
    digitos36 = str(uf) + str(aamm) + str(cnpj) + str(mod) + str(serie) + str(numero) + str(fem)
    digitos43 = preencher_com_zeros(digitos36, 43)
    dv = calcular_dv(digitos43)
    chave_de_acesso = str(digitos43) + str(dv)
    return chave_de_acesso

# Gerar 20 chaves válidas
valid_keys = [gerar_chave() for _ in range(20)]

# Imprimir as chaves no formato desejado
print('valid_keys = [')
for key in valid_keys:
    print(f'    "{key}",')
print(']')
