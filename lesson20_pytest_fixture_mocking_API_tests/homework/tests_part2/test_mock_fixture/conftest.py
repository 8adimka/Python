import pytest
from unittest.mock import MagicMock
import sys
sys.path.append("/home/v/Python/lesson20_pytest_fixture_mocking_API_tests/homework/tests_part2/test_mock_fixture/")

from test_mock_fixture2 import AddressGetter  # Импортируем класс из main.py

@pytest.fixture
def prod_cl():
    # Создаём экземпляр класса AddressGetter
    cities = AddressGetter()
    # Мокируем метод get_cities
    cities.get_cities = MagicMock(return_value=["Санкт-Петербург", "Самара", "Краснодар"])
    return cities




