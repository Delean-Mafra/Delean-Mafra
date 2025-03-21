"""
Write a function, which takes a non-negative integer (seconds) as input and returns the time in a human-readable format (HH:MM:SS)

HH = hours, padded to 2 digits, range: 00 - 99
MM = minutes, padded to 2 digits, range: 00 - 59
SS = seconds, padded to 2 digits, range: 00 - 59
The maximum time never exceeds 359999 (99:59:59)

You can find some examples in the test fixtures.

#Sample Tests
import codewars_test as test
from solution import make_readable

@test.describe("Fixed Tests")
def fixed_tests():
    @test.it('Basic Test Cases')
    def basic_test_cases():
        test.assert_equals(make_readable(0), "00:00:00")
        test.assert_equals(make_readable(59), "00:00:59")
        test.assert_equals(make_readable(60), "00:01:00")
        test.assert_equals(make_readable(3599), "00:59:59")
        test.assert_equals(make_readable(3600), "01:00:00")
        test.assert_equals(make_readable(86399), "23:59:59")
        test.assert_equals(make_readable(86400), "24:00:00")
        test.assert_equals(make_readable(359999), "99:59:59")
"""

def make_readable(seconds):
    print('Copyright © Delean Mafra, todos os direitos reservados | All rights reserved.')
    """
    Convert seconds to human-readable time format (HH:MM:SS)
    
    Args:
        seconds: Non-negative integer representing total seconds
        
    Returns:
        String formatted as "HH:MM:SS" with zero-padded values
    """
    # Calculate hours, minutes, and seconds
    hours = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    
    # Format the time string with zero padding
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
