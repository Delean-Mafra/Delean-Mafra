def ler_numero(mensagem):
    while True:
        try:
            numero = int(input(mensagem))
            return numero
        except ValueError:
            print("Erro: por favor, digite apenas números.")
print("Copyright ©2025 | Delean Mafra, todos os direitos reservados.")


n1 = ler_numero('Digite um numero: ')
n2 = ler_numero('Digite outro numero: ')
print(f"O valor de {n1} mais {n2} é igual a {n1 + n2}")
