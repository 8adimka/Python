import requests
import os
import requests
from unittest.mock import MagicMock

class AddressGetter:
    def get_cities(city):
        response = requests.get(f'https://give_me_address.com?search={city}')
        return response.data
    
    def show_cities(self):           
        cities = self.get_cities()   
        cities = ", ".join(cities)
        return f"Расположение офисов: {cities}."


def test_show_cities():
    addressgetter = AddressGetter()
    addressgetter.get_cities = MagicMock(return_value=["Санкт-Петербург", "Самара", "Краснодар"])
    expected_string = "Расположение офисов: Санкт-Петербург, Самара, Краснодар."
    assert addressgetter.show_cities() == expected_string

if __name__=="__main__":
    os.system("pytest")