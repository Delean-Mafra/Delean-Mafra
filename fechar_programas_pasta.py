import os
import psutil

def fechar_programas_da_pasta(caminho_pasta):
    """
    Fecha quaisquer programas que estejam utilizando arquivos da pasta especificada.
    
    :param caminho_pasta: Caminho da pasta a ser monitorada.
    """
    caminho_pasta = os.path.abspath(caminho_pasta)

    for processo in psutil.process_iter(['pid', 'name', 'open_files']):
        try:
            # Verifica se o processo possui arquivos abertos
            arquivos_abertos = processo.info.get('open_files')
            if arquivos_abertos:
                for arquivo in arquivos_abertos:
                    if arquivo.path.startswith(caminho_pasta):
                        print(f"Encerrando processo {processo.info['name']} (PID: {processo.info['pid']}) que utiliza {arquivo.path}")
                        psutil.Process(processo.info['pid']).terminate()
                        break
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            # Ignorar processos que foram finalizados ou sem permissão para acessar
            pass

if __name__ == "__main__":
    # Substitua pelo caminho da pasta que deseja monitorar
    caminho_da_pasta = r"C:\Users\Acer\Downloads\pratica integradora de dados"
    fechar_programas_da_pasta(caminho_da_pasta)