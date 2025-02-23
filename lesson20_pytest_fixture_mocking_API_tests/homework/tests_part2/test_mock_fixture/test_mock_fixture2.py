# Перейдём к мокированию метода в фикстурах.
#
# Воспользуемся сценарием из прошлой задачи(test_mock_simple)
# И предположим что у нас не один, а 3 метода, использующих
# запросы к платным сервисам. (В реальности их может быть ещё больше).
# 
# В данном случаее удобнее было бы создать экземпляр такого класса в фикстуре
# и передавать его как аргумент в тестовые функции.
#
# Попробуйте с помощью фикстуры поставить одну заглушку для всех функций.
# В качестве возвращаемого аргумента также используйте  список 
# ["Санкт-Петербург", "Самара", "Краснодар"]
#
import requests
import os
import pytest

import sys
print(sys.path)

# Класс, подлежащий тестированию
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


def test_show_offices(prod_cl):
    expected_string = "Расположение офисов: Санкт-Петербург, Самара, Краснодар."
    assert prod_cl.show_offices() == expected_string

def test_show_warehouses(prod_cl):
    expected_string = "Расположение cкладов: Санкт-Петербург, Самара, Краснодар."
    assert prod_cl.show_warehouses() == expected_string

def test_show_markets(prod_cl):
    expected_string = "Расположение магазинов: Санкт-Петербург, Самара, Краснодар."
    assert prod_cl.show_markets() == expected_string

if __name__=="__main__":
    os.system("pytest")
