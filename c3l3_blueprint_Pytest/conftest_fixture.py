# можем использовать фикстуры из других файлов как заготовки данных для тестов
# utils.py   ###############################################

def sum_func(a, b):
    return a + b

# conftest.py  #############################################

import pytest

@pytest.fixture()
def two_numbers_sum():  #  запомните это имя
    return (1, 1, 2)

# utils_test.py  ############################################

import conftest
from utils import sum_func

def test_sum_func( two_numbers_sum):  # обратите внимание на имя

    sum_result = sum_func(two_numbers_sum[0], two_numbers_sum[1])
    assert sum_result == two_numbers_sum[2]