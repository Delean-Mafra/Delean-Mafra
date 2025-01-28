# assinatura_teste.py
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA1
from base64 import b64encode
#from datetime import datetime
#import re
print("Copyright ©2025 | Delean Mafra, todos os direitos reservados.")


# # with open(r'xml.txt', "r", encoding="utf-8") as f:
# #     nota_fiscal = f.read()

# # emissao_match = re.search(r"Emissão: (\d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2})", nota_fiscal)
# # if emissao_match:
# #     emissao_str = emissao_match.group(1)
# #     emissao_dt = datetime.strptime(emissao_str, "%d/%m/%Y %H:%M:%S")
# #     dhEmi = emissao_dt.strftime("%Y-%m-%dT%H:%M:%S-03:00")  # Formatação da data e hora para ISO 8601
# # else:
# #     raise ValueError("Data de emissão não encontrada na nota fiscal.")

# # arquivo_path = r"D:\Python\Python_projcts\templates\xml.txt"



# # def preencher_com_zeros(valor_c, total_digitos):
# #     return valor_c + '0' * (total_digitos - len(valor_c))

# # def calcular_dv(chave):
# #     multiplicadores = [2, 3, 4, 5, 6, 7, 8, 9] * 6  
# #     soma = 0
# #     for i in range(43):
# #         soma += int(chave[42 - i]) * multiplicadores[i]
# #     resto = soma % 11
# #     if resto < 2:
# #         return 0
# #     else:
# #         return 11 - resto

# # nNF = re.search(r"Número: (\d+)", nota_fiscal).group(1)
# # serie = re.search(r"Série: (\d+)", nota_fiscal).group(1)

# # cnpj = re.search(r"CNPJ: (\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2})", nota_fiscal).group(1).replace(".", "").replace("/", "").replace("-", "")

# # chave_de_acesso = re.search(r"Chave de acesso:\n((?:\d{4} ){10}\d{4})", nota_fiscal).group(1).replace(" ", "")

# # match = re.search(r"Chave de acesso:\n((?:\d{4} ){10}\d{4})", nota_fiscal)
# # if match is not None:
# #     chave_de_acesso = match.group(1).replace(" ", "")
# #     dv = chave_de_acesso[-1]
# # else:
# #     uf = '42'
# #     aamm = dhEmi[2:4] + dhEmi[5:7]
# #     mod = '65'
# #     numero = nNF
# #     fem = '10'
# #     digitos36 = str(uf) + str(aamm) + str(cnpj) + str(mod) + str(serie) + str(numero) + str(fem)
# #     digitos43 = preencher_com_zeros(digitos36, 43)
# #     dv = calcular_dv(digitos43)
# #     chave_de_acesso = str(digitos43) + str(dv)


# Função para gerar chave privada simulada
def generate_private_key():
    key = RSA.generate(2048)
    return key

# Função para gerar chave pública correspondente
def generate_public_key(private_key):
    return private_key.publickey()

# Função para gerar a assinatura digital
def generate_signature_value(xml_string, private_key):
    h = SHA1.new(xml_string.encode('utf-8'))
    signature = pkcs1_15.new(private_key).sign(h)
    return b64encode(signature).decode('utf-8')

# Função para gerar o certificado (chave pública em base64)
def generate_certificate(public_key):
    return b64encode(public_key.export_key()).decode('utf-8')

# Função principal para gerar o XML com assinatura
def create_xml_with_signature(chave_de_acesso):
    private_key = generate_private_key()
    public_key = generate_public_key(private_key)
    return private_key, public_key
