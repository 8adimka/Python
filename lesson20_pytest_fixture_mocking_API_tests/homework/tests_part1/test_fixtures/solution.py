import pytest
import os

test_list = [25, '16', '31', 9, 7, 6, '21', 13, 5,
             1, '1', '1', 1, 1, 1, '2', 4, 5,
             27, '4', '5', 9, 7, 6, '17', 13, 5,
             6, '16', '3', 4, 9, 5, '21', 2, 5,
             25, '8', '15', 9, 7, 0, '2', 13, 5]

def summer(*args):
    for arg in args:
        if not isinstance(arg, int):
            return "ОШИБКА"
    if len(args) == 1:
        return "Мало аргументов"
    if sum(args) > 1500:
        return "Большое число"
    return sum(args)


@pytest.fixture
def list_creater():
    for index in range(len(test_list)):
        test_list[index] = int(test_list[index])
    return test_list

def test_sum_numbers(list_creater):
    list_sum = sum(list_creater)
    assert summer(*list_creater) == list_sum

if __name__ == "__main__":
    os.system("pytest")