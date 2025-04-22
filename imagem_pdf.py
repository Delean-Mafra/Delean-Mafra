from PIL import Image

# Abre o arquivo de imagem
img = Image.open(r'D:\Python\Python_projcts\templates\Sem título.png')

# Converte a imagem para o modo RGB
img = img.convert('RGB')

# Salva a imagem como PDF
img.save(r'C:\Users\Acer\Desktop\certificado.pdf')

print("A imagem foi convertida com sucesso para output.pdf")