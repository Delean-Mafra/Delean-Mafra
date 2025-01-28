import pyperclip
print("Copyright ©2025 | Delean Mafra, todos os direitos reservados.")

while True:
    valor = input('Digite o valor (ou "sair" para encerrar): ').replace('.', ',').replace('\n', '').replace('       ', '').strip()
    
    if valor.lower() == 'sair':
        break
    
    pyperclip.copy(valor)
    print(f'valor {valor} copiado')
