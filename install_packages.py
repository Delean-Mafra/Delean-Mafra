import subprocess
import sys

print("Copyright ©2025 | Delean Mafra, todos os direitos reservados.")

def install_package(package):
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"'{package}' instalado com sucesso!")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao instalar '{package}': {e}")

def install_packages():
    packages = [
        "chatterbot",
        "chatterbot_corpus",
        "nltk",
        "cython",
        "numpy",
        "spacy"
    ]
    
    for package in packages:
        install_package(package)

if __name__ == "__main__":
    install_packages()


#pip install --upgrade pyyaml
