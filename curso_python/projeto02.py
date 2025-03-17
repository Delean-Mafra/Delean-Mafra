import time
import pyautogui
import pyperclip
import webbrowser
from time import sleep
print("Copyright ©2025 | Delean Mafra, todos os direitos reservados.")

destinatario = input('Digite um e-mail: ')
assunto = "Aula Python"
mensagem = """
import time
import pyautogui
import pyperclip
import webbrowser
from time import sleep


destinatario = input('Digite um e-mail: ')
assunto = "Análises Projeto 2024"
mensagem = f""
Bom dia,

Seja bem vindo.
Seu usuario de acesso é o {destinatario}
""

pyautogui.PAUSE = 3

# abrir o navegador no gmail
webbrowser.open("https://mail.google.com/mail/u/0/#inbox?compose=new")

time.sleep(10)

# clicar no botão "Escrever"
# pyautogui.click(x=2503, y=314)

# Preencher Para
pyperclip.copy(destinatario)
pyautogui.hotkey("ctrl", "v")
pyautogui.hotkey("tab")

# Preencher Assunto
pyperclip.copy(assunto)
pyautogui.hotkey("ctrl", "v")
pyautogui.hotkey("tab")

# Preencher corpo do e-mail
pyperclip.copy(mensagem)
pyautogui.hotkey("ctrl", "v")

# Clicar no botão enviar
#pyautogui.click(x=2503, y=314)
time.sleep(5)

pyautogui.hotkey("ctrl", "enter")

# fechar a aba
pyautogui.hotkey("ctrl", "f4")

print("E-mail enviado com sucesso!")
"""

pyautogui.PAUSE = 3

# abrir o navegador no gmail
webbrowser.open("https://mail.google.com/mail/u/0/#inbox?compose=new")

time.sleep(10)

# clicar no botão "Escrever"
# pyautogui.click(x=2503, y=314)

# Preencher Para
pyperclip.copy(destinatario)
pyautogui.hotkey("ctrl", "v")
pyautogui.hotkey("tab")

# Preencher Assunto
pyperclip.copy(assunto)
pyautogui.hotkey("ctrl", "v")
pyautogui.hotkey("tab")

# Preencher corpo do e-mail
pyperclip.copy(mensagem)
pyautogui.hotkey("ctrl", "v")

# Clicar no botão enviar
#pyautogui.click(x=2503, y=314)
time.sleep(5)

pyautogui.hotkey("ctrl", "enter")

# fechar a aba
pyautogui.hotkey("ctrl", "f4")

print("E-mail enviado com sucesso!")
