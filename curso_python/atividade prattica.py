

dados = [
    "NOME",
    "Abacaxi",
    304958,
    "23/12/99",
    "Rua Alfa, 52 - Apto. 1" ,
    45.989,
    "CEP: 11222-333", 
    -90
    
    
]



def contar_caracteres(dados):
    resultados = {}
    for item in dados:
        if type(item) == str:
            tipo = "literal"
            le_quantidade_de_casas_decimas = ' '
            comprimento = len(item)
            comprimento = f'{comprimento} caracteres'
        elif type(item) == int:
            tipo = "inteiro"
            le_quantidade_de_casas_decimas = ''
            if item >= 0:
                comprimento = 'Valor positivo'
            else:
                comprimento = 'Valor negativo'
        elif type(item) == float:
            tipo = "real"
            le_quantidade_de_casas_decimas = len(str(item).split('.')[1])
            le_quantidade_de_casas_decimas = f'{le_quantidade_de_casas_decimas} casas decimais'
            if item >= 0:
                comprimento = 'Valor positivo'
            else:
                comprimento = 'Valor negativo'
        resultados[item] = {"tipo": tipo, "comprimento": comprimento, "le_quantidade_de_casas_decimas": le_quantidade_de_casas_decimas}
            
    return resultados

# Contar caracteres e exibir os resultados
resultados = contar_caracteres(dados)
for item, info in resultados.items():
    print(f'"{item}" - tipo: {info["tipo"]},  {info["comprimento"]} {info["le_quantidade_de_casas_decimas"]}')