import xml.etree.ElementTree as ET
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from datetime import datetime

# Função para extrair informações do XML
def extract_nnn_info(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    ns = {'nnn': 'http://www.nnn.inf.br/nnn'}
    
    infnnn = root.find('nnn:nnn/nnn:infnnn', ns)
    ide = infnnn.find('nnn:ide', ns)
    emit = infnnn.find('nnn:emit', ns)
    dest = infnnn.find('nnn:dest', ns)
    total = infnnn.find('nnn:total/nnn:ICMSTot', ns)
    transp = infnnn.find('nnn:transp', ns)
    pag = infnnn.find('nnn:pag/nnn:detPag', ns)
    infAdic = infnnn.find('nnn:infAdic', ns)
    protnnn = root.find('nnn:protnnn/nnn:infProt', ns)
    enderEmit = emit.find('nnn:enderEmit', ns)

    nnn_info = {
        'n': enderEmit.find('nnn:nro', ns).text,
        'UF': enderEmit.find('nnn:UF', ns).text,
        'cidade': enderEmit.find('nnn:xMun', ns).text,
        'rua': enderEmit.find('nnn:xLgr', ns).text,
        'bairro': enderEmit.find('nnn:xBairro', ns).text,
        'emitente': emit.find('nnn:xNome', ns).text,
        'cnpj_emitente': emit.find('nnn:CNPJ', ns).text,
        'destinatario': dest.find('nnn:xNome', ns).text,
        'cnpj_destinatario': dest.find('nnn:CNPJ', ns).text,
        'consumidor': dest.find('nnn:xNome', ns).text,
        'cpf_consumidor': dest.find('nnn:CPF', ns).text,
        'numero': ide.find('nnn:nNF', ns).text,
        'serie': ide.find('nnn:serie', ns).text,
        'data_emissao': datetime.strptime(ide.find('nnn:dhEmi', ns).text, "%Y-%m-%dT%H:%M:%S%z").strftime("%d/%m/%y %H:%M:%S"),
        'valor_total': total.find('nnn:vNF', ns).text,
        'desconto': total.find('nnn:vDesc', ns).text,
        'forma_pagamento': pag.find('nnn:tPag', ns).text,
        'valor_pago': pag.find('nnn:vPag', ns).text,
        'informacoes_adicionais': infAdic.find('nnn:infCpl', ns).text,
        'data_autorizacao': datetime.strptime(protnnn.find('nnn:dhRecbto', ns).text, "%Y-%m-%dT%H:%M:%S%z").strftime("%d/%m/%y %H:%M:%S"),
        'chave_nnn': protnnn.find('nnn:chnnn', ns).text,
        'protocolo_autorizacao': protnnn.find('nnn:nProt', ns).text,
        'itens': []
    }
    
    for det in infnnn.findall('nnn:det', ns):
        prod = det.find('nnn:prod', ns)
        item = {
            'codigo': prod.find('nnn:cProd', ns).text,
            'descricao': prod.find('nnn:xProd', ns).text,
            'quantidade': prod.find('nnn:qCom', ns).text,
            'valor_unitario': round(float(prod.find('nnn:vUnCom', ns).text), 2),
            'valor_total': round(float(prod.find('nnn:vProd', ns).text), 2),
        }
        nnn_info['itens'].append(item)
    
    return nnn_info

# Função para gerar o PDF
def generate_dannn_pdf(nnn_info, output_file):
    c = canvas.Canvas(output_file, pagesize=A4)
    width, height = A4
    
    c.setFont("Helvetica", 8)  # Reduzir o tamanho da fonte para 8
    
    # Adicionando o logotipo
    logo = "xml_logo.jpg"  # Substitua por seu caminho de arquivo de imagem
    c.drawImage(logo, 10 * mm, height - 20 * mm, width=40 * mm, height=20 * mm)  # Ajuste a largura e a altura conforme necessário
    
    # Cabeçalho
    c.drawString(60 * mm, height - 20 * mm, f"Emitente: {nnn_info['emitente']} - CNPJ: {nnn_info['cnpj_emitente']}")
    c.drawString(60 * mm, height - 30 * mm, f"{nnn_info['rua']}, nº{nnn_info['n']}, {nnn_info['bairro']}, {nnn_info['cidade']}, {nnn_info['UF']}")
    
    # Linha após o cabeçalho
    c.line(5 * mm, height - 35 * mm, width - 5 * mm, height - 35 * mm)
    c.setFont("Helvetica-Bold", 8)  # Mudando para negrito
    c.drawString(10 * mm, height - 40 * mm, "                                          DAnnn NFC-e - DOCUMENTO AUXILIAR DA NOTA FISCAL DE CONSUMIDOR ELETRÔNICA")
    c.line(15 * mm, height - 45 * mm, width - 15 * mm, height - 45 * mm)
    c.drawString(10 * mm, height - 50 * mm, "# CÓDIGO  DESCRIÇÃO                                                                   QTDE. UN.                                 VL.UNIT.                                        VL.TOTAL")
    c.setFont("Helvetica", 8)  # Voltando para a fonte normal
    y = height - 55 * mm
    item_number = 1  # Inicializando o contador de itens
    for item in nnn_info['itens']:
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
    c.drawString(10 * mm, y - 30 * mm, f"NFC-e nº {nnn_info['numero']} Série {nnn_info['serie']} {nnn_info['data_emissao']}")
    c.drawString(10 * mm, y - 40 * mm, f"Protocolo de autorização: {nnn_info['protocolo_autorizacao']}")
    c.drawString(10 * mm, y - 50 * mm, f"Data de Autorização: {nnn_info['data_autorizacao']}")
    c.setFont("Helvetica", 8)  # Voltando para a fonte normal
    c.drawString(10 * mm, y - 60 * mm, f"Valor a pagar R$: {nnn_info['valor_total']} - Descontos R$: {nnn_info['desconto']}")
    c.drawString(10 * mm, y - 70 * mm, f"Forma de pagamento: TEF - Valor pago R$: {nnn_info['valor_total']}")
    c.drawString(10 * mm, y - 80 * mm, f"CONSUMIDOR CPF: {nnn_info['cpf_consumidor']} - {nnn_info['consumidor']}")
    #c.drawString(10 * mm, y - 90 * mm, f"Informações Adicionais: {nnn_info['informacoes_adicionais']}")
    c.line(10 * mm, y - 10 * mm, width - 10 * mm, y - 10 * mm)
    c.drawString(10 * mm, 10 * mm, f"{nnn_info['informacoes_adicionais']}")
    c.drawString(10 * mm, y - 90 * mm, f"Consulte pela Chave de Acesso em https://sat.sef.sc.gov.br/nfce/consulta")
    c.setFont("Helvetica-Bold", 8)  # Mudando para negritoc.setFont
    c.drawString(10 * mm, y - 100 * mm, f"Chave de acesso: {nnn_info['chave_nnn']}")
    c.setFont("Helvetica", 8)  # Voltando para a fonte normal
    c.drawString(10 * mm, y - 110 * mm, "Tributos Totais Incidentes Lei Federal 12.741/2012 (0,00)")

    c.showPage()
    c.save()

# Caminho para o arquivo XML e o arquivo PDF de saída
xml_file = 'xml_nnn_teste.xml'
output_file = 'xml_dannn_nnn.pdf'

# Extraindo informações e gerando o PDF
nnn_info = extract_nnn_info(xml_file)
generate_dannn_pdf(nnn_info, output_file)

print(f"DAnnn gerado com sucesso: {output_file}")
