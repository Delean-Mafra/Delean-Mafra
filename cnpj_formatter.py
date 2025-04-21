import pyperclip
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label

def format_cnpj(cnpj):
    # Formata o CNPJ no padrão XX.XXX.XXX/XXXX-XX
    if len(cnpj) == 14 and cnpj.isdigit():
        return f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}"
    return "CNPJ inválido!"

class CNPJApp(App):
    def build(self):
        # Layout principal
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Campo de entrada para o CNPJ
        self.input_cnpj = TextInput(hint_text="Digite o CNPJ (somente números)", multiline=False, input_filter="int")
        self.layout.add_widget(self.input_cnpj)
        
        # Botão para formatar o CNPJ
        self.btn_format = Button(text="Formatar e Copiar CNPJ", size_hint=(1, 0.5))
        self.btn_format.bind(on_press=self.format_and_copy_cnpj)
        self.layout.add_widget(self.btn_format)
        
        # Label para exibir o resultado
        self.result_label = Label(text="")
        self.layout.add_widget(self.result_label)
        
        return self.layout

    def format_and_copy_cnpj(self, instance):
        # Obtém o CNPJ do campo de entrada e formata
        cnpj = self.input_cnpj.text
        formatted_cnpj = format_cnpj(cnpj)
        
        # Atualiza o texto no rótulo
        self.result_label.text = f"CNPJ formatado: {formatted_cnpj}"
        
        # Copia o CNPJ formatado para a área de transferência, se válido
        if "inválido" not in formatted_cnpj:
            pyperclip.copy(formatted_cnpj)
            self.result_label.text += " (copiado para a área de transferência)"

# Executa o aplicativo
if __name__ == "__main__":
    CNPJApp().run()
