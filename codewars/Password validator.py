"""
Description
Your job is to create a simple password validation function, as seen on many websites.

The rules for a valid password are as follows:

There needs to be at least 1 uppercase letter.
There needs to be at least 1 lowercase letter.
There needs to be at least 1 number.
The password needs to be at least 8 characters long.
You are permitted to use any methods to validate the password.

Examples:
password("Abcd1234"); ===> true
password("Abcd123"); ===> false
password("abcd1234"); ===> false
password("AbcdefGhijKlmnopQRsTuvwxyZ1234567890"); ===> true
password("ABCD1234"); ===> false
password("Ab1!@#$%^&*()-_+={}[]|\:;?/>.<,"); ===> true;
password("!@#$%^&*()-_+={}[]|\:;?/>.<,"); ===> false;
Extra info
You will only be passed strings.
The string can contain any standard keyboard character.
Accepted strings can be any length, as long as they are 8 characters or more.


Sample Tests
import codewars_test as test
from solution import password

@test.describe("Example Tests")
def example_tests():
    
    def do_test(pwd, expected):
        test.assert_equals(password(pwd), expected, f'password("{pwd}")')
        
    @test.it('Valid passwords')
    def valid_passwords():
        do_test("Abcd1234", True)
        do_test("AbcdefGhijKlmnopQRsTuvwxyZ1234567890", True)
        do_test("Ab1!@#$%^&*()-_+={}[]|:;?/>.<,", True)
        do_test(" aA1----", True)
        do_test("4aA1----", True)

    @test.it('Too short passwords')
    def too_short_passwords():
        do_test("Abcd123", False)

    @test.it('Missing uppercase letters')
    def missing_uppercase_letters():
        do_test("abcd1234", False)

    @test.it('Missing digits')
    def missing_digits():
        do_test("abcdABCD", False)

    @test.it('Missing lowercase letters')
    def missing_lowercase_letters():
        do_test("ABCD1234", False)

    @test.it('Only special characters')
    def only_special_characters():
        do_test("!@#$%^&*()-_+={}[]|:;?/>.<,", False)

    @test.it('Empty password')
    def empty_password():
        do_test("", False)
        
"""


#Copyright © Delean Mafra, todos os direitos reservados
#Created on: 2025-03-28 01:10:15 UTC
#Author: Delean-Mafra

def password(pwd):
    if len(pwd) < 8:
        return False
    has_upper = any(c.isupper() for c in pwd)
    has_lower = any(c.islower() for c in pwd)
    has_digit = any(c.isdigit() for c in pwd)
    return has_upper and has_lower and has_digit
