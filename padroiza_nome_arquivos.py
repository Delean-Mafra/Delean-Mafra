import os

print("Copyright ©2025 | Delean Mafra, todos os direitos reservados.")

# Define o caminho da pasta
folder_path = r"\pasta"

# Percorre todos os arquivos na pasta
for filename in os.listdir(folder_path):
    # Cria o novo nome do arquivo em minúsculas
    new_filename = filename.lower()
    # Gera os caminhos completos para o arquivo original e o novo
    old_file = os.path.join(folder_path, filename)
    new_file = os.path.join(folder_path, new_filename)
    # Renomeia o arquivo
    os.rename(old_file, new_file)

print("Todos os arquivos foram renomeados para minúsculas.")
