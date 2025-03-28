def nickname_generator(name):
    vowels = 'aeiou'
    if len(name) < 4:
        return 'Error: Name too short'
    if name[2].lower() in vowels:
        return name[:4]
    return name[:3]
