import random
import string

print("Copyright ©2025 | Delean Mafra, todos os direitos reservados.")

def gera_bloco():
  """Gera um bloco aleatório de 4 caracteres alfanuméricos."""
  caracteres = string.ascii_uppercase + string.digits
  bloco = ''.join(random.choice(caracteres) for _ in range(4))
  return bloco

def gera_chave():
  """Gera uma chave completa combinando 5 blocos aleatórios."""
  chave = '-'.join(gera_bloco() for _ in range(5))
  return chave

# Gera e exibe uma chave aleatória
chave_aleatoria = gera_chave()
print(chave_aleatoria)
