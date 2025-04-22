import pikepdf
import os

def desbloquear_pdf(input_pdf):
    # Abrir o arquivo PDF de entrada com a opção de permitir sobrescrever o arquivo
    with pikepdf.open(input_pdf, allow_overwriting_input=True) as pdf:
        # Salvar o PDF desbloqueado, sobrescrevendo o original
        pdf.save(input_pdf)

# Solicitar o caminho da pasta contendo os PDFs
pasta_pdf = r'D:\Python\complementos\pdf'

# Verificar se a pasta existe
if os.path.exists(pasta_pdf) and os.path.isdir(pasta_pdf):
    # Percorrer todos os arquivos na pasta
    for nome_arquivo in os.listdir(pasta_pdf):
        # Montar o caminho completo do arquivo
        caminho_arquivo = os.path.join(pasta_pdf, nome_arquivo)
        # Verificar se é um arquivo PDF
        if os.path.isfile(caminho_arquivo) and caminho_arquivo.lower().endswith('.pdf'):
            try:
                # Desbloquear o PDF
                desbloquear_pdf(caminho_arquivo)
                print(f'O arquivo {nome_arquivo} foi desbloqueado com sucesso!')
            except Exception as e:
                print(f'Erro ao desbloquear o arquivo {nome_arquivo}: {e}')
else:
    print(f'A pasta {pasta_pdf} não foi encontrada.')

print('Todos os PDFs foram processados!')