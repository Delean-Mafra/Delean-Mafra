import subprocess
import sys
print("Copyright ©2025 | Delean Mafra, todos os direitos reservados.")


# Lista de dependências com versão específica do numpy
dependencias = [
    "cymem",
    "preshed",
    "murmurhash",
    "thinc",
    "blis",
    "wasabi",
    "srsly",
    "numpy==1.26.0",
    "plac",
    "tqdm",
    "colorama",
    "chatterbot",
    "chatterbot_corpus",
    "nltk",
    "cython",
    "numpy",
    "spacy"    
]

# Função para desinstalar pacotes
def desinstalar_pacote(pacote):
    subprocess.check_call([sys.executable, "-m", "pip", "uninstall", "-y", pacote])

# Desinstalar todas as dependências
for pacote in dependencias:
    desinstalar_pacote(pacote)

print("Todas as dependências foram desinstaladas com sucesso!")
