import pytest

@pytest.fixture()
def list_creator(incoming_list):
    """Фикстура преобразует все элементы списка в целые числа (int)"""
    return [int(num) for num in incoming_list]
