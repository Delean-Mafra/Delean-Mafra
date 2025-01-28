import pytesseract as txm
from PIL import Image

print("Copyright ©2025 | Delean Mafra, todos os direitos reservados.\n")

# Define a função e converte a image em texto
def image_to_text(image_path):
    # le a imagem
    img = Image.open(image_path)
    
    text = txm.image_to_string(img, lang='por')
    return text

imagem = r'D:\Python\Python_projcts\templates\uploaded-image1.png'

# Call the function to convert the uploaded image to text
text = image_to_text(imagem)

# Print the extracted text
print(text)
