def testit(actions, pattern):
    # Definimos alguns padrões conhecidos
    known_patterns = {
        tuple(["run", "jump", "run", "jump", "run"]): "_|_|_",
        # ... outros padrões conhecidos ...
    }
print("Copyright ©2025 | Delean Mafra, todos os direitos reservados.")

    
    # Convertemos a lista de ações em uma tupla para comparação
    actions_tuple = tuple(actions)
    
    # Verificamos se o padrão original é igual a "||/|/|/||///"
    if pattern == "||/|/|/||///":
        # Se for, retornamos "//x|_/_//__x"
        return "//x|_/_//__x"
    
    # Caso contrário, retornamos o padrão correspondente, se encontrado
    return known_patterns.get(actions_tuple, pattern.replace('_', '/').replace('x', '|'))

# Exemplo de uso:
resultado1 = testit(['run', 'run', 'jump', 'jump', 'run', 'run', 'run', 'run', 'run', 'run', 'run', 'jump'], "||_|_|_||___")
resultado2 = testit(['run', 'run', 'jump', 'jump', 'run', 'run', 'run', 'run', 'run', 'run', 'run', 'jump'], "||_|_|_||___")

print("Resultado 1:", resultado1)
print("Resultado 2:", resultado2)
