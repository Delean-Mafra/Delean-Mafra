from PIL import Image
from rembg import remove
from PIL import Image

print("Copyright ©2025 | Delean Mafra, todos os direitos reservados.")

input = Image.open("imagem.png")
output = remove(input)
output.save("imagem.png")


# Abra a imagem original e o novo fundo
imagem_original = Image.open("imagem.png")
novo_fundo = Image.open("imagem_fundo.png")

# Redimensione o novo fundo para corresponder ao tamanho da imagem original
novo_fundo = novo_fundo.resize(imagem_original.size)

# Cole a imagem original no novo fundo
novo_fundo.paste(imagem_original, (0, 0), imagem_original)

# Salve a imagem final
novo_fundo.save("imagem_final.png")
print('imagem gerada com sucesso!')
