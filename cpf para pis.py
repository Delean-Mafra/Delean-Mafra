print("Copyright ©2025 | Delean Mafra, todos os direitos reservados.")

def validador():
    cpf = str(input("Digite um CPF para ser validado ao lado: "))

    # Remove os caracteres de pontuação do CPF
    cpf = cpf.replace(".", "").replace("-", "")

    # Extrai apenas os dígitos do CPF, ignorando os caracteres especiais
    numeros = [int(digito) for digito in cpf if digito.isdigit()]

    quant_digitos = False
    validacao1 = False
    validacao2 = False

    if len(numeros) == 11:
        quant_digitos = True

        soma_produtos = sum(a*b for a, b in zip(numeros[0:9], range(10, 1, -1)))
        digito_esperado = (soma_produtos * 10 % 11) % 10
        if numeros[9] == digito_esperado:
            validacao1 = True

        soma_produtos1 = sum(a*b for a, b in zip(numeros[0:10], range(11, 1, -1)))
        digito_esperado1 = (soma_produtos1 * 10 % 11) % 10
        if numeros[10] == digito_esperado1:
            validacao2 = True

        if quant_digitos == True and validacao1 == True and validacao2 == True:
            print(f"O CPF {cpf} é válido.")
            return cpf
        else:
            print(f"O CPF {cpf} não é válido... Tente outro CPF...")
            return None
    else:
        print(f"O CPF {cpf} não é válido... Tente outro CPF...")
        return None

def calcula_digito_pis(cpf):
    cpf = [int(digito) for digito in str(cpf)]
    
    pesos = [3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    
    cpf = cpf[:-1]
    
    pesos = pesos[-len(cpf):]
    
    total = sum(cpf[i] * pesos[i] for i in range(len(cpf)))
    
    resto = total % 11
    
    digito_verificador = 11 - resto
    
    if digito_verificador in [10, 11]:
        digito_verificador = 0
    
    cpf.append(digito_verificador)
    
    cpf = ''.join(str(i) for i in cpf)
    
    cpf = cpf.zfill(11)
    
    return cpf

while True:
    cpf_usuario = validador()

    if cpf_usuario is not None:
        # Calculando o dígito verificador do PIS para o CPF fornecido
        resultado = calcula_digito_pis(cpf_usuario)

        print(resultado)
 