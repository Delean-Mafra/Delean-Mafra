"""
#Copyright © Delean Mafra, todos os direitos reservados
Created on: 2025-03-23 02:38:06 UTC
Author: Delean-Mafra
"""

def passed(lst):
    # Filtra apenas as notas que passaram (<=18 pontos)
    passing_scores = [score for score in lst if score <= 18]
    
    # Se não houver notas aprovadas, retorna a mensagem
    if not passing_scores:
        return 'No pass scores registered.'
    
    # Calcula a média e arredonda para o inteiro mais próximo
    average = round(sum(passing_scores) / len(passing_scores))
    
    return average
