from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
import base64

print("Copyright ©2025 | Delean Mafra, todos os direitos reservados.")

def carregar_chave_publica():
    """
    Carrega a chave pública gerada, geralmente a chave pública correspondente à chave privada usada para assinar.
    :return: Chave pública carregada.
    """
    # A chave pública em Base64 (sem os delimitadores PEM)
    # Removidas as quebras de linha (\n) do meio da string
    public_key_base64 = (
        "SUA CHAVE MD5-1"
        "SUA CHAVE MD5-2"
        "SUA CHAVE MD5-3"
        "SUA CHAVE MD5-4"
        "SUA CHAVE MD5-6"
        "SUA CHAVE MD5-7"
        "SUA CHAVE MD5-8"
    )

    # Remover possíveis espaços em branco e juntar a string
    public_key_base64 = ''.join(public_key_base64.split())
    
    # Formatar a chave pública como PEM
    # Adicionar quebras de linha a cada 64 caracteres
    chunks = [public_key_base64[i:i+64] for i in range(0, len(public_key_base64), 64)]
    formatted_key = '\n'.join(chunks)
    
    public_key_pem = f"-----BEGIN PUBLIC KEY-----\n{formatted_key}\n-----END PUBLIC KEY-----"
    
    try:
        # Carregar chave pública do formato PEM
        public_key = serialization.load_pem_public_key(
            public_key_pem.encode('utf-8'),
            backend=default_backend()
        )
        return public_key
    except ValueError as e:
        print(f"Erro ao carregar a chave pública: {e}")
        print("Chave PEM formatada:")
        print(public_key_pem)
        raise

def validar_assinatura(mensagem_original, assinatura_base64, chave_publica):
    """
    Valida a assinatura de uma mensagem usando a chave pública.
    :param mensagem_original: Mensagem original que foi assinada (string).
    :param assinatura_base64: Assinatura digital em Base64.
    :param chave_publica: Chave pública para validar a assinatura.
    :return: True se a assinatura for válida, False caso contrário.
    """
    try:
        # Converter a assinatura de Base64 para bytes
        assinatura_bytes = base64.b64decode(assinatura_base64)

        # Converter a mensagem para bytes
        mensagem_bytes = mensagem_original.encode('utf-8')

        # Validar a assinatura utilizando a chave pública
        chave_publica.verify(
            assinatura_bytes,
            mensagem_bytes,
            padding.PKCS1v15(),
            hashes.SHA256()
        )
        return True  # Assinatura válida
    except Exception as e:
        print(f"Erro na verificação da assinatura: {e}")
        return False  # Assinatura inválida

# Exemplo de uso:
if __name__ == "__main__":
    # Exemplo de mensagem original que foi assinada
    mensagem_original = "Este é o conteúdo da NF-e a ser assinado."

    # Exemplo de assinatura Base64 (substitua com a assinatura real que você gerou)
    assinatura_base64 = "SUA CHAVE DE ASSINATURA CONTENDO APROXIMADAMENTE 345 CARACTERES"
    try:
        # Carregar a chave pública
        chave_publica = carregar_chave_publica()

        # Validar a assinatura
        if validar_assinatura(mensagem_original, assinatura_base64, chave_publica):
            print("A assinatura é válida!")
        else:
            print("A assinatura é inválida!")
    except Exception as e:
        print(f"Erro durante a execução: {e}")
