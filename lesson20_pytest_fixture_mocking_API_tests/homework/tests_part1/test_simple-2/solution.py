import os

def divider(a, b):
    for arg in [a, b]:
        if not isinstance(arg, int):
            return "ОШИБКА"
    if b == 0:
        return "Делить на ноль нельзя"
    return a / b


def test_result():
    assert divider(10,5) == 2, "Функция неправильно делит числа"

def test_zero_divide_error():
    assert divider(299, 0) == "Делить на ноль нельзя", "Во втором аргументе функция не определяет ноль"

def test_error():
    assert divider(1, "qwe") == "ОШИБКА", "Функция не перехватывает ошибки или делает это неверно"




# Имитируем команду pytest при запуске модуля
if __name__ == "__main__":
    os.system("pytest")

