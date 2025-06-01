import random
import string
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

class PasswordGenerator:
    def __init__(self):
        self.lowercase_letters = 'abcdefghijklmnopqrstuvwxyz'
        self.uppercase_letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.numbers = '0123456789'
        self.special_characters = '!@#$%^&*()-_=+[{]}|;:",<.>/?'
        
    def generate_password(self, length, use_lowercase, use_uppercase, use_numbers, use_special, use_unique):
        characters = ''
        
        if use_lowercase:
            characters += self.lowercase_letters
        if use_uppercase:
            characters += self.uppercase_letters
        if use_numbers:
            characters += self.numbers
        if use_special:
            characters += self.special_characters

        if characters == '':
            return {'error': 'Selecione pelo menos uma opção de caracteres.'}

        if use_unique and len(characters) < length:
            return {'error': f'Não há caracteres únicos suficientes. Máximo possível: {len(characters)}'}

        password = ''
        used_characters = set()
        
        for i in range(length):
            attempts = 0
            while True:
                character = random.choice(characters)
                if not use_unique or character not in used_characters:
                    password += character
                    used_characters.add(character)
                    break
                attempts += 1
                if attempts > 1000:  # Evitar loop infinito
                    return {'error': 'Erro ao gerar senha com caracteres únicos.'}
        
        return {'password': password}

generator = PasswordGenerator()

@app.route('/')
def index():
    return render_template('gerador_senha.html')

@app.route('/gerar_senha', methods=['POST'])
def gerar_senha():
    try:
        data = request.get_json()
        
        length = int(data.get('length', 12))
        use_lowercase = data.get('use_lowercase', False)
        use_uppercase = data.get('use_uppercase', False)
        use_numbers = data.get('use_numbers', False)
        use_special = data.get('use_special', False)
        use_unique = data.get('use_unique', False)
        
        if length < 4 or length > 30:
            return jsonify({'error': 'Comprimento deve estar entre 4 e 30 caracteres.'})
        
        result = generator.generate_password(length, use_lowercase, use_uppercase, use_numbers, use_special, use_unique)
        return jsonify(result)
        
    except Exception as e:
        import logging
        logging.error(f"Erro ao gerar senha: {str(e)}")
        return jsonify({'error': 'Ocorreu um erro interno ao gerar a senha. Por favor, tente novamente mais tarde.'})

if __name__ == '__main__':
    import os
    debug_mode = os.getenv('FLASK_DEBUG', 'false').lower() == 'true'
    app.run(debug=debug_mode, host='127.0.0.1', port=5000)