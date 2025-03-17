def idade():
    while True:
        try:
            idade = input("Digite a sua idade: ")
            idade_int = int(idade)
            if idade_int > 17 and idade_int < 60:
                print(idade, "anos é adulto")
            elif idade_int >= 60:
                print(idade, "anos é idoso")
            elif idade_int < 18:
                print(idade, "anos é menor de idade")
            else:
                print("Idade inválida")
            break  # Sai do loop se uma idade válida foi digitada
        except ValueError:
            print("Por favor, digite um número válido.")

# Chama a função idade
idade()
