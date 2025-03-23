#Copyright © Delean Mafra, todos os direitos reservados

def pizza_rewards(customers, min_orders, min_price):
    # Lista para armazenar clientes elegíveis
    eligible_customers = []
    
    # Itera sobre cada cliente e seus pedidos
    for customer, orders in customers.items():
        # Conta quantos pedidos atendem ao critério de preço mínimo
        qualifying_orders = sum(1 for order in orders if order >= min_price)
        
        # Se o número de pedidos qualificados for maior ou igual ao mínimo necessário
        if qualifying_orders >= min_orders:
            eligible_customers.append(customer)
            
    return eligible_customers
