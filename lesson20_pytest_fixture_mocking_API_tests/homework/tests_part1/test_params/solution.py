import os
import pytest

def summer(*args):
    if len(args) == 1:
        return "Мало аргументов"
    for arg in args:
        if not isinstance(arg, int):
            return "ОШИБКА"
    if sum(args) > 300:
        return "Большое число"
    return sum(args)
    
# from solution import summer

summer_args = [
    [(5, 7, 9), 21], 
    [(302, ), "Мало аргументов"], 
    [("Qwe",), "ОШИБКА"], 
    [(260, 70), "Большое число"]]


@pytest.mark.parametrize('test_input, expected', summer_args)
def test_sum_numbers(test_input, expected):
    assert summer(*test_input) == expected


if __name__ == "__main__":
    os.system("pytest")