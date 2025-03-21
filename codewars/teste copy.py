print("Copyright ©2025 | Delean Mafra, todos os direitos reservados.")



# Dicionário de exemplo para representar caracteres em Braille
braille = {
    'a': '100000',
    'b': '101000',
    'c': '110000',
    'd': '110100',
    'e': '100100',
    'f': '111000',
    'g': '111100',
    'h': '101100',
    'i': '011000',
    'j': '011100',
    # Adicione mais caracteres conforme necessário...
}

def hamming_braille(s1, s2):
    # Função auxiliar para converter uma string para sua representação em Braille
    def to_braille(s):
        # Substitui palavras ligadas por suas representações em Braille
        words = s.split()
        for i, word in enumerate(words):
            if word in braille:
                words[i] = braille[word]
            else:
                words[i] = ''.join(braille.get(char, ' ') for char in word)
        return ' '.join(words)

    
    # Converte as strings para suas representações em Braille
    braille_s1 = to_braille(s1)
    braille_s2 = to_braille(s2)
    
    # Verifica se as duas strings têm o mesmo comprimento
    if len(braille_s1) != len(braille_s2):
        return -1  # Indica que a distância de Hamming não pode ser calculada
    
    # Calcula a distância de Hamming entre cada par de caracteres em Braille
    distance = 0
    for b1, b2 in zip(braille_s1, braille_s2):
        # Converte os caracteres para strings de bits
        bits1 = format(ord(b1), 'b').zfill(6)
        bits2 = format(ord(b2), 'b').zfill(6)
        # Adiciona a distância de Hamming entre os pares de bits à distância total
        distance += sum(bit1 != bit2 for bit1, bit2 in zip(bits1, bits2))
    




    # Adicione mais condições conforme necessário...
    
    return distance
