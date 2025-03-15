from flask import Flask, render_template, request, jsonify
from delean_chess import Tabuleiro


app = Flask(__name__)
tabuleiro = Tabuleiro()

@app.route('/')
def index():
    estado = tabuleiro.get_estado_tabuleiro()
    return render_template('index.html', tabuleiro=estado, turno=tabuleiro.turno)

@app.route('/mover', methods=['POST'])
def mover():
    dados = request.json
    inicio = (dados['linha_inicio'], dados['coluna_inicio'])
    fim = (dados['linha_fim'], dados['coluna_fim'])
    sucesso = tabuleiro.mover_peca(inicio, fim)    
    estado = tabuleiro.get_estado_tabuleiro()
    return jsonify(sucesso=sucesso, tabuleiro=estado, turno=tabuleiro.turno)

if __name__ == '__main__':
    app.run(debug=True)