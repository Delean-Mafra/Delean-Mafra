#Copyright © Delean Mafra, todos os direitos reservados
#Created on: 2025-03-24 02:54:01 UTC
#Author: Delean-Mafra

def lottery(s):
    seen = set()
    result = []

    for char in s:
        if char.isdigit() and char not in seen:
            seen.add(char)
            result.append(char)

    return ''.join(result) if result else "One more run!"
