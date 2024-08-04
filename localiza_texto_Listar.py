import os

print("Copyright ©2024 | Delean Mafra, todos os direitos reservados.")

def find_in_files():
    while True:
        directory = input("Digite o caminho da pasta: ")
        if os.path.isdir(directory):
            break
        else:
            print("Diretório inválido. Por favor, tente novamente.")

    while True:
        target_string = input("Agora digite o texto que você quer pesquisar: ")

        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith((".rpy", ".txt", ".json", ".conf")):
                    try:
                        with open(os.path.join(root, file), 'r', encoding='utf-8', errors='ignore') as f:
                            lines = f.readlines()
                            for i, line in enumerate(lines, start=1):
                                if target_string in line:
                                    print(f'O arquivo "{file}" contém a string "{target_string}" na linha {i}: {line.strip()}')
                    except Exception as e:
                        print(f"Erro ao ler o arquivo {file}: {e}")

        resposta = input("Deseja pesquisar em outro diretório? (S/N) ").upper()
        if resposta in ["NÃO", "N", "NO", "N"]:
            print("Obrigado por usar o programa. Até mais!")
            break
        elif resposta in ["SIM", "S", "YES", "Y"]:
            while True:
                directory = input("Digite o caminho da pasta: ")
                if os.path.isdir(directory):
                    break
                else:
                    print("Diretório inválido. Por favor, tente novamente.")
        else:
            print("Resposta inválida. Por favor, responda com 'S' ou 'N'.")

# Uso
find_in_files()
