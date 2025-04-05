def calcular_digito_verificacao_isbn(isbn):

    if not isinstance(isbn, str) or not isbn.isdigit() or len(isbn) != 9:
        return -1  # ISBN inválido

    soma = 0
    pesos = range(10, 1, -1)  # Pesos de 10 a 2

    for i in range(9):
        digito = int(isbn[i])
        peso = pesos[i]
        soma += digito * peso


    resto = soma % 11
    if resto == 0:
        digito_verificacao = 0
    else:
        digito_verificacao = 11 - resto

    return digito_verificacao

# Exemplo de uso com o ISBN fornecido (158714373)
isbn_exemplo = "158714373"
digito_verificacao = calcular_digito_verificacao_isbn(isbn_exemplo)

if digito_verificacao != -1:
    print(f"Para o ISBN {isbn_exemplo}, o dígito de verificação calculado é: {digito_verificacao}")
else:
    print("O ISBN fornecido é inválido.")

# Verificando o exemplo do texto:
isbn_texto = "158714373"
soma_texto = 0
pesos_texto = range(10, 1, -1)
for i in range(9):
    soma_texto += int(isbn_texto[i]) * pesos_texto[i]
print(f"Soma do exemplo do texto: {soma_texto}") # Deve ser 233

resto_texto = soma_texto % 11
digito_verificacao_texto = (11 - resto_texto) % 11
print(f"Dígito de verificação calculado para o exemplo do texto: {digito_verificacao_texto}") # Deve ser 9
