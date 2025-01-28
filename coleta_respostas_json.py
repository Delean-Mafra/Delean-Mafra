import json
import re

print("Copyright ©2025 | Delean Mafra, todos os direitos reservados.")

# Função para limpar caracteres de controle
def limpar_caracteres(texto):
    return re.sub(r'[\x00-\x1F\x7F]', '', texto)

# Função para ler e imprimir as respostas do JSON
def imprimir_respostas(json_file):
    with open(json_file, 'r', encoding='utf-8') as file:
        conteudo = file.read()
        conteudo_limpo = limpar_caracteres(conteudo)
        try:
            dados = json.loads(conteudo_limpo)
            respostas = [f'    """{item["R"].replace("\n", " ")}"""' for item in dados if 'R' in item]
            print("respostas = [\n" + ",\n".join(respostas) + "\n]")
        except json.JSONDecodeError as e:
            print(f"Erro ao decodificar JSON: {e}")

# Nome do arquivo JSON
arquivo_json = r'\Novo Documento de Texto.json'

# Chama a função para imprimir as respostas
imprimir_respostas(arquivo_json)
