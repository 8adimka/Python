import pytest 

from Primes_in_numbers import prime_factors

def test_1 ():
    a = prime_factors(7775460)
    assert a == "(2**2)(3**3)(5)(7)(11**2)(17)", f'Test_1 Error, we have {a}, but (2**2)(3**3)(5)(7)(11**2)(17) needed'

def test_2 ():
    assert prime_factors(7919) == '(7919)', 'Test_2 Error'

