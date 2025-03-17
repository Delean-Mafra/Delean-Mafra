# Lista de dados fornecidos
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
        comprimento = len(item)
        if item in ["verdadeiro", "falso"]:
            tipo = "valor lógico"
        else:
            tipo = "literal"
        resultados[item] = {"tipo": tipo, "comprimento": comprimento}
    return resultados

# Contar caracteres e exibir os resultados
resultados = contar_caracteres(dados)
for item, info in resultados.items():
    print(f'"{item}" - {info["tipo"]} de comprimento {info["comprimento"]}')
