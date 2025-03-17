# Funções de comparação
def diferente(a, b):
    """Verifica se 'a' é diferente de 'b'"""
    return a != b

def escreva(*args):
    print(*args)
    
def falso():
    return False

def verdadeiro():
    return True

def leia(mensagem=""):
    return input(mensagem)  # Retorna a entrada como string

def leianumerointeiro(mensagem=""):
    return int(input(mensagem)) # Retorna a entrada como inteiro

def leianumeroreal(mensagem=""):
    return float(input(mensagem)) # Retorna a entrada como real

def enquanto(condicao, bloco):
    while condicao():
        bloco()