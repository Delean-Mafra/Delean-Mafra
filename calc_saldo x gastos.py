print("Copyright ©2025 | Delean Mafra, todos os direitos reservados.")

def calcular_tempo(saldo, gasto_mensal):
    meses = saldo / gasto_mensal
    anos = int(meses // 12)
    meses_restantes = int(meses % 12)
    return anos, meses_restantes

saldo_em_conta = 20000
gasto_mensal_excessivo = 400.25

anos, meses_restantes = calcular_tempo(saldo_em_conta, gasto_mensal_excessivo)
print(f"Você ficaria sem dinheiro em aproximadamente {anos} anos e {meses_restantes} meses.")
