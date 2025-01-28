from datetime import datetime
import pytz

print('Qual fuso horário você quer comparar?')

# Definindo o fuso horário do computador (GMT-3)
local_tz = pytz.timezone('America/Sao_Paulo')

# Obtendo a hora atual no fuso horário local
local_time = datetime.now(local_tz)

# Lista de fusos horários
timezones = {
    'r': ('Reino Unido', 'Europe/London'),
    'p': ('Paris', 'Europe/Paris'),
    'e': ('Egito', 'Africa/Cairo'),
    'i': ('Índia', 'Asia/Kolkata'),
    'c': ('China', 'Asia/Shanghai'),
    'j': ('Japão', 'Asia/Tokyo'),
    'k': ('Coreia', 'Asia/Seoul'),
    'm': ('México', 'America/Mexico_City'),
    'v': ('Venezuela', 'America/Caracas'),
    'n': ('Noruega', 'Europe/Oslo'),
    'a': ('Alemanha', 'Europe/Berlin'),
    's': ('Suíça', 'Europe/Zurich'),
    'u': ('Estados Unidos', 'America/New_York'),
    'ca': ('Canadá', 'America/Toronto'),
    'ru': ('Rússia', 'Europe/Moscow'),
    'es': ('Espanha', 'Europe/Madrid'),
    'is': ('Israel', 'Asia/Jerusalem'),
    'pe': ('Pérsia', 'Asia/Tehran'),
    'pn': ('Polo Norte', 'Arctic/Longyearbyen'),
    'ps': ('Polo Sul', 'Antarctica/South_Pole'),
    'pt': ('Portugal', 'Europe/Lisbon')  # Adicionando Portugal
}

# Exibindo as opções para o usuário
for key, value in timezones.items():
    print(f'Pressione "{key}" para selecionar o fuso horário de {value[0]}')

fuso = input('Digite a letra conforme sua escolha: ').lower()

if fuso in timezones:
    tz_name = timezones[fuso][1]
    selected_tz = pytz.timezone(tz_name)
    selected_time = local_time.astimezone(selected_tz)
    print(f'Hora em {timezones[fuso][0]} ({tz_name}):', selected_time.strftime('%d/%m/%Y %H:%M:%S'))
else:
    print('Opção inválida.')

print("Hora local (GMT-3):", local_time.strftime('%d/%m/%Y %H:%M:%S'))
