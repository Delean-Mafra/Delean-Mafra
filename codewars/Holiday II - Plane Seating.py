def plane_seat(seat):
    # Extract the number and letter from the seat code
    number, letter = seat[:-1], seat[-1]
    
    # Check if the number is within the valid range (1-60)
    if not (1 <= int(number) <= 60):
        return 'No Seat!!'
    
    # Check if the letter is valid
    if letter not in 'ABCDEFGHK':
        return 'No Seat!!'
    
    # Determine the section based on the number
    if 1 <= int(number) <= 20:
        section = 'Front'
    elif 21 <= int(number) <= 40:
        section = 'Middle'
    else:
        section = 'Back'
    
    # Determine the cluster based on the letter
    if letter in 'ABC':
        cluster = 'Left'
    elif letter in 'DEF':
        cluster = 'Middle'
    else:
        cluster = 'Right'
    
    # Return the seat location
    return f'{section}-{cluster}'

# Test cases
def test_plane_seat():
    assert plane_seat('2B') == 'Front-Left'
    assert plane_seat('20B') == 'Front-Left'
    assert plane_seat('58I') == 'No Seat!!'
    assert plane_seat('60D') == 'Back-Middle'
    assert plane_seat('17K') == 'Front-Right'

# Run tests
test_plane_seat()
