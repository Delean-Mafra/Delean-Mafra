# Inicialização da matriz (3x2 com valores fornecidos pelo usuário)
matriz = []

# Loop para receber os valores do usuário
for i in range(3):  # 3 linhas
    linha = []
    for j in range(2):  # 2 colunas
        valor = int(input(f"Digite o valor para a linha {i+1} e coluna {j+1}: "))
        linha.append(valor)
    matriz.append(linha)

# Adicionando 2 a cada valor da matriz
for i in range(len(matriz)):  # Percorre as linhas
    for j in range(len(matriz[i])):  # Percorre as colunas
        matriz[i][j] += 2  # Soma 2 ao elemento atual

# Exibindo o resultado
print("Matriz atualizada:")
for linha in matriz:
    print(linha)















# Algoritmo "exemploMatriz"

# Var
# // Seção de Declarações das variáveis
# numeros: vetor [1..3,1..2] de inteiro
# i,j: inteiro

# Inicio
# // Seção de Comandos, procedimento, funções, operadores, etc...
# // Laço para percorrer as linhas
# PARA i DE 1 ATE 3 FACA
#     // Laço para percorrer as colunas
#     PARA j DE 1 ATE 2 FACA
#         ESCREVA("Digite o valor para a linha ", i, " e coluna ", j, ": ")
#         LEIA(numeros[i, j])
#     FIMPARA
# FIMPARA

# Fimalgoritmo
