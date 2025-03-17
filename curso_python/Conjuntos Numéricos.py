import math

def classify_number(num):
    if isinstance(num, int):
        if num >= 0:
            return "N (Número Natural)"
        else:
            return "Z (Número Inteiro)"
    elif isinstance(num, float):
        if num.is_integer():
            return "Z (Número Inteiro)"
        else:
            return "Q (Número Racional)"
    else:
        return "R (Número Real)"
print("Copyright ©2025 | Delean Mafra, todos os direitos reservados.")


def is_irrational(num):
    if isinstance(num, float):
        if num in [math.pi, math.e] or any(math.isclose(num, math.sqrt(x)) for x in [2, 3, 5, 7]):
            return True
    return False

def main():
    try:
        user_input = input("Digite um número: ")
        if user_input.lower() == "pi" or user_input == "π":
            num = math.pi
        else:
            num = float(user_input)
        
        if is_irrational(num):
            print("R (Número Irracional)")
        else:
            print(classify_number(num))
    except ValueError:
        print("Entrada inválida. Por favor, digite um número válido.")

if __name__ == "__main__":
    main()
