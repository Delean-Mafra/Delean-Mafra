def dobrar_valor(valor, vezes):
    acumulado = valor
    for _ in range(vezes - 1):
        valor *= 2
        acumulado += valor
    return valor, acumulado

# Solicita ao usuário para digitar o valor e quantas vezes deseja dobrar
valor_inicial = float(input("Digite um valor: "))
vezes = int(input("Digite quantas vezes você quer dobrar esse valor: "))

# Calcula o resultado e o valor acumulado
resultado, acumulado = dobrar_valor(valor_inicial, vezes)

# Exibe o resultado e o valor acumulado
print(f"Resultado: {resultado}")
print(f"Valor acumulado: {acumulado}")
