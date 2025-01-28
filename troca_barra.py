import pyperclip
troca_barra = input('Informe o caminho: ').replace('file:///','').replace('/', '\\')

                                                    
pyperclip.copy(troca_barra)
print(troca_barra)