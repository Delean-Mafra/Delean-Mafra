import pikepdf
import os

print("Copyright ©2025 | Delean Mafra, todos os direitos reservados.")


def desbloquear_pdf(input_pdf, output_pdf):
    # Abrir o arquivo PDF de entrada
    with pikepdf.open(input_pdf) as pdf:
        # Salvar o novo PDF desbloqueado
        pdf.save(output_pdf)

# Exemplo de uso

nome = input('Informe o nome do boleto: ')  # Corrigido o nome de "booleto" para "boleto"
input_caminho_pdf = r'\pdf'

# Corrigindo a montagem do caminho do arquivo
input_pdf = os.path.join(input_caminho_pdf, nome + '.pdf')

output_pdf = r'\pdf\boleto_desbloqueado.pdf'

# Verificar se o arquivo existe antes de tentar desbloqueá-lo
if os.path.exists(input_pdf):
    desbloquear_pdf(input_pdf, output_pdf)
else:
    print(f'O arquivo {input_pdf} não foi encontrado.')



print('PDF desbloqueado com sucesso!')

