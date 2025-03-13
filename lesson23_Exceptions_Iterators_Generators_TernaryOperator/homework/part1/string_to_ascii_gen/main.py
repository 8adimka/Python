# Нужно реализовать функцию convert,
# которая должна преобразовывать строку input_str
# в массив аски-кодов (https://ru.wikipedia.org/wiki/ASCII).
# Ваша функция должна возвращать генератор,
# который при каждом вызове метода __next__ возвращает акси-код буквы
# из полученной строки input_str


input_str = "hello my friend"


def convert(input_str):
    return ()


if __name__ == "__main__":
    for letter in convert(input_str):
        print(letter)
