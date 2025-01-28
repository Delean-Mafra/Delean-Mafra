import pyperclip

print("Copyright ©2025 | Delean Mafra, todos os direitos reservados.")

total = input('Digite o valor total: ').replace('.', '').replace(',', '.')

total = float(total)

total_str = str(total).replace('.', ',')
print(f'Valor {total_str}0 copiado para área de transferencia')
pyperclip.copy(f'{total_str}0')


mensalidade_plano = input('DESC.MENSALIDADE PLANO: ').replace('.', '').replace(',', '.')
mensalidade_plano = float(mensalidade_plano)

incidencia_plano = mensalidade_plano/total*100

incidencia_plano = str(incidencia_plano).replace('.', ',')

print(f'Valor {incidencia_plano}% copiado para área de transferencia')
pyperclip.copy(incidencia_plano)

# INSS define valor para base 
inss = input('Valor base INSS: ').replace('.', '').replace(',', '.')
inss = float(inss)
inss_str = str(inss).replace('.', ',')
# print(f'Valor {inss_str} copiado para área de transferencia')
# pyperclip.copy(inss_str)
incidencia_inss = inss/total*100
incidencia_inss = str(incidencia_inss).replace('.', ',')
print(f'Valor {incidencia_inss}% copiado para área de transferencia')
pyperclip.copy(incidencia_inss)

irrf = input('Valor base IRRF: ').replace('.', '').replace(',', '.')
irrf = float(irrf)
irrf_str = str(irrf).replace('.', ',')
incidencia_irrf = irrf/total*100
incidencia_irrf = str(incidencia_irrf).replace('.', ',')
print(f'Valor {incidencia_irrf}% copiado para área de transferencia')
pyperclip.copy(incidencia_irrf)

