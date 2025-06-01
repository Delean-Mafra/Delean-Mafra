import os
import psutil
from flask import Flask, render_template, request, jsonify, redirect, url_for

app = Flask(__name__)

def fechar_programas_da_pasta(caminho_pasta):
    """
    Fecha quaisquer programas que estejam utilizando arquivos da pasta especificada.
    
    :param caminho_pasta: Caminho da pasta a ser monitorada.
    :return: Lista de processos encerrados
    """
    caminho_pasta = os.path.abspath(caminho_pasta)
    processos_encerrados = []

    for processo in psutil.process_iter(['pid', 'name', 'open_files']):
        try:
            # Verifica se o processo possui arquivos abertos
            arquivos_abertos = processo.info.get('open_files')
            if arquivos_abertos:
                for arquivo in arquivos_abertos:
                    if arquivo.path.startswith(caminho_pasta):
                        processo_info = {
                            'name': processo.info['name'],
                            'pid': processo.info['pid'],
                            'path': arquivo.path
                        }
                        processos_encerrados.append(processo_info)
                        psutil.Process(processo.info['pid']).terminate()
                        break
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            # Ignorar processos que foram finalizados ou sem permissão para acessar
            pass
    
    return processos_encerrados

def listar_processos_da_pasta(caminho_pasta):
    """
    Lista processos que estão utilizando arquivos da pasta especificada.
    
    :param caminho_pasta: Caminho da pasta a ser monitorada.
    :return: Lista de processos encontrados
    """
    caminho_pasta = os.path.abspath(caminho_pasta)
    processos_encontrados = []

    for processo in psutil.process_iter(['pid', 'name', 'open_files']):
        try:
            arquivos_abertos = processo.info.get('open_files')
            if arquivos_abertos:
                for arquivo in arquivos_abertos:
                    if arquivo.path.startswith(caminho_pasta):
                        processo_info = {
                            'name': processo.info['name'],
                            'pid': processo.info['pid'],
                            'path': arquivo.path
                        }
                        processos_encontrados.append(processo_info)
                        break
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    
    return processos_encontrados

@app.route('/')
def index():
    return render_template('fechar_programas_pasta.html')

@app.route('/verificar', methods=['POST'])
def verificar_processos():
    caminho_pasta = request.form.get('caminho_pasta')
    if not caminho_pasta:
        return jsonify({'error': 'Caminho da pasta é obrigatório'}), 400
    
    if not os.path.exists(caminho_pasta):
        return jsonify({'error': 'Caminho da pasta não existe'}), 400
    
    processos = listar_processos_da_pasta(caminho_pasta)
    return jsonify({'processos': processos})

@app.route('/fechar', methods=['POST'])
def fechar_processos():
    caminho_pasta = request.form.get('caminho_pasta')
    if not caminho_pasta:
        return jsonify({'error': 'Caminho da pasta é obrigatório'}), 400
    
    if not os.path.exists(caminho_pasta):
        return jsonify({'error': 'Caminho da pasta não existe'}), 400
    
    processos_encerrados = fechar_programas_da_pasta(caminho_pasta)
    return jsonify({'processos_encerrados': processos_encerrados})

if __name__ == "__main__":
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() in ['true', '1', 't']
    app.run(debug=debug_mode, host='127.0.0.1', port=5000)