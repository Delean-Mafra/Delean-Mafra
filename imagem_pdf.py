from PIL import Image

print("Copyright ©2025 | Delean Mafra, todos os direitos reservados.")

# Abre o arquivo de imagem
img = Image.open(r'\Sem título.png')

# Converte a imagem para o modo RGB
img = img.convert('RGB')

# Salva a imagem como PDF
img.save(r'arquivo.pdf')

print("A imagem foi convertida com sucesso para output.pdf")
