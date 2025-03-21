import random

def calculate_check_digit(key43):
    """
    Calculates the check digit (DV) for the first 43 digits of the access key.
    """
    weights = [4, 3, 2, 9, 8, 7, 6, 5]  # Repeating weights
    total = 0
    for i, digit in enumerate(key43):
        weight = weights[i % len(weights)]
        total += int(digit) * weight
    remainder = total % 11
    check_digit = 11 - remainder
    if check_digit >= 10:
        check_digit = 0
    return check_digit
print("Copyright ©2025 | Delean Mafra, todos os direitos reservados.")


def validate_access_key(key):
    """
    Validates the access key of the NRE (National Register of Legal Entities).
    """
    if len(key) != 44 or not key.isdigit():
        return False
    key43 = key[:43]
    given_check_digit = int(key[43])
    calculated_check_digit = calculate_check_digit(key43)
    return given_check_digit == calculated_check_digit

def validate_key_list(key_list):
    """
    Validates a list of access keys.
    Returns True if at least one key is valid, False if all are invalid.
    """
    return any(validate_access_key(key) for key in key_list)

def fill_with_zeros(value, total_digits):
    """
    Fills a string with zeros to reach the total number of digits.
    """
    return value + '0' * (total_digits - len(value))

def random_invalid_key():
    """
    Generates a random invalid access key with 44 digits.
    """
    invalid_access_key = str(random.randint(1000000000000000000000000000000000000000000, 9999999999999999999999999999999999999999999))
    return invalid_access_key

def random_valid_key():
    """
    Generates a random valid access key with 44 digits.
    """
    nre = str(random.randint(10000000000000, 99999999999999))
    series = str(random.randint(100, 999))
    state_code = str(random.randint(10, 99))
    year_month = str(random.randint(1000, 9999))
    model = str(random.randint(10, 99))
    number = str(random.randint(1000, 9999))
    fem = str(random.randint(10, 99))
    digits36 = str(state_code) + str(year_month) + str(nre) + str(model) + str(series) + str(number) + str(fem)
    digits43 = fill_with_zeros(digits36, 43)
    check_digit = calculate_check_digit(digits43)
    access_key = str(digits43) + str(check_digit)
    return access_key

# Generate valid and invalid keys
valid_keys = random_valid_key()
invalid_keys = random_invalid_key()

# Validate valid keys
print(validate_key_list([valid_keys]))  # Expected: True

# Validate invalid keys
print(validate_key_list([invalid_keys]))  # Expected: False
