import csv
from datetime import datetime
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup

print("Copyright ©2025 | Delean Mafra, todos os direitos reservados.")


CSV_FILE = 'despesas.csv'

class FinanceApp(App):
    def build(self):
        self.despesas = self.load_despesas()
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.valor_input = TextInput(hint_text='Valor da Despesa')
        self.categoria_input = TextInput(hint_text='Categoria de Custo')
        self.data_input = TextInput(hint_text='Data do Pagamento (dd/mm/yyyy)')

        self.add_button = Button(text='Adicionar Despesa', on_press=self.add_despesa)
        self.view_button = Button(text='Visualizar Total de Gastos', on_press=self.view_total_gastos)

        self.layout.add_widget(self.valor_input)
        self.layout.add_widget(self.categoria_input)
        self.layout.add_widget(self.data_input)
        self.layout.add_widget(self.add_button)
        self.layout.add_widget(self.view_button)

        return self.layout

    def load_despesas(self):
        despesas_list = []
        try:
            with open(CSV_FILE, mode='r', newline='') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    row['valor'] = float(row['valor'])
                    row['data'] = datetime.strptime(row['data'], '%d/%m/%Y')
                    despesas_list.append(row)
        except FileNotFoundError:
            pass
        return despesas_list

    def save_despesas(self):
        with open(CSV_FILE, mode='w', newline='') as file:
            fieldnames = ['valor', 'categoria', 'data']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for despesa in self.despesas:
                if isinstance(despesa['data'], datetime):
                    despesa['data'] = despesa['data'].strftime('%d/%m/%Y')
                writer.writerow(despesa)

    def add_despesa(self, instance):
        valor = self.valor_input.text
        categoria = self.categoria_input.text
        data = self.data_input.text

        if not self.validate_valor(valor):
            self.show_popup('Erro', 'Valor da despesa inválido! Deve ser um número.')
            return

        if not self.validate_data(data):
            self.show_popup('Erro', 'Data do pagamento inválida! Deve estar no formato dd/mm/yyyy.')
            return

        despesa = {
            'valor': float(valor),
            'categoria': categoria,
            'data': datetime.strptime(data, '%d/%m/%Y')
        }
        self.despesas.append(despesa)
        self.save_despesas()
        self.show_popup('Sucesso', 'A despesa foi adicionada com sucesso!')

    def view_total_gastos(self, instance):
        total_gastos = sum(d['valor'] for d in self.despesas)
        self.show_popup('Total de Gastos', f'O total de gastos é: R$ {total_gastos:.2f}')

    def validate_valor(self, valor):
        try:
            float(valor)
            return True
        except ValueError:
            return False

    def validate_data(self, data):
        try:
            datetime.strptime(data, '%d/%m/%Y')
            return True
        except ValueError:
            return False

    def show_popup(self, title, message):
        popup_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        popup_label = Label(text=message)
        close_button = Button(text='Fechar', size_hint=(1, 0.2))
        popup_layout.add_widget(popup_label)
        popup_layout.add_widget(close_button)
        popup = Popup(title=title, content=popup_layout, size_hint=(0.8, 0.8))
        close_button.bind(on_press=popup.dismiss)
        popup.open()

if __name__ == '__main__':
    FinanceApp().run()
