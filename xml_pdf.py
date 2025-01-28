import xml.etree.ElementTree as ET
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from datetime import datetime

print("Copyright ©2025 | Delean Mafra, todos os direitos reservados.")


# Função para extrair informações do XML
def extract_deleanmafra_info(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    ns = {'deleanmafra': 'http://www.deleanmafra.inf.br/deleanmafra'}
    
    infdeleanmafra = root.find('deleanmafra:deleanmafra/deleanmafra:infdeleanmafra', ns)
    ide = infdeleanmafra.find('deleanmafra:ide', ns)
    emit = infdeleanmafra.find('deleanmafra:emit', ns)
    dest = infdeleanmafra.find('deleanmafra:dest', ns)
    total = infdeleanmafra.find('deleanmafra:total/deleanmafra:ICMSTot', ns)
    transp = infdeleanmafra.find('deleanmafra:transp', ns)
    pag = infdeleanmafra.find('deleanmafra:pag/deleanmafra:detPag', ns)
    infAdic = infdeleanmafra.find('deleanmafra:infAdic', ns)
    protdeleanmafra = root.find('deleanmafra:protdeleanmafra/deleanmafra:infProt', ns)
    enderEmit = emit.find('deleanmafra:enderEmit', ns)

    deleanmafra_info = {
        'n': enderEmit.find('deleanmafra:nro', ns).text,
        'UF': enderEmit.find('deleanmafra:UF', ns).text,
        'cidade': enderEmit.find('deleanmafra:xMun', ns).text,
        'rua': enderEmit.find('deleanmafra:xLgr', ns).text,
        'bairro': enderEmit.find('deleanmafra:xBairro', ns).text,
        'emitente': emit.find('deleanmafra:xNome', ns).text,
        'cnpj_emitente': emit.find('deleanmafra:CNPJ', ns).text,
        'destinatario': dest.find('deleanmafra:xNome', ns).text,
        'cnpj_destinatario': dest.find('deleanmafra:CNPJ', ns).text,
        'consumidor': dest.find('deleanmafra:xNome', ns).text,
        'cpf_consumidor': dest.find('deleanmafra:CPF', ns).text,
        'numero': ide.find('deleanmafra:nNF', ns).text,
        'serie': ide.find('deleanmafra:serie', ns).text,
        'data_emissao': datetime.strptime(ide.find('deleanmafra:dhEmi', ns).text, "%Y-%m-%dT%H:%M:%S%z").strftime("%d/%m/%y %H:%M:%S"),
        'valor_total': total.find('deleanmafra:vNF', ns).text,
        'desconto': total.find('deleanmafra:vDesc', ns).text,
        'forma_pagamento': pag.find('deleanmafra:tPag', ns).text,
        'valor_pago': pag.find('deleanmafra:vPag', ns).text,
        'informacoes_adicionais': infAdic.find('deleanmafra:infCpl', ns).text,
        'data_autorizacao': datetime.strptime(protdeleanmafra.find('deleanmafra:dhRecbto', ns).text, "%Y-%m-%dT%H:%M:%S%z").strftime("%d/%m/%y %H:%M:%S"),
        'chave_deleanmafra': protdeleanmafra.find('deleanmafra:chdeleanmafra', ns).text,
        'protocolo_autorizacao': protdeleanmafra.find('deleanmafra:nProt', ns).text,
        'itens': []
    }
    
    for det in infdeleanmafra.findall('deleanmafra:det', ns):
        prod = det.find('deleanmafra:prod', ns)
        item = {
            'codigo': prod.find('deleanmafra:cProd', ns).text,
            'descricao': prod.find('deleanmafra:xProd', ns).text,
            'quantidade': prod.find('deleanmafra:qCom', ns).text,
            'valor_unitario': round(float(prod.find('deleanmafra:vUnCom', ns).text), 2),
            'valor_total': round(float(prod.find('deleanmafra:vProd', ns).text), 2),
        }
        deleanmafra_info['itens'].append(item)
    
    return deleanmafra_info

# Função para gerar o PDF
def generate_dadeleanmafra_pdf(deleanmafra_info, output_file):
    c = canvas.Canvas(output_file, pagesize=A4)
    width, height = A4
    
    c.setFont("Helvetica", 8)  # Reduzir o tamanho da fonte para 8
    
    # Adicionando o logotipo
    logo = "xml_logo.jpg"  # Substitua por seu caminho de arquivo de imagem
    c.drawImage(logo, 10 * mm, height - 20 * mm, width=40 * mm, height=20 * mm)  # Ajuste a largura e a altura conforme necessário
    
    # Cabeçalho
    c.drawString(60 * mm, height - 20 * mm, f"Emitente: {deleanmafra_info['emitente']} - CNPJ: {deleanmafra_info['cnpj_emitente']}")
    c.drawString(60 * mm, height - 30 * mm, f"{deleanmafra_info['rua']}, nº{deleanmafra_info['n']}, {deleanmafra_info['bairro']}, {deleanmafra_info['cidade']}, {deleanmafra_info['UF']}")
    
    # Linha após o cabeçalho
    c.line(5 * mm, height - 35 * mm, width - 5 * mm, height - 35 * mm)
    c.setFont("Helvetica-Bold", 8)  # Mudando para negrito
    c.drawString(10 * mm, height - 40 * mm, "                                          DAdeleanmafra NFC-e - DOCUMENTO AUXILIAR DA NOTA FISCAL DE CONSUMIDOR ELETRÔNICA")
    c.line(15 * mm, height - 45 * mm, width - 15 * mm, height - 45 * mm)
    c.drawString(10 * mm, height - 50 * mm, "# CÓDIGO  DESCRIÇÃO                                                                   QTDE. UN.                                 VL.UNIT.                                        VL.TOTAL")
    c.setFont("Helvetica", 8)  # Voltando para a fonte normal
    y = height - 55 * mm
    item_number = 1  # Inicializando o contador de itens
    for item in deleanmafra_info['itens']:
        c.drawString(10 * mm, y, f"{item_number} {item['codigo']}       {item['descricao']}")
        c.drawString(100 * mm, y, f"{item['quantidade']}")
        c.drawString(140 * mm, y, f"{item['valor_unitario']}")  # Arredondar para 2 casas decimais
        c.drawString(180 * mm, y, f"{item['valor_total']}")  # Arredondar para 2 casas decimais
        y -= 10 * mm
        item_number += 1  # Incrementar o contador de itens
    
    # Linha antes do rodapé
    c.line(10 * mm, y - 10 * mm, width - 10 * mm, y - 10 * mm)
    
    # Movendo as informações adicionais, a data de emissão, o número da chave e a mensagem sobre os tributos totais para o final do PDF
    c.setFont("Helvetica-Bold", 8)  # Mudando para negrito
    c.drawString(10 * mm, y - 30 * mm, f"NFC-e nº {deleanmafra_info['numero']} Série {deleanmafra_info['serie']} {deleanmafra_info['data_emissao']}")
    c.drawString(10 * mm, y - 40 * mm, f"Protocolo de autorização: {deleanmafra_info['protocolo_autorizacao']}")
    c.drawString(10 * mm, y - 50 * mm, f"Data de Autorização: {deleanmafra_info['data_autorizacao']}")
    c.setFont("Helvetica", 8)  # Voltando para a fonte normal
    c.drawString(10 * mm, y - 60 * mm, f"Valor a pagar R$: {deleanmafra_info['valor_total']} - Descontos R$: {deleanmafra_info['desconto']}")
    c.drawString(10 * mm, y - 70 * mm, f"Forma de pagamento: TEF - Valor pago R$: {deleanmafra_info['valor_total']}")
    c.drawString(10 * mm, y - 80 * mm, f"CONSUMIDOR CPF: {deleanmafra_info['cpf_consumidor']} - {deleanmafra_info['consumidor']}")
    #c.drawString(10 * mm, y - 90 * mm, f"Informações Adicionais: {deleanmafra_info['informacoes_adicionais']}")
    c.line(10 * mm, y - 10 * mm, width - 10 * mm, y - 10 * mm)
    c.drawString(10 * mm, 10 * mm, f"{deleanmafra_info['informacoes_adicionais']}")
    c.drawString(10 * mm, y - 90 * mm, f"Consulte pela Chave de Acesso em https://sat.sef.sc.gov.br/nfce/consulta")
    c.setFont("Helvetica-Bold", 8)  # Mudando para negritoc.setFont
    c.drawString(10 * mm, y - 100 * mm, f"Chave de acesso: {deleanmafra_info['chave_deleanmafra']}")
    c.setFont("Helvetica", 8)  # Voltando para a fonte normal
    c.drawString(10 * mm, y - 110 * mm, "Tributos Totais Incidentes Lei Federal 12.741/2012 (0,00)")

    c.showPage()
    c.save()

# Caminho para o arquivo XML e o arquivo PDF de saída
xml_file = 'xml_deleanmafra_teste.xml'
output_file = 'xml_dadeleanmafra_deleanmafra.pdf'

# Extraindo informações e gerando o PDF
deleanmafra_info = extract_deleanmafra_info(xml_file)
generate_dadeleanmafra_pdf(deleanmafra_info, output_file)

print(f"DAdeleanmafra gerado com sucesso: {output_file}")
