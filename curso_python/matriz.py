# Inicializando as variáveis
notas = []  # Lista para armazenar as notas
soma = 0
ndn = int(input('Informe quantas notas serão calculadas: '))

# Leitura das notas dos alunos
for i in range(ndn):
    nota = float(input(f"Digite a nota do aluno {i + 1}: "))
    notas.append(nota)
    soma += nota

# Cálculo da média
media = soma / ndn

# Exibição do resultado
print(f"A média da turma é: {media:.2f}")
