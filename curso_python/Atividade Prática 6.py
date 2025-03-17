"""
Algoritmo "ENQUANTO1ASSOMA"

Var
    i, soma, num: inteiro

Inicio
    i <- 1
    soma <- 0
    ENQUANTO i <= 5 FAÇA
        ESCREVAL ("Digite um número do tipo inteiro para a SOMA: ")
        LEIA (num)
        soma <- soma + num
        i <- i + 1
    FIMENQUANTO
    ESCREVAL ("Resultado da SOMA: ", soma)

Fimalgoritmo
"""
# Inicialização da variável
i = 1

# Estrutura de Repetição "Para" em Python
for i in range(1, 6):
    num = int(input("Digite um número do tipo inteiro para a MULTIPLICAÇÃO: "))
    i *= num

print("Resultado da MULTIPLICAÇÃO:", i)




"""
Algoritmo "MultiplicacaoRepitaAte"

Var
    i, num, produto: inteiro

Inicio
    i <- 1
    produto <- 1
    Repita
        ESCREVAL ("Digite um número do tipo inteiro para a MULTIPLICAÇÃO: ")
        LEIA (num)
        produto <- produto * num
        i <- i + 1
    Ate i > 5
    ESCREVAL ("Resultado da MULTIPLICAÇÃO: ", produto)

Fimalgoritmo


"""
# Inicialização das variáveis
i = 1
produto = 1

# Estrutura de Repetição "Repita Até" em Python
while True:
    num = int(input("Digite um número do tipo inteiro para a MULTIPLICAÇÃO: "))
    produto *= num
    i += 1
    if i > 5:
        break

print("Resultado da MULTIPLICAÇÃO:", produto)

