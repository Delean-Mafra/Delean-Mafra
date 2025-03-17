# Desafio 6
print("Copyright ©2025 | Delean Mafra, todos os direitos reservados.")


a = int(input('Digite um número inteiro: '))

raiz_quadrada = a ** 0.5

# Verifica se a raiz quadrada é um número inteiro
if raiz_quadrada.is_integer():
    raiz_quadrada = int(raiz_quadrada)


print(f'O dobro de {a} é {a * 2}, o triplo de {a} é {a * 3} e a raiz quadrada de {a} é {raiz_quadrada}\n')
