from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Random import get_random_bytes
import hashlib

# Função para gerar um par de chaves RSA
def generate_rsa_key_pair():
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return private_key, public_key

# Função para criptografia assimétrica usando RSA
def asymmetric_encrypt(data, public_key):
    recipient_key = RSA.import_key(public_key)
    cipher_rsa = PKCS1_OAEP.new(recipient_key)
    encrypted_data = cipher_rsa.encrypt(data)
    return encrypted_data

# Função para descriptografia assimétrica usando RSA
def asymmetric_decrypt(encrypted_data, private_key):
    private_key = RSA.import_key(private_key)
    cipher_rsa = PKCS1_OAEP.new(private_key)
    decrypted_data = cipher_rsa.decrypt(encrypted_data)
    return decrypted_data

# Função para gerar hash usando SHA-3
def generate_sha3_hash(data):
    sha3_256_hash = hashlib.sha3_256()
    sha3_256_hash.update(data)
    return sha3_256_hash.hexdigest()

# Exemplo de uso

# Gerando um par de chaves RSA
private_key, public_key = generate_rsa_key_pair()

# Dados a serem criptografados
data = "Dados sensíveis que precisam ser protegidos.".encode('utf-8')

# Criptografia assimétrica (RSA)
encrypted_data = asymmetric_encrypt(data, public_key)
print("Texto cifrado (RSA):", encrypted_data)

# Descriptografia assimétrica (RSA)
decrypted_data = asymmetric_decrypt(encrypted_data, private_key)
print("Texto decifrado (RSA):", decrypted_data)

# Gerar hash usando SHA-3
hash_value = generate_sha3_hash(data)
print("Hash (SHA-3):", hash_value)
