print("Copyright ©2025 | Delean Mafra, todos os direitos reservados.")

converte = input('Digite o valor: ')
hex_value = converte

def decimal_para_binario(n):
    return bin(n).replace("0b", "")

def decimal_para_hexadecimal(n):
    return hex(n).replace("0x", "").upper()

def decimal_para_octal(n):
    return oct(n).replace("0o", "")

def binario_para_decimal(b):
    return int(b, 2)

def binario_para_hexadecimal(b):
    decimal = binario_para_decimal(b)
    return decimal_para_hexadecimal(decimal)

def binario_para_octal(b):
    decimal = binario_para_decimal(b)
    return decimal_para_octal(decimal)

def octal_para_decimal(o):
    return int(o, 8)

def octal_para_binario(o):
    decimal = octal_para_decimal(o)
    return decimal_para_binario(decimal)

def octal_para_hexadecimal(o):
    decimal = octal_para_decimal(o)
    return decimal_para_hexadecimal(decimal)

def hexadecimal_para_decimal(h):
    return int(h, 16)

def hexadecimal_para_binario(h):
    decimal = hexadecimal_para_decimal(h)
    return decimal_para_binario(decimal)

def hexadecimal_para_octal(h):
    decimal = hexadecimal_para_decimal(h)
    return decimal_para_octal(decimal)

# Função principal para exibir as conversões
def show_conversions(n):
    try:
        if n.isdigit():
            n = int(n)
            print(f"Decimal para Binário: {n} = {decimal_para_binario(n)}")
            print(f"Decimal para Hexadecimal: {n} = {decimal_para_hexadecimal(n)}")
            print(f"Decimal para Octal: {n} = {decimal_para_octal(n)}")
        elif all(c in '0123456789ABCDEFabcdef' for c in n):
            # Assuming n is hex
            decimal_value = hexadecimal_para_decimal(n)
            print(f"Hexadecimal para Decimal: {n} = {decimal_value}")
        else:
            raise ValueError("Formato inválido.")
    except ValueError as e:
        print(e)

# Exemplo de uso
show_conversions(converte)

# Resposta à pergunta
decimal_value = hexadecimal_para_decimal(hex_value)
print(f"O número {hex_value} na base hexadecimal corresponde ao número {decimal_value} na base decimal.")
