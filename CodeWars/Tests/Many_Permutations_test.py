from Many_Permutations import unique_permutations
from math import factorial

def test_1 ():
    value = unique_permutations('aabb')
    for i in value:
        if i in ['aabb', 'abab', 'abba', 'baab', 'baba', 'bbaa']:
            b = True
        else:
            b = False
    assert b == True, f'test_1 -> "aabb" should return "[aabb, abab, abba, baab, baba, bbaa]", but return {value}'

def test_2 ():
    test_str = 'ab'
    value = unique_permutations(test_str)
    if  len (value) == factorial (len(set(test_str)))/ factorial(len(set(test_str)) - len(test_str)):
        b = True
    else:
        b = False
    assert b == True, f'test_2 -> "ab" should return "[ab, ba]", but return {value}'

def test_3 ():
    test_str = 'aabb'
    distingt_letter_counter = [test_str.count(letter) for letter in set(test_str)]
    print (distingt_letter_counter)
    unique_letters_factorial = 1
    for i in distingt_letter_counter:
        unique_letters_factorial *= factorial(i)
        print (unique_letters_factorial)

    count_possible_combinations = factorial (len(test_str))/ unique_letters_factorial
    value = unique_permutations(test_str)
    if  len (value) == count_possible_combinations:
        b = True
    else:
        b = False
    assert b == True, f'len ({value}) must be {count_possible_combinations}'

def test_4 ():
    test_str = 'abcd'
    distingt_letter_counter = [test_str.count(letter) for letter in set(test_str)]
    print (distingt_letter_counter)
    unique_letters_factorial = 1
    for i in distingt_letter_counter:
        unique_letters_factorial *= factorial(i)
        print (unique_letters_factorial)

    count_possible_combinations = factorial (len(test_str))/ unique_letters_factorial
    value = unique_permutations(test_str)
    if  len (value) == count_possible_combinations:
        b = True
    else:
        b = False
    assert b == True, f'len ({value}) must be {count_possible_combinations}'

def test_5 ():
    test_str = 'abbcdd'
    distingt_letter_counter = [test_str.count(letter) for letter in set(test_str)]
    print (distingt_letter_counter)
    unique_letters_factorial = 1
    for i in distingt_letter_counter:
        unique_letters_factorial *= factorial(i)
        print (unique_letters_factorial)

    count_possible_combinations = factorial (len(test_str))/ unique_letters_factorial
    value = unique_permutations(test_str)
    if  len (value) == count_possible_combinations:
        b = True
    else:
        b = False
    assert b == True, f'len ({value}) must be {count_possible_combinations}'
