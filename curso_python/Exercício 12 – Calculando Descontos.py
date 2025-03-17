# Desafio 12
b = float(input(f'Digite o percentual de desconto(Apenas números): '))
a = float(input(f'Digite o valor do produto que receberá {b}% de desconto: '))
b = b / 100
print("Copyright ©2025 | Delean Mafra, todos os direitos reservados.")


print(f'O valor do desconto de {b*100}% é de R${b*a:.2f}')
print(f'Seu produto com desconto de {b*100}% ficou no valor de R${a-b*a:.2f}\n')