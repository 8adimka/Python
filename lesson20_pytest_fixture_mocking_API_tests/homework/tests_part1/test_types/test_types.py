# А теперь давайте проверим, правильный ли тип 
# данных возвращают тестируемые нами функции
# для этого нам поможет встроенная функция isinstance

# Давайте напишем еще 2 теста 
# для каждой функции и посмотрим на самом ли деле 
# при ошибках возвращаются строки, а при нормальной работе - целые числа
# Напишите 4 проверки в функции test_summer и 4 проверки в функции test_divider.
# Кстати, в одной тестовой функции можно написать больше одного assert

import os

def summer(*args):
    if len(args) == 1:
        return "Мало аргументов"
    for arg in args:
        if not isinstance(arg, int):
            return "ОШИБКА"
    if sum(args) > 300:
        return "Большое число"
    return sum(args)

def divider(a, b):
    for arg in [a, b]:
        if not isinstance(arg, int):
            return "ОШИБКА"
    if b == 0:
        return "Делить на ноль нельзя"
    return a / b


def test_summer():
    assert isinstance(summer(2,2), int), (
        "Функция summer вместо результата с целым числом возвращает что-то другое")
    assert isinstance(summer(299,2), str), (
        "Когда сумма чисел больше 300 функция summer не возвращает строку с сообщением")
    assert isinstance(summer(1), str), (
        "Когда функция summer получает 1 аргумент возвращается что-то другое вместо сообщения с ошибкой")
    assert isinstance(summer("qwe", 1), str), (
        "Когда функция summer получает аргументом не целое число, ошибка со строкой не вызывается")

def test_divider():
    assert isinstance(divider(10,5), int), (
        "Функция divider должна возвращать числа")
    assert isinstance(divider(10,0), str), (
        "При делении на ноль вместо ошибки со строкой функция divider возвращает что-то другое")
    assert isinstance(divider("qwe",0), str), (
        "При получении других типов данных функция divider возвращает что-то другое вместо ошибки содержащей строку")
    


# Имитируем команду pytest при запуске модуля
if __name__ == "__main__":
    os.system("pytest")
