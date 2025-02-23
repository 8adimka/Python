from functools import reduce
import pytest

@pytest.fixture
def incoming_list():
    return [1, "2", 10, "20", 1, 5, 3 ,8]


def multiplicator(*args):
    return reduce(lambda x, y: x*y, args)


def test_multiplicator(list_creator):
    multiple_sum = reduce(lambda x, y: x*y, list_creator)
    assert multiplicator(*list_creator) == multiple_sum