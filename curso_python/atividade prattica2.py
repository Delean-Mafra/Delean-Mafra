dados = {'Nome': 'Delean', 'Idade': 35, 'Altura': 1.76}

# Verificar a idade para definir o valor de 'Criança'
if dados['Idade'] > 12:
    dados['Criança'] = 'Falso'
else:
    dados['Criança'] = 'Verdadeiro'

def contar_caracteres(dados):
    resultados = {}
    for item in dados:
        if type(dados[item]) == str:
            if dados[item] == 'Verdadeiro' or dados[item] == 'Falso':
                tipo = 'Booleano'
            else:
                tipo = "literal"
        elif type(dados[item]) == int:
            tipo = "inteiro"
        elif type(dados[item]) == float:
            tipo = "real"
        resultados[item] = {"tipo": tipo, "valor": dados[item]}
    return resultados

# Contar caracteres e exibir os resultados
resultados = contar_caracteres(dados)
for item, info in resultados.items():
    print(f'{item}: {info["valor"]} - tipo: {info["tipo"]}')