
print("Copyright ©2025 | Delean Mafra, todos os direitos reservados.")

def preencher_com_zeros(valor_c, total_digitos):
    return valor_c + '0' * (total_digitos - len(valor_c))

def calcular_dv(chave):
    multiplicadores = [2, 3, 4, 5, 6, 7, 8, 9] * 6  
    soma = 0
    for i in range(43):
        soma += int(chave[i]) * multiplicadores[i]
    resto = soma % 11
    if resto < 2:
        return 0
    else:
        return 11 - resto

uf = 42
aamm = 2410
cnpj = 82956160005051
modelo = 65
serie = 1
numero = 323752
fem = 10

digitos36 = str(uf) + str(aamm) + str(cnpj) + str(modelo) + str(serie) + str(numero) + str(fem)
digitos43 = preencher_com_zeros(digitos36, 43)


dv = calcular_dv(digitos43)

digitos44 = str(digitos43) + str (dv)

print(digitos44)
