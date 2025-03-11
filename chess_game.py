from flask import Flask, render_template, request, jsonify
print('Copyright © Delean Mafra, todos os direitos reservados | All rights reserved.')
app = Flask(__name__)
class Peca:
    def __init__(self, cor):
        self.cor = cor        
    def __repr__(self):
        return f"{self.__class__.__name__[0]}_{self.cor[0]}"
    def movimentos_validos(self, tabuleiro, linha, coluna):
        raise NotImplementedError()
class Peao(Peca):
    def movimentos_validos(self, tabuleiro, linha, coluna):
        movimentos = []
        if self.cor == 'branca':
            if linha > 0 and tabuleiro[linha - 1][coluna] is None:
                movimentos.append((linha - 1, coluna))
            if linha == 6 and tabuleiro[linha - 2][coluna] is None and tabuleiro[linha - 1][coluna] is None:
                movimentos.append((linha - 2, coluna))
            # Capturas diagonais
            for dc in [-1, 1]:
                if 0 <= linha - 1 < 8 and 0 <= coluna + dc < 8:
                    if tabuleiro[linha - 1][coluna + dc] and tabuleiro[linha - 1][coluna + dc].cor != self.cor:
                        movimentos.append((linha - 1, coluna + dc))
        else:
            if linha < 7 and tabuleiro[linha + 1][coluna] is None:
                movimentos.append((linha + 1, coluna))
            if linha == 1 and tabuleiro[linha + 2][coluna] is None and tabuleiro[linha + 1][coluna] is None:
                movimentos.append((linha + 2, coluna))
            for dc in [-1, 1]:
                if 0 <= linha + 1 < 8 and 0 <= coluna + dc < 8:
                    if tabuleiro[linha + 1][coluna + dc] and tabuleiro[linha + 1][coluna + dc].cor != self.cor:
                        movimentos.append((linha + 1, coluna + dc))
        return movimentos
class Torre(Peca):
    def movimentos_validos(self, tabuleiro, linha, coluna):
        movimentos = []
        direcoes = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dl, dc in direcoes:
            l, c = linha + dl, coluna + dc
            while 0 <= l < 8 and 0 <= c < 8:
                if tabuleiro[l][c] is None:
                    movimentos.append((l, c))
                elif tabuleiro[l][c].cor != self.cor:
                    movimentos.append((l, c))
                    break
                else:
                    break
                l += dl
                c += dc
        return movimentos
class Cavalo(Peca):
    def movimentos_validos(self, tabuleiro, linha, coluna):
        movimentos = []
        direcoes = [(-2, -1), (-2, 1), (2, -1), (2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2)]
        for dl, dc in direcoes:
            l, c = linha + dl, coluna + dc
            if 0 <= l < 8 and 0 <= c < 8:
                if tabuleiro[l][c] is None or tabuleiro[l][c].cor != self.cor:
                    movimentos.append((l, c))
        return movimentos
class Bispo(Peca):
    def movimentos_validos(self, tabuleiro, linha, coluna):
        movimentos = []
        direcoes = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dl, dc in direcoes:
            l, c = linha + dl, coluna + dc
            while 0 <= l < 8 and 0 <= c < 8:
                if tabuleiro[l][c] is None:
                    movimentos.append((l, c))
                elif tabuleiro[l][c].cor != self.cor:
                    movimentos.append((l, c))
                    break
                else:
                    break
                l += dl
                c += dc
        return movimentos
class Rainha(Peca):
    def movimentos_validos(self, tabuleiro, linha, coluna):
        movimentos = []
        direcoes_torre = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dl, dc in direcoes_torre:
            l, c = linha + dl, coluna + dc
            while 0 <= l < 8 and 0 <= c < 8:
                if tabuleiro[l][c] is None:
                    movimentos.append((l, c))
                elif tabuleiro[l][c].cor != self.cor:
                    movimentos.append((l, c))
                    break
                else:
                    break
                l += dl
                c += dc        
        direcoes_bispo = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dl, dc in direcoes_bispo:
            l, c = linha + dl, coluna + dc
            while 0 <= l < 8 and 0 <= c < 8:
                if tabuleiro[l][c] is None:
                    movimentos.append((l, c))
                elif tabuleiro[l][c].cor != self.cor:
                    movimentos.append((l, c))
                    break
                else:
                    break
                l += dl
                c += dc        
        return movimentos
class Rei(Peca):
    def movimentos_validos(self, tabuleiro, linha, coluna):
        movimentos = []
        direcoes = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for dl, dc in direcoes:
            l, c = linha + dl, coluna + dc
            if 0 <= l < 8 and 0 <= c < 8:
                if tabuleiro[l][c] is None or tabuleiro[l][c].cor != self.cor:
                    movimentos.append((l, c))
        return movimentos
class Tabuleiro:
    def __init__(self):
        self.tabuleiro = [[None for _ in range(8)] for _ in range(8)]
        self.configurar_tabuleiro()
        self.turno = 'branca'  # Começa com as peças brancas
    def configurar_tabuleiro(self):
        for i in range(8):
            self.tabuleiro[1][i] = Peao('preta')
            self.tabuleiro[6][i] = Peao('branca')
        self.tabuleiro[0][0] = self.tabuleiro[0][7] = Torre('preta')
        self.tabuleiro[7][0] = self.tabuleiro[7][7] = Torre('branca')
        self.tabuleiro[0][1] = self.tabuleiro[0][6] = Cavalo('preta')
        self.tabuleiro[7][1] = self.tabuleiro[7][6] = Cavalo('branca')
        self.tabuleiro[0][2] = self.tabuleiro[0][5] = Bispo('preta')
        self.tabuleiro[7][2] = self.tabuleiro[7][5] = Bispo('branca')
        self.tabuleiro[0][3] = Rainha('preta')
        self.tabuleiro[7][3] = Rainha('branca')
        self.tabuleiro[0][4] = Rei('preta')
        self.tabuleiro[7][4] = Rei('branca')
    def mover_peca(self, inicio, fim):
        linha_inicio, coluna_inicio = inicio
        linha_fim, coluna_fim = fim
        peca = self.tabuleiro[linha_inicio][coluna_inicio]        
        if not peca:
            return False
        if peca.cor != self.turno:
            return False            
        if (linha_fim, coluna_fim) in peca.movimentos_validos(self.tabuleiro, linha_inicio, coluna_inicio):
            self.tabuleiro[linha_fim][coluna_fim] = peca
            self.tabuleiro[linha_inicio][coluna_inicio] = None            
            self.turno = 'preta' if self.turno == 'branca' else 'branca'
            return True
        return False
    def peca_para_unicode(self, peca):
        if not peca:
            return " "        
        simbolos = {
            'P_b': '♙', 'T_b': '♖', 'C_b': '♘', 'B_b': '♗', 'R_b': '♔', 'Q_b': '♕',
            'P_p': '♟', 'T_p': '♜', 'C_p': '♞', 'B_p': '♝', 'R_p': '♚', 'Q_p': '♛'
        }        
        return simbolos.get(str(peca), "?")        
    def get_estado_tabuleiro(self):
        return [[self.peca_para_unicode(self.tabuleiro[i][j]) for j in range(8)] for i in range(8)]
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
@app.route('/templates/index.html')
def template_index():
    return render_template('index.html', tabuleiro=tabuleiro.get_estado_tabuleiro(), turno=tabuleiro.turno)
if __name__ == '__main__':
    app.run(debug=True)