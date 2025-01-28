import os
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch

print("Copyright ©2025 | Delean Mafra, todos os direitos reservados.")


def criar_pdf_com_imagens(pasta_origem, arquivo_pdf):
    # Lista para armazenar os caminhos das imagens
    imagens = []
    
    # Extensões de arquivo de imagem suportadas
    extensoes_suportadas = ('.png', '.jpg', '.jpeg', '.gif', '.bmp')
    
    # Encontrar todas as imagens na pasta
    for arquivo in os.listdir(pasta_origem):
        if arquivo.lower().endswith(extensoes_suportadas):
            caminho_completo = os.path.join(pasta_origem, arquivo)
            imagens.append(caminho_completo)
    
    if not imagens:
        print("Nenhuma imagem encontrada na pasta!")
        return
    
    # Criar um novo PDF
    c = canvas.Canvas(arquivo_pdf, pagesize=letter)
    largura_pagina, altura_pagina = letter
    
    # Margem superior inicial
    y_posicao = altura_pagina - inch
    
    # Adicionar cada imagem ao PDF
    for caminho_imagem in imagens:
        try:
            # Abrir a imagem com PIL
            img = Image.open(caminho_imagem)
            largura_img, altura_img = img.size
            
            # Calcular a escala para ajustar a imagem à largura da página
            escala = min((largura_pagina - 2*inch) / largura_img, 4*inch / altura_img)
            largura_final = largura_img * escala
            altura_final = altura_img * escala
            
            # Se não houver espaço suficiente na página atual, criar uma nova página
            if y_posicao - altura_final < inch:
                c.showPage()
                y_posicao = altura_pagina - inch
            
            # Desenhar a imagem no PDF
            x_posicao = (largura_pagina - largura_final) / 2  # Centralizar horizontalmente
            c.drawImage(caminho_imagem, x_posicao, y_posicao - altura_final, 
                       width=largura_final, height=altura_final)
            
            # Atualizar a posição Y para a próxima imagem
            y_posicao -= (altura_final + 0.5*inch)  # Adiciona um pequeno espaço entre as imagens
            
        except Exception as e:
            print(f"Erro ao processar a imagem {caminho_imagem}: {str(e)}")
    
    # Salvar o PDF
    c.save()
    print(f"PDF criado com sucesso: {arquivo_pdf}")

# Caminho da pasta com as imagens
pasta_imagens = 'caminho'
# Caminho do arquivo PDF de saída
arquivo_pdf_saida = os.path.join(pasta_imagens, "imagens_combinadas.pdf")

# Executar a função
criar_pdf_com_imagens(pasta_imagens, arquivo_pdf_saida)
