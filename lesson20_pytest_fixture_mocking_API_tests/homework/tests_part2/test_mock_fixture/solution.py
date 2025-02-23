import requests
import os
from unittest.mock import MagicMock
import requests
import pytest

class AddressGetter:
    def get_cities(city):
        response = requests.get(f'https://give_me_address.com?search={city}')
        return response.data
    
    def show_offices(self):
        cities = self.get_cities()
        cities = ", ".join(cities)
        return f"Расположение офисов: {cities}."
    
    def show_warehouses(self):
        cities = self.get_cities()
        cities = ", ".join(cities)
        return f"Расположение cкладов: {cities}."
    
    def show_markets(self):
        cities = self.get_cities()
        cities = ", ".join(cities)
        return f"Расположение магазинов: {cities}."

@pytest.fixture
def addressgetter():
	addressgetter = AddressGetter()
	addressgetter.get_cities = MagicMock(return_value=["Санкт-Петербург", "Самара", "Краснодар"])
	return addressgetter

def test_show_offices(addressgetter: AddressGetter):
    expected_string = "Расположение офисов: Санкт-Петербург, Самара, Краснодар."
    assert addressgetter.show_offices() == expected_string

def test_show_warehouses(addressgetter: AddressGetter):
    expected_string = "Расположение cкладов: Санкт-Петербург, Самара, Краснодар."
    assert addressgetter.show_warehouses() == expected_string

def test_show_markets(addressgetter: AddressGetter):
    expected_string = "Расположение магазинов: Санкт-Петербург, Самара, Краснодар."
    assert addressgetter.show_markets() == expected_string

if __name__=="__main__":
    os.system("pytest")
