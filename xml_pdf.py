import xml.etree.ElementTree as ET
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from datetime import datetime

# Função para extrair informações do XML
def extract_nfe_info(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    ns = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}
    
    infNFe = root.find('nfe:NFe/nfe:infNFe', ns)
    ide = infNFe.find('nfe:ide', ns)
    emit = infNFe.find('nfe:emit', ns)
    dest = infNFe.find('nfe:dest', ns)
    total = infNFe.find('nfe:total/nfe:ICMSTot', ns)
    transp = infNFe.find('nfe:transp', ns)
    pag = infNFe.find('nfe:pag/nfe:detPag', ns)
    infAdic = infNFe.find('nfe:infAdic', ns)
    protNFe = root.find('nfe:protNFe/nfe:infProt', ns)
    enderEmit = emit.find('nfe:enderEmit', ns)

    nfe_info = {
        'n': enderEmit.find('nfe:nro', ns).text,
        'UF': enderEmit.find('nfe:UF', ns).text,
        'cidade': enderEmit.find('nfe:xMun', ns).text,
        'rua': enderEmit.find('nfe:xLgr', ns).text,
        'bairro': enderEmit.find('nfe:xBairro', ns).text,
        'emitente': emit.find('nfe:xNome', ns).text,
        'cnpj_emitente': emit.find('nfe:CNPJ', ns).text,
        'destinatario': dest.find('nfe:xNome', ns).text,
        'cnpj_destinatario': dest.find('nfe:CNPJ', ns).text,
        'consumidor': dest.find('nfe:xNome', ns).text,
        'cpf_consumidor': dest.find('nfe:CPF', ns).text,
        'numero': ide.find('nfe:nNF', ns).text,
        'serie': ide.find('nfe:serie', ns).text,
        'data_emissao': datetime.strptime(ide.find('nfe:dhEmi', ns).text, "%Y-%m-%dT%H:%M:%S%z").strftime("%d/%m/%y %H:%M:%S"),
        'valor_total': total.find('nfe:vNF', ns).text,
        'desconto': total.find('nfe:vDesc', ns).text,
        'forma_pagamento': pag.find('nfe:tPag', ns).text,
        'valor_pago': pag.find('nfe:vPag', ns).text,
        'informacoes_adicionais': infAdic.find('nfe:infCpl', ns).text,
        'data_autorizacao': datetime.strptime(protNFe.find('nfe:dhRecbto', ns).text, "%Y-%m-%dT%H:%M:%S%z").strftime("%d/%m/%y %H:%M:%S"),
        'chave_nfe': protNFe.find('nfe:chNFe', ns).text,
        'protocolo_autorizacao': protNFe.find('nfe:nProt', ns).text,
        'itens': []
    }
    
    for det in infNFe.findall('nfe:det', ns):
        prod = det.find('nfe:prod', ns)
        item = {
            'codigo': prod.find('nfe:cProd', ns).text,
            'descricao': prod.find('nfe:xProd', ns).text,
            'quantidade': prod.find('nfe:qCom', ns).text,
            'valor_unitario': round(float(prod.find('nfe:vUnCom', ns).text), 2),
            'valor_total': round(float(prod.find('nfe:vProd', ns).text), 2),
        }
        nfe_info['itens'].append(item)
    
    return nfe_info

# Função para gerar o PDF
def generate_danfe_pdf(nfe_info, output_file):
    c = canvas.Canvas(output_file, pagesize=A4)
    width, height = A4
    
    c.setFont("Helvetica", 8)  # Reduzir o tamanho da fonte para 8
    
    # Adicionando o logotipo
    logo = "xml_logo.jpg"  # Substitua por seu caminho de arquivo de imagem
    c.drawImage(logo, 10 * mm, height - 20 * mm, width=40 * mm, height=20 * mm)  # Ajuste a largura e a altura conforme necessário
    
    # Cabeçalho
    c.drawString(60 * mm, height - 20 * mm, f"Emitente: {nfe_info['emitente']} - CNPJ: {nfe_info['cnpj_emitente']}")
    c.drawString(60 * mm, height - 30 * mm, f"{nfe_info['rua']}, nº{nfe_info['n']}, {nfe_info['bairro']}, {nfe_info['cidade']}, {nfe_info['UF']}")
    
    # Linha após o cabeçalho
    c.line(5 * mm, height - 35 * mm, width - 5 * mm, height - 35 * mm)
    c.setFont("Helvetica-Bold", 8)  # Mudando para negrito
    c.drawString(10 * mm, height - 40 * mm, "                                          DANFE NFC-e - DOCUMENTO AUXILIAR DA NOTA FISCAL DE CONSUMIDOR ELETRÔNICA")
    c.line(15 * mm, height - 45 * mm, width - 15 * mm, height - 45 * mm)
    c.drawString(10 * mm, height - 50 * mm, "# CÓDIGO  DESCRIÇÃO                                                                   QTDE. UN.                                 VL.UNIT.                                        VL.TOTAL")
    c.setFont("Helvetica", 8)  # Voltando para a fonte normal
    y = height - 55 * mm
    item_number = 1  # Inicializando o contador de itens
    for item in nfe_info['itens']:
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
    c.drawString(10 * mm, y - 30 * mm, f"NFC-e nº {nfe_info['numero']} Série {nfe_info['serie']} {nfe_info['data_emissao']}")
    c.drawString(10 * mm, y - 40 * mm, f"Protocolo de autorização: {nfe_info['protocolo_autorizacao']}")
    c.drawString(10 * mm, y - 50 * mm, f"Data de Autorização: {nfe_info['data_autorizacao']}")
    c.setFont("Helvetica", 8)  # Voltando para a fonte normal
    c.drawString(10 * mm, y - 60 * mm, f"Valor a pagar R$: {nfe_info['valor_total']} - Descontos R$: {nfe_info['desconto']}")
    c.drawString(10 * mm, y - 70 * mm, f"Forma de pagamento: TEF - Valor pago R$: {nfe_info['valor_total']}")
    c.drawString(10 * mm, y - 80 * mm, f"CONSUMIDOR CPF: {nfe_info['cpf_consumidor']} - {nfe_info['consumidor']}")
    #c.drawString(10 * mm, y - 90 * mm, f"Informações Adicionais: {nfe_info['informacoes_adicionais']}")
    c.line(10 * mm, y - 10 * mm, width - 10 * mm, y - 10 * mm)
    c.drawString(10 * mm, 10 * mm, f"{nfe_info['informacoes_adicionais']}")
    c.drawString(10 * mm, y - 90 * mm, f"Consulte pela Chave de Acesso em https://sat.sef.sc.gov.br/nfce/consulta")
    c.setFont("Helvetica-Bold", 8)  # Mudando para negritoc.setFont
    c.drawString(10 * mm, y - 100 * mm, f"Chave de acesso: {nfe_info['chave_nfe']}")
    c.setFont("Helvetica", 8)  # Voltando para a fonte normal
    c.drawString(10 * mm, y - 110 * mm, "Tributos Totais Incidentes Lei Federal 12.741/2012 (0,00)")

    c.showPage()
    c.save()

# Caminho para o arquivo XML e o arquivo PDF de saída
xml_file = 'xml_nfe_teste.xml'
output_file = 'xml_danfe_nfe.pdf'

# Extraindo informações e gerando o PDF
nfe_info = extract_nfe_info(xml_file)
generate_danfe_pdf(nfe_info, output_file)

print(f"DANFE gerado com sucesso: {output_file}")
