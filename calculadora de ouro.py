
print("Copyright ©2025 | Delean Mafra, todos os direitos reservados.")

# Define o preço do ouro puro por grama em BRL
preco_por_grama = 385.73

# Solicita a pureza do ouro em quilates e converte para inteiro

while True:
    try:
        pureza_em_quilates = int(input('Quilates do ouro (1-24): '))
        if 1 <= pureza_em_quilates <= 24:
            break
        else:
            print("Por favor, insira um número entre 1 e 24.")
    except ValueError:
        print("Entrada inválida. Por favor, insira um número inteiro.")


# Calcula a porcentagem de ouro puro em 1 quilate
percentual_ouro_puro = pureza_em_quilates / 24

# Solicita o peso da barra de ouro em gramas e converte para inteiro
while True:
    try:
        peso_da_barra_de_ouro = int(input('Peso do ouro em gramas: '))
        if peso_da_barra_de_ouro > 0:
            break
        else:
            print("Por favor, insira o total de gramas: ")
    except ValueError:
        print("Entrada inválida. Por favor, insira um número inteiro.")



# Calcula o valor de 1 quilograma de ouro com pureza de 1 quilate
valor_da_barra_de_ouro = peso_da_barra_de_ouro * preco_por_grama * percentual_ouro_puro

# Imprime o valor da barra de ouro



if peso_da_barra_de_ouro < 1000:
    print(f"O valor de uma barra de ouro de {peso_da_barra_de_ouro} gramas com pureza de {pureza_em_quilates} quilate(s) é aproximadamente BRL {valor_da_barra_de_ouro:.2f}")
elif peso_da_barra_de_ouro >= 1000 and peso_da_barra_de_ouro < 1000000:
    print(f"O valor de uma barra de ouro de {peso_da_barra_de_ouro/1000} Kg com pureza de {pureza_em_quilates} quilate(s) é aproximadamente BRL {valor_da_barra_de_ouro:.2f}")
elif peso_da_barra_de_ouro >= 1000000:
    print(f"O valor de uma barra de ouro de {peso_da_barra_de_ouro/1000000} toneladas com pureza de {pureza_em_quilates} quilate(s) é aproximadamente BRL {valor_da_barra_de_ouro:.2f}")

    

