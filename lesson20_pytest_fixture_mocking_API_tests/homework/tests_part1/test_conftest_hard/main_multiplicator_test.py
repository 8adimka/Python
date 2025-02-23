# фаил c тестами № 2
# Основной текст задания находится в файле main_summer_test.py
#
from functools import reduce
import pytest

# Исходная функция:
def multiplicator(*args):
    return reduce(lambda x, y: x * y, args)

@pytest.fixture
def incoming_list():
    return [1, "2", 10, "20", 1, 5, 3, 8]


def mult(list_c):
    res = 1
    for num in list_c:  # Просто перемножаем все элементы
        res *= num
    return res


def test_multiplicator(list_creator):
    result = multiplicator(*list_creator)
    expected = mult(list_creator)
    assert result == expected


