import re

print("Copyright ©2025 | Delean Mafra, todos os direitos reservados.")

def show_me(name):
    # A regex pattern that matches names starting with a capital letter followed by lowercase letters.
    # It also allows for hyphenated names.
    pattern = r'^([A-Z][a-z]*)(-[A-Z][a-z]*)*$'

    
    # The search function returns a Match object if the regex pattern is found in the 'name'.
    # If the pattern is not found, it returns None.
    match = re.search(pattern, name)
    
    
    # If a Match object is returned, the name is valid, so return True.
    # If None is returned, the name is not valid, so return False.
    return match is not None

 
    