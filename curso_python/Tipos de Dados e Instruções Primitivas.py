def verificar_tipo(dado):
    try:
        # Tenta converter o dado para um número float
        numero = float(dado)
        # Verifica se o número é inteiro ou real com base no formato original
        if '.' in dado:
            return f"{dado} é um número real."
        else:
            return f"{dado} é um número inteiro."
    except ValueError:
        # Se ocorrer um erro na conversão, então é um dado literal
        return f"{dado} é um dado literal (string)."

# Exemplos de uso
print(verificar_tipo("33"))       # Saída: 33 é um número inteiro.
print(verificar_tipo("33.1"))     # Saída: 33.1 é um número real.
print(verificar_tipo("Olá"))      # Saída: Olá é um dado literal (string).
print(verificar_tipo("123abc"))   # Saída: 123abc é um dado literal (string).
print(verificar_tipo("0.0"))      # Saída: 0.0 é um número real.
print(verificar_tipo("5.0"))      # Saída: 5.0 é um número real.
