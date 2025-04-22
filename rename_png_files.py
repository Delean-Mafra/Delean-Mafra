import os

def rename_png_files(folder_path):
    # Verifica se a pasta existe
    if not os.path.exists(folder_path):
        print(f"O diretório {folder_path} não existe.")
        return

    # Lista todos os arquivos na pasta e filtra apenas arquivos PNG
    png_files = [f for f in os.listdir(folder_path) if f.endswith('.png')]

    # Ordena os arquivos para renomear de forma consistente
    png_files.sort()

    # Renomeia os arquivos
    for i, file_name in enumerate(png_files, start=1):
        # Caminho completo do arquivo original
        old_file_path = os.path.join(folder_path, file_name)
        
        # Caminho completo do novo nome
        new_file_name = f"certificado_{i}.png"
        new_file_path = os.path.join(folder_path, new_file_name)
        
        # Renomeia o arquivo
        try:
            os.rename(old_file_path, new_file_path)
            print(f"Renomeado: {file_name} -> {new_file_name}")
        except Exception as e:
            print(f"Erro ao renomear {file_name}: {e}")

if __name__ == "__main__":
    # Substitua pelo caminho da pasta onde estão os arquivos PNG
    folder_path = r"D:\Python\Python_projcts\complementos\Certificados"
    rename_png_files(folder_path)