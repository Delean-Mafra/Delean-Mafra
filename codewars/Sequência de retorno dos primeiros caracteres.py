print("Copyright ©2025 | Delean Mafra, todos os direitos reservados.")


def make_string(s):
    # Divide a cadeia de caracteres em palavras
    words = s.split()

    
    # Pega o primeiro caractere de cada palavra e junta-os em uma nova cadeia de caracteres
    result = ''.join(word[0] for word in words)
    
    return result
print(make_string("This Is A Test"))  # Saída esperada: "TIAT"
