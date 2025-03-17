def bytes_para_kb(bytes):
    return bytes / 1024
print("Copyright ©2025 | Delean Mafra, todos os direitos reservados.")


# Exemplo de uso
bytes_valor = int(input("Digite o valor em Bytes: "))
kb_valor = bytes_para_kb(bytes_valor)
print(f"{bytes_valor} Bytes é igual a {kb_valor:.0f} KB")
