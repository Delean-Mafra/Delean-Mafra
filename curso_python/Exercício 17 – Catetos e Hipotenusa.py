from math import sqrt

# Ler os comprimentos dos catetos
cateto_oposto = float(input("Digite o comprimento do cateto oposto: "))
cateto_adjacente = float(input("Digite o comprimento do cateto adjacente: "))
print("Copyright ©2025 | Delean Mafra, todos os direitos reservados.")


# Calcular a hipotenusa
hipotenusa = sqrt(cateto_oposto**2 + cateto_adjacente**2)

# Mostrar o resultado
print(f"O comprimento da hipotenusa é: {hipotenusa}")
