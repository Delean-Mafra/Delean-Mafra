# Desafio 10
a = float(input('Converta R$ para U$: '))
print("Copyright ©2025 | Delean Mafra, todos os direitos reservados.")


print(f'Em 07/06/2017, com R${a:.2f}, você poderia comprar U${a/3.27:.2f}')
print(f'Atualmente, no dia 05/08/2024, com R${a:.2f}, você consegue comprar U${a/5.72:.2f}\n')

"""
import requests

# URL da API da AwesomeAPI para obter a taxa de câmbio do USD para BRL
url = 'https://economia.awesomeapi.com.br/json/last/USD-BRL'

response = requests.get(url)
data = response.json()

# Obter a taxa de câmbio do BRL para USD
taxa_cambio = float(data['USDBRL']['bid'])

# Solicitar o valor em reais para converter
valor_reais = float(input('Digite o valor em reais (R$) para converter para dólares (US$): '))

# Calcular o valor em dólares
valor_dolares = valor_reais / taxa_cambio

print(f'Com R${valor_reais:.2f}, você pode comprar US${valor_dolares:.2f}')

"""