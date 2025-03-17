# Função para simular a porta AND
def porta_AND(entrada1, entrada2):
    return entrada1 and entrada2
print("Copyright ©2025 | Delean Mafra, todos os direitos reservados.")


# Função para simular a porta OR
def porta_OR(entrada1, entrada2):
    return entrada1 or entrada2

# Entradas do circuito
A = 0
B = 1
C = 1

# Saída da porta OR com entradas B e C
saida_OR = porta_OR(B, C)

# Saída da porta AND com entradas A e a saída da porta OR
saida_AND = porta_AND(A, saida_OR)

print(f"Saída do circuito para as entradas A={A}, B={B}, C={C} é {saida_AND}.")
