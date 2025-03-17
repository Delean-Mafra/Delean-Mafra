print("Opções:")
print(" 1 - Calcular o dobro do número")
print(" 2 - Calcular o triplo do número")
op = input("Escolha uma opção: ")


if op == "1":
    num = float(input("Digite um número: "))
    print("O dobro do número é", num * 2)
elif op == "2":
    num = float(input("Digite um número: "))
    print("O triplo do número é", num * 3)
else:
    print("Opção inválida")
