import random
import string
import tkinter as tk
from tkinter import ttk

class PasswordGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerador de Senha")
        
        # Variáveis de controle
        self.use_lowercase = tk.BooleanVar()
        self.use_uppercase = tk.BooleanVar()
        self.use_numbers = tk.BooleanVar()
        self.use_special = tk.BooleanVar()
        self.use_unique = tk.BooleanVar()
        self.password_length = tk.IntVar(value=12)
        
        # Criar widgets
        self.create_widgets()
        
    def create_widgets(self):
        # Checkboxes
        ttk.Checkbutton(self.root, text="Letras minúsculas", variable=self.use_lowercase).pack()
        ttk.Checkbutton(self.root, text="Letras maiúsculas", variable=self.use_uppercase).pack()
        ttk.Checkbutton(self.root, text="Números", variable=self.use_numbers).pack()
        ttk.Checkbutton(self.root, text="Caracteres especiais", variable=self.use_special).pack()
        ttk.Checkbutton(self.root, text="Caracteres únicos", variable=self.use_unique).pack()
        
        # Slider para comprimento
        ttk.Label(self.root, text="Comprimento da senha:").pack()
        length_scale = ttk.Scale(self.root, from_=4, to=30, variable=self.password_length, orient='horizontal')
        length_scale.pack()
        
        # Campo de resultado
        self.password_var = tk.StringVar()
        ttk.Label(self.root, textvariable=self.password_var).pack(pady=10)
        
        # Botão gerar
        ttk.Button(self.root, text="Gerar Senha", command=self.generate_password).pack(pady=10)
        
    def generate_password(self):
        lowercase_letters = 'abcdefghijklmnopqrstuvwxyz'
        uppercase_letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        numbers = '0123456789'
        special_characters = '!@#$%^&*()-_=+[{]}|;:",<.>/?'
        
        characters = ''
        if self.use_lowercase.get():
            characters += lowercase_letters
        if self.use_uppercase.get():
            characters += uppercase_letters
        if self.use_numbers.get():
            characters += numbers
        if self.use_special.get():
            characters += special_characters

        if characters == '':
            self.password_var.set('Selecione pelo menos uma opção de caracteres.')
            return

        password = ''
        used_characters = set()
        for i in range(self.password_length.get()):
            while True:
                character = random.choice(characters)
                if not self.use_unique.get() or character not in used_characters:
                    password += character
                    used_characters.add(character)
                    break
        
        self.password_var.set(password)

if __name__ == '__main__':
    root = tk.Tk()
    app = PasswordGenerator(root)
    root.mainloop()