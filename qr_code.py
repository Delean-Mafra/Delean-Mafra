import qrcode

def generate_qr_code(url, file_name):
    # Cria uma instância de QR code
    qr = qrcode.QRCode(  # Corrigido aqui
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )

    # Adiciona dados ao QR code
    qr.add_data(url)
    qr.make(fit=True)

    # Cria uma imagem a partir da instância de QR code
    img = qr.make_image()

    # Salva o QR code como um arquivo de imagem
    img.save(file_name)

# Exemplo de uso
url = input('Informe o link: ')
file_name = r"D:\Python\Python_projcts\templates\qrcode.png"
generate_qr_code(url, file_name)

print(f"O QR code para {url} foi salvo com sucesso em {file_name}.")
