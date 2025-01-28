import csv
import os

# Define the path to the CSV file
csv_file_path = '\.csv'

# Function to calculate and log the profit and expense
def roleta():
    # Initialize the total expense and profit
    total_expense = 0
    total_profit = 0
    
    # Check if the CSV file exists, if not create it and write the header
    if not os.path.exists(csv_file_path):
        with open(csv_file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Rodada", "Despesa", "Lucro", "Saldo"])
    
    rodada = 1
    while True:
        # Deduct the cost of one round
        total_expense -= 1250
        
        # Ask the user for the amount won in this round
        valor_ganho = int(input(f"Favor informe o valor que você ganhou na roleta (Rodada {rodada}): "))
        
        # Calculate the current balance
        saldo = total_expense + valor_ganho
        
        # Log the results in the CSV file
        with open(csv_file_path, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([rodada, -1250, valor_ganho, saldo])
        
        # Print the current balance to the user
        print(f"Você teve um saldo de {saldo}")
        
        # Ask if the user wants to play another round
        continuar = input("Deseja rodar a roleta novamente? (s/n): ")
        if continuar.lower() != 's':
            break
        
        rodada += 1

# Run the function
roleta()
