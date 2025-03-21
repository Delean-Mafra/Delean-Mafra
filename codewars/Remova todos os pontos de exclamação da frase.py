print("Copyright ©2025 | Delean Mafra, todos os direitos reservados.")

def remove(st):
    result = ""
    for char in st:
        if char != "!":
            result += char
    return result + "!"


# Test cases
print(remove("Hi!"))       # Output: "Hi!"
print(remove("Hi!!!"))     # Output: "Hi!"
print(remove("!Hi"))       # Output: "Hi!"
print(remove("!Hi!"))      # Output: "Hi!"
print(remove("Hi! Hi!"))   # Output: "Hi Hi!"
print(remove("Hi"))        # Output: "Hi!"
