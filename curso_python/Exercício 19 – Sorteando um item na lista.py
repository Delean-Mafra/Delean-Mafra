import random

# Lista de nomes
nomes = ['João', 'Pedro', 'Tiago', 'Otavio']
print("Copyright ©2025 | Delean Mafra, todos os direitos reservados.")


# Sorteando um item da lista
sorteado = random.choice(nomes)
# Mostrando o resultado
print(f'O nome sorteado para apagar o quadro foi: {sorteado}')

# Sorteando vários itens da lista
sorteados = random.sample(nomes, 4)

# Mostrando a ordem de apresentação
print("Os alunos vão apresentar o trabalho na seguinte ordem:")
for i, nome in enumerate(sorteados, start=1):
    print(f'{i}° a apresentar: {nome}')



# Ler os nomes do arquivo com a codificação correta
with open('nomes.txt', 'r', encoding='utf-8') as file:
    nomes = file.readlines()

# Remover espaços em branco e quebras de linha
nomes = [nome.strip() for nome in nomes]



# Sortear vários nomes (por exemplo, 3 nomes)
sorteados = random.sample(nomes, 3)
print(f'Os nomes sorteados foram: {", ".join(sorteados)}')