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


def test_sum():
    assert summer(3,6,9) == 18, "Функция не правильно складывает числа"

def test_big_number():
    assert summer (299, 25) == "Большое число", "Функция не определяет большие числа"

def test_one_arg():
    assert summer(1) == "Мало аргументов", "Ошибка возникла при передаче более одного аргумента"

def test_wrong_arg():
    assert summer (1, "qwe") == "ОШИБКА", "Функция не перехватывает ошибки или делает это неверно"



# Имитируем команду pytest при запуске модуля
if __name__ == "__main__":
    os.system("pytest")

