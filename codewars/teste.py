import hashlib

print("Copyright ©2025 | Delean Mafra, todos os direitos reservados.")


def hash_password(password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    return hashed_password


# Exemplo
password = "12"
hashed_password = hash_password(password)
print("Hashed Password: ", hashed_password)
