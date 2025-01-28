import re
import pandas as pd

print("Copyright ©2025 | Delean Mafra, todos os direitos reservados.")

def parse_nfce_txt(file_path):
    # 
    # Analisa o arquivo de texto de uma Nota Fiscal de Consumidor Eletrônica (NFC-e)
    # e extrai os itens da compra.
    
    # Args:
    #     file_path (str): Caminho completo para o arquivo de texto
    
    # Returns:
    #     pandas.DataFrame: DataFrame com os produtos processados


    # Lista para armazenar os produtos
    produtos = []
    
    # Abre e lê o arquivo
    with open(file_path, 'r', encoding='utf-8') as file:
        texto = file.read()
    
    # Padrão de regex para capturar as informações dos produtos
    padrao = r'(.*?)\s*\(Código:\s*(\d+)\s*\)\s*Qtde.:(\d+(?:,\d+)?)\s*UN:\s*(\w+)\s*Vl\. Unit\.:\s*([\d,]+)\s*Vl\. Total\s*([\d,]+)'
    
    # Encontra todos os produtos no texto
    matches = re.findall(padrao, texto)
    
    # Processa cada produto encontrado
    for match in matches:
        nome_produto, codigo, quantidade, un, vl_unitario, vl_total = match
        
        # Converte valores para o formato correto
        quantidade = float(quantidade.replace(',', '.'))
        vl_unitario = float(vl_unitario.replace(',', '.'))
        vl_total = float(vl_total.replace(',', '.'))
        
        # Adiciona o produto à lista
        produtos.append({
            'PRODUTO': nome_produto.strip(),
            'Codigo': codigo,
            'QTD': quantidade,
            'UN': un,
            'Vl. Unit': vl_unitario,
            'Vl. Total': vl_total
        })
    
    # Cria o DataFrame
    df = pd.DataFrame(produtos)
    
    return df

def salvar_arquivo(df, caminho_original, formato='xlsx'):
    # 
    # Salva o DataFrame como um arquivo Excel ou CSV no mesmo diretório do arquivo original.
    
    # Args:
    #     df (pandas.DataFrame): DataFrame a ser salvo
    #     caminho_original (str): Caminho do arquivo de texto original
    #     formato (str): Formato do arquivo de saída ('xlsx' ou 'csv')
    
    # Cria o caminho para o arquivo de saída
    caminho_saida = caminho_original.replace('.txt', f'.{formato}')
    
    # Salva o DataFrame sem o cabeçalho
    if formato == 'xlsx':
        df.to_excel(caminho_saida, index=False, header=False)
    else:
        df.to_csv(caminho_saida, index=False, header=False, encoding='utf-8')
    
    print(f"Arquivo {formato.upper()} salvo em: {caminho_saida}")

def main():
    # Caminho do arquivo de texto
    caminho_arquivo = r"\xml.txt"
    
    try:
        # Converte o texto para DataFrame
        df_produtos = parse_nfce_txt(caminho_arquivo)
        
        # Tenta salvar como XLSX primeiro
        try:
            salvar_arquivo(df_produtos, caminho_arquivo, 'xlsx')
        except Exception as e:
            print(f"Erro ao salvar XLSX: {e}")
            print("Tentando salvar como CSV...")
            salvar_arquivo(df_produtos, caminho_arquivo, 'csv')
        
        # Mostra o DataFrame (opcional, para verificação)
        print("\nProdutos processados:")
        print(df_produtos)
        
        # Informações adicionais
        print(f"\nTotal de itens: {len(df_produtos)}")
        print(f"Valor total: R$ {df_produtos['Vl. Total'].sum():.2f}")
    
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

if __name__ == "__main__":
    main()
