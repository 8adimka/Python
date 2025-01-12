import pytest 

from pony_exspress import riders

def test_1 ():
    a = riders([19, 49, 44, 38, 13, 22, 21, 44, 18, 22, 43, 28, 47], 2)
    assert riders([19, 49, 44, 38, 13, 22, 21, 44, 18, 22, 43, 28, 47], 2) == 6, f'Test_1 Error, we have {a}, but 6 needed'

def test_2 ():
    assert riders([37, 28, 29, 12, 12, 26, 30, 46, 6, 23], 5) == 4, 'Test_2 Error'

def test_3 ():
    assert riders([60, 80, 30, 15], 2) == 5, 'Test_3 Error'

def test_4 ():
    assert riders([33, 45, 48, 15], 4) == 4, 'Test_4 Error'

def test_Zero ():
    with pytest.raises(ValueError):
        riders([33, 45, 48, 15], 0)

def test_Negative ():
    with pytest.raises(ValueError):
        riders([-1], -1)

def test_Negative_2 ():
    with pytest.raises(ValueError):
        riders([-1], 2)

