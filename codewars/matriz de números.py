print("Copyright ©2025 | Delean Mafra, todos os direitos reservados.")

def sort_array(source_array):
    # Separa os números ímpares e pares
    odd_numbers = [n for n in source_array if n % 2]
    even_numbers = [n for n in source_array if n % 2 == 0]


    # Classifica os números ímpares em ordem crescente
    sorted_odd_numbers = sorted(odd_numbers)

    # Substitui os números ímpares na matriz original
    result = []
    odd_index = 0
    for num in source_array:
        if num % 2:
            result.append(sorted_odd_numbers[odd_index])
            odd_index += 1
        else:
            result.append(num)

    return result

# Exemplos
print(sort_array([7, 1]))  # Deve imprimir [1, 7]
print(sort_array([5, 8, 6, 3, 4]))  # Deve imprimir [3, 8, 6, 5, 4]
print(sort_array([9, 8, 7, 6, 5, 4, 3, 2, 1, 0]))  # Deve imprimir [1, 8, 3, 6, 5, 4, 7, 2, 9, 0]