### Estou aprendendo Python do jeito certo ###
print("Copyright ©2025 | Delean Mafra, todos os direitos reservados.")



from fpdf import FPDF

projeto = input("Digite a descrição do projeto: ")
horas_estimadas = int(input("Digite o total de horas estimadas: "))
valor_hora = int(input("Digite o valor da hora trabalhada: "))
prazo = input("Digite o prazo estimado para conclusão: ")

valor_total = (horas_estimadas) * (valor_hora)

variante = str(valor_total)+",00"
valor_total = variante
variante = str(horas_estimadas)
horas_estimadas = variante+":00"
variante = str(valor_hora)
valor_hora = variante+",00"

pdf = FPDF()
pdf.add_page()
pdf.set_font('Arial')


pdf.image('template.png', x=0, y=0)

pdf.text(115, 145, projeto)
pdf.text(115, 160, horas_estimadas)
pdf.text(115, 175, valor_hora)
pdf.text(115, 190, prazo)
pdf.text(115, 205, (valor_total))

pdf.output('Orçamento.pdf')

print("Orçamento gerado com sucesso!")
