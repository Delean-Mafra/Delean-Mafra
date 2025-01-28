import math
print("Copyright ©2025 | Delean Mafra, todos os direitos reservados.")

def tempo_para_decimal(tempo):
    horas, minutos = map(int, tempo.split(':'))
    return horas * 60 + minutos

def decimal_para_sexagesimal(decimal, noturno):
    decimal *= noturno
    horas = decimal // 60
    minutos = decimal % 60
    return horas, minutos

noturno = 8/7

# Pergunta ao usuário se ele deseja uma explicação sobre o adicional noturno
while True:
    resposta = input("Deseja uma explicação sobre o que é adicional noturno antes de usar o programa? (S/N) ").upper()
    if resposta in ["SIM", "S", "YES", "Y"]:
        print("""
O adicional noturno é um direito assegurado pela CLT aos trabalhadores que exercem suas atividades no período noturno, 
entre as 22h e as 5h do dia seguinte. 
Esse adicional visa compensar o trabalhador pelo seu labor em horário considerado mais penoso.
O adicional noturno está previsto no Artigo 73 da CLT, que estabelece:
O tempo de trabalho noturno é contado de forma reduzida. 
Cada 52 minutos e 30 segundos trabalhados equivalem a 1 hora normal.
O cálculo da hora noturna funciona da seguinte forma: 
cada 7 hrs noturnas trabalhadas equivale a 8 hrs diurnas. 
A forma mais simples de chegar no resultado esperado é dividir 7 hrs por 8 hrs, 
aí você terá o fator de peso da hora trabalhada.
Como esse aplicativo funciona:
O fator de conversão noturno é definido como 8/7 para considerar que 1 hora noturna equivale a 1 hora e 8 minutos de trabalho diurno,
ou que 52 minutos e 30 segundos equivale a 1 hora ou até que 7 horas equivalem a 8 horas.
Em resumo, a regra sempre será 8/7 sobre a tempo trabalhado.\n
""")

        break
    elif resposta in ["NÃO", "N", "NO", "N"]:
        break
    else:
        print("Resposta inválida. Por favor, responda com 'S' ou 'N'.")

while True:
    while True:
        try:
            tempo = input("Por favor, insira o tempo no formato HH:MM para ter as horas noturnas ")
            if len(tempo) == 4 and tempo.isdigit():  # Se o tempo for um número de 4 dígitos
                tempo = tempo[:2] + ':' + tempo[2:]  # Insira ":" entre o segundo e o terceiro dígito
            decimal = tempo_para_decimal(tempo)
            horas, minutos = decimal_para_sexagesimal(decimal, noturno)
            print(f"{int(horas)} horas e {int(minutos)} minutos")
            break
        except ValueError:
            print("Valor inválido. Por favor, insira o tempo no formato HH:MM.")
    
    while True:
        resposta = input("Deseja fazer outro cálculo? (S/N) ").upper()
        if resposta in ["SIM", "S", "YES", "Y"]:
            break
        elif resposta in ["NÃO", "N", "NO", "N"]:
            print("Obrigado por usar o programa. Até mais!")
            exit(0)
        else:
            print("Resposta inválida. Por favor, responda com 'S' ou 'N'.")