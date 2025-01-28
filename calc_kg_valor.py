import os
os.environ['KIVY_NO_CONSOLELOG'] = '1'  # Desativar logs no console
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
print("Copyright ©2025 | Delean Mafra, todos os direitos reservados.")

class MyApp(App):
    def build(self):
        self.title = 'Calculadora de preço por quantidade'
        self.layout = BoxLayout(orientation='vertical')
        
        self.total_label = Label(text='Digite o total do produto (gm, unid, kg, etc...):')
        self.layout.add_widget(self.total_label)
        
        self.total_input = TextInput(multiline=False)
        self.layout.add_widget(self.total_input)
        
        self.value_label = Label(text='Digite o valor total:')
        self.layout.add_widget(self.value_label)
        
        self.value_input = TextInput(multiline=False)
        self.layout.add_widget(self.value_input)
        
 
        
        self.calculate_button = Button(text='Calcular')
        self.calculate_button.bind(on_press=self.calculate)
        self.layout.add_widget(self.calculate_button)
        self.copyright_label = Label(text='Copyright ©2025 | Delean Mafra, todos os direitos reservados.')
        self.layout.add_widget(self.copyright_label)       
        
        # Adicionando a mensagem de copyright

        
        return self.layout

    def calculate(self, instance):
        try:
            g = float(self.total_input.text.replace(",", "."))
            v = float(self.value_input.text.replace(",", "."))
            t = v / g
            self.result_label.text = f'O valor sai por R$ {t:.2f} cada'
        except ValueError:
            self.result_label.text = 'Por favor, insira valores válidos.'

if __name__ == '__main__':
    MyApp().run()
