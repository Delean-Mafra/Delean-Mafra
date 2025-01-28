import pyperclip

print("Copyright ©2025 | Delean Mafra, todos os direitos reservados.")

troca_barra = input('Informe o caminho: ').replace('file:///','').replace('/', '\\')

                                                    
pyperclip.copy(troca_barra)
print(troca_barra)
