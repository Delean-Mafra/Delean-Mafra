import os
import fitz  # PyMuPDF

def pdf_to_png(folder_path):
    # Verifica se o diretório fornecido existe
    if not os.path.exists(folder_path):
        print(f"O caminho {folder_path} não existe.")
        return

    # Cria uma pasta para armazenar as imagens PNG, se não existir
    output_folder = os.path.join(folder_path, "png_output")
    os.makedirs(output_folder, exist_ok=True)

    # Lista todos os arquivos na pasta
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".pdf"):
            pdf_path = os.path.join(folder_path, file_name)
            try:
                # Abre o PDF
                pdf_document = fitz.open(pdf_path)
                for page_number in range(len(pdf_document)):
                    # Renderiza a página como uma imagem
                    page = pdf_document[page_number]
                    pix = page.get_pixmap()
                    # Salva a imagem como PNG
                    output_file = os.path.join(output_folder, f"{file_name[:-4]}_page_{page_number + 1}.png")
                    pix.save(output_file)
                pdf_document.close()
                print(f"PDF {file_name} convertido com sucesso.")
            except Exception as e:
                print(f"Erro ao processar {file_name}: {e}")

if __name__ == "__main__":
    folder_path = r"D:\Python\Python_projcts\complementos\Certificados"
    pdf_to_png(folder_path)