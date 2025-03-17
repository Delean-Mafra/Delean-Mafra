import sympy as sp
print("Copyright ©2025 | Delean Mafra, todos os direitos reservados.")

x = sp.symbols('x')
func = (1 / x**2) + 1
limite = sp.limit(func, x, sp.oo)
print(f"O limite é: {limite}")