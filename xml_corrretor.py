import xml.etree.ElementTree as ET

print("Copyright ©2025 | Delean Mafra, todos os direitos reservados.")


# Função para ler o XML e retornar a árvore e a raiz
def read_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    return tree, root

# Função para calcular a soma dos descontos dos itens
def calculate_total_item_discount(root, ns):
    total_item_discount = 0.0
    for item in root.findall('.//deleanmafra:det/deleanmafra:prod/deleanmafra:vDesc', ns):
        total_item_discount += float(item.text)
    return total_item_discount

# Função para redistribuir o desconto total entre os itens
def redistribute_discount(root, total_discount, ns):
    items = root.findall('.//deleanmafra:det/deleanmafra:prod/deleanmafra:vDesc', ns)
    num_items = len(items)
    new_discount = round(total_discount / num_items, 2)
    total_new_discount = new_discount * num_items
    difference = round(total_discount - total_new_discount, 2)

    for i, item in enumerate(items):
        if i == num_items - 1:  # Último item
            item.text = f'{new_discount + difference:.2f}'
        else:
            item.text = f'{new_discount:.2f}'

# Função para remover namespaces
def remove_namespace(tree):
    for elem in tree.iter():
        if '}' in elem.tag:
            elem.tag = elem.tag.split('}', 1)[1]
        elem.attrib = {key.split('}', 1)[-1]: value for key, value in elem.attrib.items()}

# Função principal
def main():
    file_path = r'\teste.xml'  # Substitua pelo caminho do seu arquivo XML
    tree, root = read_xml(file_path)

    ns = {'deleanmafra': 'http://www.portalfiscal.inf.br/deleanmafra'}
    total_discount = float(root.find('.//deleanmafra:total/deleanmafra:ICMSTot/deleanmafra:vDesc', ns).text)
    total_item_discount = calculate_total_item_discount(root, ns)

    if total_discount != total_item_discount:
        redistribute_discount(root, total_discount, ns)
        remove_namespace(tree)
        tree.write('xml_deleanmafra_teste_corrigido.xml', encoding='utf-8', xml_declaration=True)  # Salva o XML corrigido

if __name__ == '__main__':
    main()
