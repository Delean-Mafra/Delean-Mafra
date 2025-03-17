import os
from PyPDF2 import PdfReader, PdfWriter
print("Copyright ©2025 | Delean Mafra, todos os direitos reservados.")

def combinar_pdfs(pasta):
    escritor = PdfWriter()
    for arquivo in os.listdir(pasta):
        if arquivo.endswith('.pdf'):
            caminho_arquivo = os.path.join(pasta, arquivo)
            leitor = PdfReader(caminho_arquivo)
            for pagina in range(len(leitor.pages)):
                escritor.add_page(leitor.pages[pagina])

    
    with open('pdf_combinado.pdf', 'wb') as saida:
        escritor.write(saida)

# Caminho da pasta onde estão os PDFs
combinar_pdfs(r'D:\\Descomplica\\Matematica\\respostas em pdf')
