'''i = 1


while i < 10:
    print(i)
    i += 1

print("Terminou")
print(i)
'''

'''
criancas = ["Efraim","Sofia","Georgia","Eliza"]

for item in criancas:
    print(item)
'''

'''
canal = "Mafra"

for letra in canal:
    print(letra)
'''

'''
for index in range(0,21,2):
    print(index)
    '''

'''
criancas = ["Efraim","Sofia","Georgia","Eliza"]

for index in range(len(criancas)):
    print(criancas[index],index)

'''

"""for index in range(5):
    if index == 0:
        print("Primeira linha")
    else:
        print(f"Outras linhas {index}")"""
print("Copyright ©2025 | Delean Mafra, todos os direitos reservados.")

matrix_num = [
[1,2,3],
[4,5,6],
[7,8,9],
[0],
]

for linha in matrix_num:
    print("-----")
    for coluna in linha:
        print(coluna)