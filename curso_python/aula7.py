def big_mac():
    print(f"Sanduiche")
print("Copyright ©2025 | Delean Mafra, todos os direitos reservados.")


def big_mac(nome):
    print(f"Sanduiche para o {nome}")

def fazer_batata(tamanho):
    print(f"batata {tamanho}")

def entregar_refri(tipo_refri,tamanho):
    print(f"{tipo_refri} {tamanho}")

def pedido(nome, tamanho, tipo_refri, tamanho_refri):
    big_mac(nome)
    fazer_batata(tamanho)
    entregar_refri(tipo_refri, tamanho_refri)

pedido("Delean", "Médio", "Guarana", "Grande")
