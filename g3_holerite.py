import pyperclip

while True:
    valor = input('Digite o valor: ').replace('.','')
    pyperclip.copy(valor)
    print(valor)

    while True:
        resposta = input("Deseja fazer outro ajuste? (S/N) ").upper()
        if resposta in ["SIM", "S", "YES", "Y"]:
            break
        elif resposta in ["NÃO", "N", "NO", "N"]:
            print("Obrigado por usar o programa. Até mais!")
            exit(0)
        else:
            print("Resposta inválida. Por favor, responda com 'S' ou 'N'.")
