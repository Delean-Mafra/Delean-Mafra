# Ordem de Precedência
print("Copyright ©2025 | Delean Mafra, todos os direitos reservados.")


# () - Parênteses
# ** - Exponenciação
# * - Multiplicação
# + e - - Adição e Subtração

nome = input('Qual seu nome? ')
print(f'Prazer em te conhecer {nome:=^20}')

a = input('Quanto é 5+2? R: ')

if a == '7':
    a = 7
if a == 'Sete':    
    a = 7
if a == 'sete':
    a = 7 
if a == 'SETE':
    a = 7         
print(f'a resposta é {5+2 == a}')


# Primeira expressão
resultado_um = int(input('1° valor a somar: ')) + int(input('2° valor a somar: ')) * int(input('Valor a multiplicar: '))      

# Segunda expressão
resultado_dois = 3 * 5 + 4 ** 2

# Terceira expressão
resultado_tres = 3 * (5 + 4) ** 2

print(resultado_um)   # Saída: 11
print(resultado_dois) # Saída: 31
print(resultado_tres) # Saída: 243



# Adição
resultado_adicao = 5 + 2

# Exponenciação
resultado_exponenciacao = 5 ** 2

# Subtração
resultado_subtracao = 5 - 2

# Divisão (ponto flutuante)
resultado_divisao = 5 / 2

# Multiplicação
resultado_multiplicacao = 5 * 2

# Divisão inteira
resultado_divisao_inteira = 5 // 2

# Módulo (Resto da divisão)
resultado_modulo = 5 % 2

# Divisão ponto flutuante (com uma casa decimal)
resultado_divisao_ponto_fluante = round(5 / 2, 1)

print(resultado_adicao)              # Saída: 7
print(resultado_exponenciacao)       # Saída: 25
print(resultado_subtracao)           # Saída: 3
print(resultado_divisao)             # Saída: 2.5
print(resultado_multiplicacao)       # Saída: 10
print(resultado_divisao_inteira)     # Saída: 2
print(resultado_modulo)              # Saída: 1
print(resultado_divisao_ponto_fluante) # Saída: 2.5



n1 = int(input('Digite um valor: '))
n2 = int(input('Digite outro valor: '))

print(f'A soma é {n1 + n2}, o produto é {n1 * n2} e a divisão é {n1 / n2:.3f}', end=' ')
print(f'Divisão inteira {n1 // n2} e potência {n1 ** n2}')