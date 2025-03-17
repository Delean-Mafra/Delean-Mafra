print("Copyright ©2025 | Delean Mafra, todos os direitos reservados.")

def busca_binaria(lista, alvo):
    inicio = 0
    fim = len(lista) - 1


    while inicio <= fim:
        meio = (inicio + fim) // 2
        chute = lista[meio]

        if chute == alvo:
            return meio
        elif chute > alvo:
            fim = meio - 1
        else:
            inicio = meio + 1

    return None

# Exemplo de uso:
# A lista deve estar ordenada para a busca binária funcionar corretamente.
lista_ordenada = [1, 3, 5, 7, 9]
valor_alvo = 5

resultado = busca_binaria(lista_ordenada, valor_alvo)
if resultado is not None:
    print(f"Valor encontrado no índice: {resultado}")
else:
    print("Valor não encontrado na lista.")
