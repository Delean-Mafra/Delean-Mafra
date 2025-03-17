# Definindo as variáveis
n_livros = 1000
pg_por_livro = 150
palavras_por_pagina = 200
carct_por_palavra = 7
print("Copyright ©2025 | Delean Mafra, todos os direitos reservados.")


# Calculando o número total de carct em um livro
carct_por_livro = pg_por_livro * palavras_por_pagina * carct_por_palavra

# Calculando o número total de carct para todos os livros
total_carct = carct_por_livro * n_livros

# Convertendo o total de carct em b (1 caractere = 1 Byte)
total_b = total_carct

# Convertendo b em mb
total_mb = total_b / (1024 * 1024)

# Exibindo o resultado
print(f"precisará de aproximadamente {total_mb:.2f} MegaBytes de memória para armazenar todo o acervo digitalizado.")
