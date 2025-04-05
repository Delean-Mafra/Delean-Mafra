from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Random import get_random_bytes
import hashlib

# Função para criptografia simétrica usando AES
def symmetric_encrypt(data, key):
    cipher = AES.new(key, AES.MODE_EAX)
    nonce = cipher.nonce
    ciphertext, tag = cipher.encrypt_and_digest(data)
    return nonce, ciphertext, tag

# Função para descriptografia simétrica usando AES
def symmetric_decrypt(nonce, ciphertext, tag, key):
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    data = cipher.decrypt_and_verify(ciphertext, tag)
    return data

# Função para criptografia assimétrica usando RSA
def asymmetric_encrypt(data, public_key):
    cipher = PKCS1_OAEP.new(public_key)
    ciphertext = cipher.encrypt(data)
    return ciphertext

# Função para descriptografia assimétrica usando RSA
def asymmetric_decrypt(ciphertext, private_key):
    cipher = PKCS1_OAEP.new(private_key)
    data = cipher.decrypt(ciphertext)
    return data

# Função para gerar hash usando SHA-256
def generate_hash(data):
    sha256_hash = hashlib.sha256()
    sha256_hash.update(data)
    return sha256_hash.hexdigest()

# Exemplo de uso

# Dados a serem criptografados
data = "Dados sensíveis que precisam ser protegidos.".encode()

# Criptografia simétrica (AES)
symmetric_key = get_random_bytes(16)  # Chave de 128 bits
nonce, ciphertext, tag = symmetric_encrypt(data, symmetric_key)
print("Texto cifrado (AES):", ciphertext)

# Descriptografia simétrica (AES)
decrypted_data = symmetric_decrypt(nonce, ciphertext, tag, symmetric_key)
print("Texto decifrado (AES):", decrypted_data)

# Criptografia assimétrica (RSA)
key_pair = RSA.generate(2048)
public_key = key_pair.publickey()
private_key = key_pair

ciphertext_rsa = asymmetric_encrypt(data, public_key)
print("Texto cifrado (RSA):", ciphertext_rsa)

# Descriptografia assimétrica (RSA)
decrypted_data_rsa = asymmetric_decrypt(ciphertext_rsa, private_key)
print("Texto decifrado (RSA):", decrypted_data_rsa)

# Gerar hash usando SHA-256
hash_value = generate_hash(data)
print("Hash (SHA-256):", hash_value)
