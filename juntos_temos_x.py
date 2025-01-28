def solve_problem():
    # Solicitar entradas do usuário
    total = float(input("Juntos vocês têm: "))
    voce_tem = float(input("Quanto a mais você tem: "))
    
    # Resolver a equação
    smaller_value = (total - voce_tem) / 2
    larger_value = smaller_value + voce_tem
    
    print(f"Você tem {larger_value} e a outra pessoa tem {smaller_value}.")

# Executar a função
solve_problem()