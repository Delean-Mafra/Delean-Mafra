import random
import string

print("Copyright ©2025 | Delean Mafra, todos os direitos reservados.")

# Função para gerar um texto aleatório com base em um número de caracteres
def gerar_texto(tamanho):
    caracteres = string.ascii_lowercase + string.ascii_uppercase + string.punctuation + ' '
    texto = ''.join(random.choice(caracteres) for _ in range(tamanho))
    return texto

# Função para gerar um livro com várias páginas de textos aleatórios
def gerar_livro(paginas, tamanho_pagina):
    livro = []
    for _ in range(paginas):
        livro.append(gerar_texto(tamanho_pagina))
    return livro

# Função para buscar uma frase no livro
def buscar_frase(livro, frase):
    resultados = []
    for i, pagina in enumerate(livro):
        if frase.lower() in pagina.lower():
            resultados.append((i, pagina))
    return resultados

# Exemplo de uso do código
tamanho_pagina = 500  # Quantidade de caracteres por página
paginas = 100  # Quantidade de páginas no livro

# Gerar um "livro" com páginas aleatórias
livro = gerar_livro(paginas, tamanho_pagina)

# Buscar por uma frase
frase_busca = input("Digite a frase que você deseja buscar: ")
resultados = buscar_frase(livro, frase_busca)

# Exibir resultados da busca
if resultados:
    print(f"\nA frase '{frase_busca}' foi encontrada nas seguintes páginas:\n")
    for i, pagina in resultados:
        print(f"Página {i+1}:")
        print(pagina[:300])  # Exibir os primeiros 300 caracteres da página encontrada
        print("...\n")
else:
    print(f"\nA frase '{frase_busca}' não foi encontrada no livro.")
