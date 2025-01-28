
print("Copyright ©2025 | Delean Mafra, todos os direitos reservados.")


while True:
    try:
        peso = int(input('Digite quantos Kg você deseja converter: '))
        if peso > 0:
            break
        else:
            print("Por favor, insira o total valido: ")
    except ValueError:
        print("Entrada inválida. Por favor, insira um número inteiro.")
        
# Convertendo o peso para gramas
peso = peso * 10**6

if peso < 10**9:
    print(f'{peso / 10**6} kg')
elif peso < 10**12:
    print(f'{peso / 10**9} toneladas')
elif peso < 10**15:
    print(f'{peso / 10**12} Quilotonelada')
elif peso < 10**18:
    print(f'{peso / 10**15} Megatonelada')
elif peso < 10**21:
    print(f'{peso / 10**18} Gigatonelada')
elif peso < 10**24:
    print(f'{peso / 10**21} Teratonelada')
elif peso < 10**27:
    print(f'{peso / 10**24} Petatonelada')
elif peso < 10**30:
    print(f'{peso / 10**27} Exatonelada')     
else:
    print(f'{peso / 10**30} Zettatonelada')
