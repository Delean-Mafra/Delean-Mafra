print("Copyright ©2025 | Delean Mafra, todos os direitos reservados.")


def invert(lst):
    return [-d for d in lst]


# Example usage:
print(invert([1, 2, 3, 4, 5]))  # Output: [-1, -2, -3, -4, -5]
print(invert([1, -2, 3, -4, 5]))  # Output: [-1, 2, -3, 4, -5]
print(invert([]))  # Output: []
