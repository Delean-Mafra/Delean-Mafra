from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
import base64

print("Copyright ©2025 | Delean Mafra, todos os direitos reservados.")


def gerar_chaves():
    """
    Gera um par de chaves RSA (privada e pública).
    :return: Chave privada e chave pública
    """
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )

    public_key = private_key.public_key()

    return private_key, public_key

def assinar_mensagem(mensagem, private_key):
    """
    Assina uma mensagem usando a chave privada.
    :param mensagem: Mensagem a ser assinada (string).
    :param private_key: Chave privada para assinar.
    :return: Assinatura em base64
    """
    # Codificar a mensagem em bytes (a assinatura exige bytes, não string)
    mensagem_bytes = mensagem.encode('utf-8')

    # Assinar a mensagem com a chave privada usando PKCS1v15 e SHA256
    assinatura = private_key.sign(
        mensagem_bytes,
        padding.PKCS1v15(),
        hashes.SHA256()
    )

    # Codificar a assinatura em Base64 para exibição
    return base64.b64encode(assinatura).decode('utf-8')

def gerar_assinatura(mensagem):
    """
    Função que gera a assinatura digital para ser exportada.
    :param mensagem: Mensagem que será assinada.
    :return: Assinatura em Base64.
    """
    # Gerar par de chaves (privada e pública)
    private_key, public_key = gerar_chaves()

    # Assinar a mensagem
    assinatura_base64 = assinar_mensagem(mensagem, private_key)
    
    return assinatura_base64

# Função principal, chamada quando o script for executado diretamente
if __name__ == "__main__":
    # Exemplo de uso - Aqui você pode passar a mensagem diretamente
    # ou você pode carregar de um arquivo de texto, como demonstrado abaixo
    
    arquivo_path = r"\xml.txt"  # Caminho do seu arquivo de texto
    
    # Ler o conteúdo do arquivo de texto
    with open(arquivo_path, "r", encoding="utf-8") as file:
        conteudo_arquivo = file.read()

    # Gerar a assinatura para o conteúdo lido
    assinatura = gerar_assinatura(conteudo_arquivo)
    
    # Exibir a assinatura gerada em Base64
    print("Assinatura gerada (Base64):", assinatura)
 
