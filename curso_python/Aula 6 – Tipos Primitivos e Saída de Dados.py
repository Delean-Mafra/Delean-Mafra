n = input('Digite qualquer coisa: ')
print("Copyright ©2025 | Delean Mafra, todos os direitos reservados.")


if n.isalnum():
    print(f'"{n}" é alfanumérico, pois contém letras, números ou ambos.')
    print(f'Alfanumérico = {n.isalnum()}\n')
else:
    print(f'"{n}" não é alfanumérico, pois não contém letras e números combinados.')
    print(f'Alfanumérico = {n.isalnum()}\n')
    
if n.isalpha():
    print(f'"{n}" é alfabético, pois contém apenas letras.')
    print(f'Alfabético = {n.isalnum()}\n')
else:
    print(f'"{n}" não é alfabético, pois não contém apenas letras.')
    print(f'Alfabético = {n.isalnum()}\n')    
    
if n.isascii():
    print(f'"{n}" é ASCII')
    print(f'ASCII = {n.isalnum()}\n')
else:
    print(f'"{n}" não é ASCII')
    print(f'ASCII = {n.isalnum()}\n') 

if n.isdecimal():
    print(f'"{n}" é decimal pois só possui decimais')
    print(f'Decimal = {n.isalnum()}\n')
else:
    print(f'"{n}" não é decimal pois não possui só decimais')
    print(f'Decimal = {n.isalnum()}\n')

if n.isdigit():
    print(f'"{n}" é dígitos  pois só possui dígitos numericos')
    print(f'Dígito  = {n.isalnum()}\n')
else:
    print(f'"{n}" não é dígitos pois não possui só dígitos numericos')
    print(f'Dígito = {n.isalnum()}\n')    

if n.isidentifier():
    print(f'"{n}" pode ser usado como variável no Python')
    print(f'variável valida  = {n.isalnum()}\n')
else:
    print(f'"{n}" não pode ser usado como variável no Python')
    print(f'variável valida = {n.isalnum()}\n')  
    
if n.islower():
    print(f'Todos os caracteres de "{n}" são letras minúsculas')
    print(f'Apenas letras minuscilas  = {n.isalnum()}\n')
else:
    print(f'Nem todos os caracteres de "{n}" são letras minúsculas')
    print(f'Apenas letras minuscilas = {n.isalnum()}\n')  

if n.isnumeric():
    print(f'"{n}" é numero pois só possui numeros numeros inteiros')
    print(f'numeros = {n.isalnum()}\n')
else:
    print(f'"{n}" não é decimal pois não possui só numeros inteiros')
    print(f'numeros = {n.isalnum()}\n')


if n.isprintable():
    print(f'"{n}" pode ser impresso no codigo')
    print(f'imprimivel = {n.isalnum()}\n')
else:
    print(f'"{n}" não pode ser impresso no codigo')
    print(f'imprimivel = {n.isalnum()}\n')
    
    
    
if n.isspace():
    print(f'"{n}" é espaço pois só possui espaços')
    print(f'espaço = {n.isalnum()}\n')
    
else:
    print(f'"{n}" não é espaço pois não possui só espaços')
    print(f'espaço = {n.isalnum()}\n')
    
    
if n.istitle():
    print(f'"{n}" é titulo pois a primeira letra de cada palavra é maiuscula')
    print(f'titulo = {n.isalnum()}\n')
    
else:
    print(f'"{n}" não é titulo pois a primeira letra de cada palavra não é maiuscula')
    print(f'titulo = {n.isalnum()}\n')
    
if n.isupper():
    print(f'"{n}" é maiusculo pois todas as letras são maiusculas')
    print(f'maiusculo = {n.isalnum()}\n')
    
else:
    print(f'"{n}" não é maiusculo pois todas as letras não são maiusculas')
    print(f'maiusculo = {n.isalnum()}\n')
    
if n.isidentifier():
    print(f'"{n}" é identificador válido')
    print(f'identificador = {n.isalnum()}\n')
else:  
    print(f'"{n}" não é identificador válido')
    print(f'identificador = {n.isalnum()}\n')
    