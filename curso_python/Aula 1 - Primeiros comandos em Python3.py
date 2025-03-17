
# nome = input("Qual o seu nome?: ")
# idade = input("Qual a sua idade: ")
# peso = input("Quanto você pesa: ")
print("Copyright ©2025 | Delean Mafra, todos os direitos reservados.")


# print(f"Meu nome é {nome}",f"Tenho {idade} anos",f"e peso {peso} kg")


# nome = input("Qual o seu nome?: ")

# print(f"Olá {nome}! prazer em te conhecer!")

# dia = input("Que dia você nasceu? \nDia:")
# mes = input("E o mes? \nMês:")
# ano = input("E o ano? \nAno:")

# print(f"Então você nasceu no dia {dia} de {mes} de {ano}, correto?")

while True:
    try:
        n1 = int(input("Vamos somar alguns números.\nPor favor, informe o primeiro número: "))
        break  
    except ValueError:
        print("O valor informado não é um número. Por favor, tente novamente.")


while True:
    try:
        n2 = int(input("Segundo número: "))
        break  
    except ValueError:
        print("O valor informado não é um número. Por favor, tente novamente.")
        
        
soma = n1+n2
print(f"A soma entre {n1} e {n2} vale {soma}")