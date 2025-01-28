from rembg import remove
from PIL import Image

input = Image.open("python.png")
output = remove(input)
output.save("uploaded-image1.png")
