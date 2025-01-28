print("Copyright ©2025 | Delean Mafra, todos os direitos reservados.")

# Função para calcular a potência
def calcular_potencia(base, potencia):
    return base ** potencia

# Entrada do usuário
base = float(input("Digite o número: "))

# Substitui a vírgula por ponto para aceitar valores decimais
potencia = input("Digite a potência: ").replace(",", ".")

# Converte a potência para float
potencia = float(potencia)

# Calculando o resultado
resultado = calcular_potencia(base, potencia)

# Exibindo o resultado
print(f"Resultado: {resultado}")
