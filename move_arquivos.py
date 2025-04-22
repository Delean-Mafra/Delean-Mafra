import os
import shutil

downloads_folder = r"C:/Users/YourUsername/Downloads"

# Defina categorias de tipos de arquivos
file_categories = {
    "Images": [".jpg", ".jpeg", ".png", ".gif"],
    "Documents": [".pdf", ".docx", ".txt"],
    "Videos": [".mp4", ".mkv", ".avi"],
    "Music": [".mp3", ".wav"]
}

for category in file_categories:
    category_path = os.path.join(downloads_folder, category)
    if not os.path.exists(category_path):
        os.makedirs(category_path)

for filename in os.listdir(downloads_folder):
    file_path = os.path.join(downloads_folder, filename)
    if os.path.isfile(file_path):
        moved = False
        for category, extensions in file_categories.items():
            if any(filename.lower().endswith(ext) for ext in extensions):
                shutil.move(file_path, os.path.join(downloads_folder, category, filename))
                print(f'Arquivo "{filename}" movido para a pasta "{category}".')
                moved = True
                break
        if not moved:
            others_path = os.path.join(downloads_folder, "Others")
            if not os.path.exists(others_path):
                os.makedirs(others_path)
            shutil.move(file_path, os.path.join(others_path, filename))
            print(f'Arquivo "{filename}" movido para a pasta "Others".')
