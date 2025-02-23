import os
import pytest

@pytest.fixture
def incoming_list():
    return [7, "4", 15, "12", 95, 5, 3 ,8]

def summer(*args):
    return sum(args)

def test_sum_numbers(list_creator):
    list_sum = sum(list_creator)
    assert summer(*list_creator) == list_sum


if __name__ == "__main__":
    os.system("pytest")