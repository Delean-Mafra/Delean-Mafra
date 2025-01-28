from flask import Flask, request, jsonify, render_template
import json
import os
from valida_cpf import isCpfValid

print("Copyright ©2025 | Delean Mafra, todos os direitos reservados.")

app = Flask(__name__)

# Caminho base do projeto
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Caminhos absolutos dos arquivos JSON
VOTOS_FILE = os.path.join(BASE_DIR, r'\1.json')
CPFS_FILE = os.path.join(BASE_DIR, r'\2.json')

def ler_json(arquivo):
    if not os.path.exists(arquivo):
        # Se o arquivo não existir, cria ele com uma lista vazia
        salvar_json(arquivo, [])
        return []
    with open(arquivo, 'r', encoding='utf-8') as f:
        return json.load(f)

def salvar_json(arquivo, dados):
    os.makedirs(os.path.dirname(arquivo), exist_ok=True)
    with open(arquivo, 'w', encoding='utf-8') as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/votacao', methods=['POST'])
def votacao():
    cpf = request.form['cpf']
    
    # Valida o CPF
    if not isCpfValid(cpf):
        return jsonify({'status': 'error', 'message': 'CPF inválido!'}), 400
    
    # Se for apenas validação do CPF
    if 'validacao' in request.form:
        cpfs = ler_json(CPFS_FILE)
        if cpf in cpfs:
            return jsonify({'status': 'error', 'message': 'Este CPF já votou!'}), 400
        return jsonify({'status': 'success', 'message': 'CPF válido!'}), 200
    
    # Se for registro de voto
    candidato = request.form['candidato']
    
    # Carrega os votos existentes
    votos = ler_json(VOTOS_FILE)
    
    # Procura o candidato na lista de votos
    candidato_encontrado = False
    for v in votos:
        if v['Numero'] == candidato:
            v['Total de votos'] += 1
            candidato_encontrado = True
            break
    
    # Se não encontrou o candidato, cria um novo registro
    if not candidato_encontrado:
        nome_candidato = {
            '00': 'Nulo/Em branco',
            '22': 'D',
            '17': 'J',
            '13': 'L',
            '15': 'P'
        }.get(candidato, 'Nulo/Em branco')
        
        votos.append({
            'Candidato': nome_candidato,
            'Numero': candidato,
            'Total de votos': 1
        })
    
    # Salva os votos atualizados
    salvar_json(VOTOS_FILE, votos)
    
    # Salva o CPF na lista de votantes
    cpfs = ler_json(CPFS_FILE)
    cpfs.append(cpf)
    salvar_json(CPFS_FILE, cpfs)
    
    return jsonify({'status': 'success', 'message': 'Voto registrado com sucesso!'}), 200

if __name__ == '__main__':
    # Use a variável de ambiente FLASK_DEBUG para controlar o modo debug
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() in ['true', '1', 't']
    app.run(debug=debug_mode)
