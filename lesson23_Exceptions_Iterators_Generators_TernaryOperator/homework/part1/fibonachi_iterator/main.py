# Напишите, свой собственный итератор,
# который отдавал бы N чисел фибоначчи
# (https://ru.wikipedia.org/wiki/Числа_Фибоначчи).
# Для решения задачи нужно дополнить класс Fib
# Достаточно будет сделать итератор только для положительных чисел


class Fib:
    def __init__(self, n):
        self.n = n
        # TODO напишите Ваш код здесь

    def __iter__(self):
        # TODO напишите Ваш код здесь
        pass

    def __next__(self):
        # TODO напишите Ваш код
        pass


fib = Fib(15)

if __name__ == "__main__":
    print([x for x in fib])
