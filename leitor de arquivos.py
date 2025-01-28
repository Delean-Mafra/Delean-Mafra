
print("Copyright ©2025 | Delean Mafra, todos os direitos reservados.")

def contar_caracteres(nome_arquivo):
    with open(nome_arquivo, 'r') as arquivo:
        conteudo = arquivo.read()
    return len(conteudo)

# Exemplo de uso:
print("Total de caracteres: " + str(contar_caracteres('contar_caracters.txt')))


def contar_caracteres_visiveis(nome_arquivo):
    with open(nome_arquivo, 'r') as arquivo:
        conteudo = arquivo.read()
    conteudo_sem_espacos = conteudo.replace(' ', '')  # remove espaços em branco
    conteudo_sem_novas_linhas = conteudo_sem_espacos.replace('\n', '')  # remove caracteres de nova linha
    return len(conteudo_sem_novas_linhas)

# Exemplo de uso:
print("Total de caracteres sem espaços em branco e sem nova linha: " + str(contar_caracteres_visiveis('contar_caracters.txt')))