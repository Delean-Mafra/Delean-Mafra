
# """def decimal_para_sexagesimal(decimal):
#     horas = decimal // 60
#     minutos = decimal % 60
#     return horas, minutos

# decimal = int(input("Por favor, insira o valor decimal para ter as horas normais: "))
# horas, minutos = decimal_para_sexagesimal(decimal)
# print(f"{horas}:{minutos}")



# def decimal_para_sexagesimal(decimal, noturno):
#     decimal *= noturno
#     horas = decimal // 60
#     minutos = decimal % 60
#     return horas, minutos

# noturno = 8/7
# decimal = float(input("Por favor, insira o valor decimal para ter as horas noturnas: "))
# horas, minutos = decimal_para_sexagesimal(decimal, noturno)
# print(f"{int(horas)} horas e {int(minutos)} minutos")
# """
import math
print("Copyright © 2024 | Delean Mafra, todos os direitos reservados.")

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
    resposta = input("Deseja uma explicação sobre o que é adicional noturno? (S/N) ").upper()
    if resposta in ["SIM", "S", "YES", "Y"]:
        print("O adicional noturno é um direito assegurado pela Consolidação das Leis do Trabalho (CLT) aos trabalhadores que exercem suas atividades no período noturno, entre as 22h e as 5h do dia seguinte. Esse adicional visa compensar o trabalhador pelo seu labor em horário considerado mais penoso.")
        print("O adicional noturno está previsto no Artigo 73 da CLT, que estabelece:")
        print("O tempo de trabalho noturno é contado de forma reduzida. Cada 52 minutos e 30 segundos trabalhados equivalem a 1 hora normal.")
        print("O calculo da hora noturna funciona da seguinte forma cada 7 hrs noturnas trabalhdas equivale a 8 hrs diurnas, a forma mais simples de chegar no resultado esperado é dividir 7 hrs por 8 hrs ai você tera o fator de peso da hora trabalhada")
        print("Como esse aplicativo funciona: ")
        print("O fator de conversão noturno é definido como 8/7 para considerar que 1 hora noturna equivale a 1 hora e 8 minutos de trabalho diurno.")
        
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

