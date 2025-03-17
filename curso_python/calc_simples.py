import math
print("Copyright ©2025 | Delean Mafra, todos os direitos reservados.")

def soma_num(num1,num2):
    return num1 + num2


resultados = soma_num(15,20)
print(resultados)

def maior_num(lista_num):
    lista_num.sort()
    lista_num.reverse()
    maior = lista_num[0]  # Aqui está a correção
    return maior  # Certifique-se de retornar o valor

resultado = maior_num([12,35,14,17,21,31,87,1111,20])
print(resultado)
