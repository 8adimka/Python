import pytest
from main_multiplicator_test import multiplicator
from main_summer_test import summer
from functools import reduce

# Параметризация для разных списков
@pytest.fixture(params=[
    [1, "2", 10, "20", 1, 5, 3, 8],  # Первый список
    [7, "4", '15', "12", '95', 5, 3, 8]  # Второй список
])
def incoming_list(request):
    return request.param

def test_sum_numbers(list_creator):
    list_sum = sum(list_creator)
    assert summer(*list_creator) == list_sum

def test_multiplicator(list_creator):
    result = multiplicator(*list_creator)
    expected = reduce(lambda x, y: x * y, list_creator)
    assert result == expected
