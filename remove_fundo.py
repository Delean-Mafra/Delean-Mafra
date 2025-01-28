from rembg import remove
from PIL import Image
print("Copyright ©2025 | Delean Mafra, todos os direitos reservados.")

input = Image.open("python.png")
output = remove(input)
output.save("uploaded-image1.png")
