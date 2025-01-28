from numerize_lib import numerize

# Primeiro captura a string com input, depois converte para float
valor = float(input("Digite um valor: "))

# Como valor é um número único, não precisa do loop
print(f'Valor simplificado: {numerize(valor)}')