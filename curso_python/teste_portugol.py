from pyportugol import escreva, enquanto,leianumerointeiro, diferente

class Valores:
    def __init__(self):
        self.soma = 0
        self.valordigitado = 0

valores = Valores()

escreva("Digite um valor para a soma: ")
valores.valordigitado = leianumerointeiro()

def atualizar():
    valores.soma += valores.valordigitado
    escreva(f"Total: {valores.soma}")
    escreva("Digite um valor para a soma: ")
    valores.valordigitado = leianumerointeiro()

# Correção aqui: invertemos a ordem dos argumentos e removemos os parênteses extras
enquanto(
    lambda: diferente(valores.valordigitado, 0),  # Agora passamos os dois argumentos corretamente
    atualizar
)

escreva(f"Resultado: {valores.soma}")