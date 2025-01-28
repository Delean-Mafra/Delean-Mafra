import os
import shutil

print("Copyright ©2025 | Delean Mafra, todos os direitos reservados.")


def deletar_arquivos_e_pastas(caminho):
    for nome in os.listdir(caminho):
        subcaminho = os.path.join(caminho, nome)
        try:
            if os.path.isdir(subcaminho):
                shutil.rmtree(subcaminho)
            else:
                os.remove(subcaminho)
        except PermissionError:
            print(f"Permissão negada para {subcaminho}. Continuando com o próximo.")

caminho = r"C:\Users\Acer\AppData\Local\Microsoft\Windows\INetCache\IE\KVGBJOP1"
deletar_arquivos_e_pastas(caminho)
