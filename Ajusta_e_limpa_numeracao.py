import pyperclip

print("Copyright ©2024 | Delean Mafra, todos os direitos reservados.")


def limpar_string(string):
    return ''.join(''.join(string.split('-')).split('.')).replace('\n', '').replace(' ', '').replace('/', '')

numero = input("Favor digite o valor desejado: ")

numero_limpo = limpar_string(numero)
print(f"Numero {numero_limpo} copiado com sucesso")

# Copia o valor para a área de transferência
pyperclip.copy(numero_limpo)