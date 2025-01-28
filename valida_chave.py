print("Copyright ©2025 | Delean Mafra, todos os direitos reservados.")


def calcular_dv(chave43):
    """
    Calcula o dígito verificador (DV) para os 43 primeiros dígitos da chave de acesso.
    """
    pesos = [4, 3, 2, 9, 8, 7, 6, 5]  # Pesos que se repetem
    soma = 0
    for i, digito in enumerate(chave43):
        peso = pesos[i % len(pesos)]
        soma += int(digito) * peso
    resto = soma % 11
    dv = 11 - resto
    if dv >= 10:
        dv = 0
    return dv

def validar_chave_acesso(chave):
    """
    Valida a chave de acesso da NF-e.
    """
    if len(chave) != 44 or not chave.isdigit():
        return False
    chave43 = chave[:43]
    dv_informado = int(chave[43])
    dv_calculado = calcular_dv(chave43)
    return dv_informado == dv_calculado

# Exemplo de uso
chave = input("Digite a chave de acesso (44 dígitos): ")
if validar_chave_acesso(chave):
    print("Chave de acesso válida.")
else:
    print("Chave de acesso inválida.")
