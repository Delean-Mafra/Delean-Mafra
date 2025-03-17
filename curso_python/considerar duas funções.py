def f(x):
    return 2 * x + 4
print("Copyright ©2025 | Delean Mafra, todos os direitos reservados.")


def g(x):
    return 6

def soma(x):
    return f(x) + g(x)

def subtracao(x):
    return f(x) - g(x)

def produto(x):
    return f(x) * g(x)

def quociente(x):
    return f(x) / g(x)

# Testando as funções com um valor de x
x = 1  # Você pode alterar este valor para testar com outros valores de x

print(f"Soma das funções (f + g) para x = {x}: {soma(x)}")
print(f"Subtração das funções (f - g) para x = {x}: {subtracao(x)}")
print(f"Produto das funções (f * g) para x = {x}: {produto(x)}")
print(f"Quociente das funções (f / g) para x = {x}: {quociente(x)}")
