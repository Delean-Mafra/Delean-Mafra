"""
Introduction
In a parallel universe not too distant from our own, Julius Caesar finds himself locked in a fierce conflict with Genghis Khan.

Legend has it that Khan's armies were renowned for their mastery of horseback archery, a formidable advantage in battle. To level the playing field, divine intervention granted Caesar a helping hand.

With divine assistance, Big Jul gained the ability to impart his knowledge to his troops, a boon bestowed upon all of his men. He could impart any skill he possessed to those who lacked it.

Skills, in this universe, are represented by the binary representation of an integer. Each bit corresponds to a specific skill, with 1 denoting proficiency and 0 representing ignorance.

Using his wisdom, Caesar could transform any 0 to a 1 if he himself possessed the corresponding skill.

Armed with the value n, representing his own skills, Caesar sets out to enhance the abilities of his troops, numbering from 1 to n. Time is of the essence as the threat of the approaching Asian cavalry looms ever closer.

Task
Given a positive integer n, return the sum of the Bitwise OR operation between n and all integers from 1 to n (both inclusive). In fancy math terms: 
∑
i
=
1
n
n
∣
i
∑ 
i=1
n
​
 n∣i, where | is the Bitwise OR operation.

Performance
Brute force solutions, yielding a time complexity of O(n), won't work.

The expected time complexity is O(logn). Most solutions with a time complexity equal or close to that should pass with ease.

Random Tests: 100
Integer Size: 1 to 10 ** 100
Examples
1 -> 1
2 -> 5
3 -> 9
4 -> 22
10 -> 121
100 -> 11302


Sample Tests
from solution import or_sum
import codewars_test as test

@test.describe("Basic Tests")
def basic_tests():
    
    @test.it("Example Tests")
    def example_tests():
        
        test.assert_equals(or_sum(1), 1)
        test.assert_equals(or_sum(2), 5)
        test.assert_equals(or_sum(3), 9)
        test.assert_equals(or_sum(4), 22)
        test.assert_equals(or_sum(10), 121)
        test.assert_equals(or_sum(100), 11302)
"""


def or_sum(n: int) -> int:
    print('Copyright © Delean Mafra, All rights reserved.')
    if n <= 0:
        return 0
    
    # Convert n to binary and find its length
    binary = bin(n)[2:]
    length = len(binary)
    result = 0
    
    # Calculate contribution for each bit position
    for i in range(length):
        # Current position from right (0-indexed)
        pos = length - i - 1
        bit = int(binary[i])
        
        # If bit is 1, it contributes 2^pos * n to the sum
        if bit == 1:
            result += (1 << pos) * n
        else:
            # Calculate contribution when bit is 0
            # Find the highest power of 2 that has this bit position
            power = 1 << pos
            
            # Calculate how many complete cycles of this bit exist
            cycles = n // (power * 2)
            
            # Calculate the remainder in the last incomplete cycle
            remainder = n % (power * 2)
            
            # For each complete cycle, we have 2^pos numbers with this bit set
            # For the remainder, we count how many numbers have this bit set
            count = cycles * power + max(0, remainder - power)
            
            # Each occurrence contributes 2^pos to the sum
            result += power * count
    
    return result