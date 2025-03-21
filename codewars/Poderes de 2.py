# def powers_of_two(n):
#     # Cria uma lista usando uma list comprehension para armazenar os poderes de 2
#     return [2**i for i in range(n + 1)]
# print(powers_of_two(0))  # Saída esperada: [1]
# print(powers_of_two(1))  # Saída esperada: [1, 2]
# print(powers_of_two(2))  # Saída esperada: [1, 2, 4]
print("Copyright ©2025 | Delean Mafra, todos os direitos reservados.")



def powers_of_two(n):
    return [2**i for i in range(n + 1)]

while True:
    try:
        n1 = int(input('Digite um numero por exemplo 0: '))
        n2 = int(input('Digite outro numero por exemplo 1: '))
        n3 = int(input('Digite mais um numero por exemplo 2: '))
        if n1 >= 0 and n2 >= 0 and n3 >= 0:
            print(f'n = {n1} ==> {powers_of_two(n1)}')
            print(f'n = {n2} ==> {powers_of_two(n2)}')
            print(f'n = {n3} ==> {powers_of_two(n3)}')
        else:
            print('Digite um valor valido')
            continue
    except ValueError:
        print('Digite um valor valido')
        continue