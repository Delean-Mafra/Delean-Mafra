#Copyright © Delean Mafra, todos os direitos reservados
#Created on: 2025-03-25 02:52:59 UTC
#Author: Delean-Mafra

def initialize_names(name):
    parts = name.split()
    if len(parts) <= 2:
        return name
    else:
        first_name = parts[0]
        last_name = parts[-1]
        middle_names = ' '.join([f'{part[0]}.' for part in parts[1:-1]])
        return f'{first_name} {middle_names} {last_name}'
