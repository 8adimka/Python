import pytest

from Take_a_Ten_Minutes_Walk import is_valid_walk

def test_1 ():
    assert is_valid_walk(['n', 's', 'n', 's', 'n', 's', 'n', 's', 'n', 's']) == True, 'should return True'

def test_2 ():
    assert is_valid_walk(['w', 'e', 'w', 'e', 'w', 'e', 'w', 'e', 'w', 'e', 'w', 'e']) == False, 'should return False'

def test_3 ():
    assert is_valid_walk(['e', 'w', 'e', 'w', 'n', 's', 'n', 's', 'e', 'w']) == True, 'should return True'

def test_4():
    assert is_valid_walk(['n','s','n','s','n','s','n','s','n','s']) == True, 'should return True'
    