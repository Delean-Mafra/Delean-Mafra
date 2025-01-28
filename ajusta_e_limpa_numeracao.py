import pyperclip

print("Copyright ©2025 | Delean Mafra, todos os direitos reservados.")

numero2 = input("digite o valor a ser limpo: ").replace('\n', '').replace(' ', '').replace('/', '').replace('.', '').replace('-', '')
print(numero2)
pyperclip.copy(numero2)



# # def limpar_string(string):
# #     return ''.join(''.join(string.split('-')).split('.')).replace('\n', '').replace(' ', '').replace('/', '')

# # numero = input("Favor digite o valor desejado: ")

# # numero_limpo = limpar_string(numero)
# # print(f"Numero {numero_limpo} copiado com sucesso")

# # # Copia o valor para a área de transferência
# # pyperclip.copy(numero_limpo)





numero2 = input("digite o valor a ser limpo: ").replace('\n', '').replace(' ', '').replace('/', '').replace('.', '').replace('-', '')

print(numero2)
pyperclip.copy(numero2)