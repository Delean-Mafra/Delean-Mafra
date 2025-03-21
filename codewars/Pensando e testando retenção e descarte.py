print("Copyright ©2025 | Delean Mafra, todos os direitos reservados.")

def mystery(n):
    if n <= 0:
        return []

    
    divisores = [1]  # Sempre inclui 1
    for i in range(2, n + 1):
        if n % i == 0 and i % 2 != 0:  # Se for divisor e ímpar
            divisores.append(i)
    
    return divisores
