import hashlib

def calculate_checksum(data):

    sha256_hash = hashlib.sha256()
    sha256_hash.update(data.encode('utf-8'))
    return sha256_hash.hexdigest()

def verify_data_integrity(original_data, received_data):

    original_checksum = calculate_checksum(original_data)
    received_checksum = calculate_checksum(received_data)
    return original_checksum == received_checksum

original_data = "Exemplo de dados para transferência."
received_data = "Exemplo de dados para transferência."  # Simulando que os dados foram recebidos corretamente

original_checksum = calculate_checksum(original_data)
received_checksum = calculate_checksum(received_data)

print(f"Checksum original: {original_checksum}")
print(f"Checksum recebido: {received_checksum}")

# Verificando a integridade dos dados
if verify_data_integrity(original_data, received_data):
    print("A integridade dos dados foi mantida.")
else:
    print("Os dados foram corrompidos.")
