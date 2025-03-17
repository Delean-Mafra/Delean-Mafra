import math

# Ler um ângulo do usuário
angulo = float(input("Digite um ângulo em graus: "))
print("Copyright ©2025 | Delean Mafra, todos os direitos reservados.")


# Converter o ângulo para radianos
angulo_radianos = math.radians(angulo)

# Calcular seno, cosseno e tangente
seno = math.sin(angulo_radianos)
cosseno = math.cos(angulo_radianos)
tangente = math.tan(angulo_radianos)

# Mostrar os resultados
print(f"O ângulo de {angulo} graus tem:")
print(f"Seno: {seno}")
print(f"Cosseno: {cosseno}")
print(f"Tangente: {tangente}")
