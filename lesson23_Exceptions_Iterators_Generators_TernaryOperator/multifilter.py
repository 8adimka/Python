import itertools
from typing import Iterable


class multifilter:
    @staticmethod
    def judge_half(pos, neg):
        return pos >= neg

        # допускает элемент, если его допускает хотя бы половина фукнций (pos >= neg)

    @staticmethod
    def judge_any(pos, neg):
        return pos >= 1

        # допускает элемент, если его допускает хотя бы одна функция (pos >= 1)

    @staticmethod
    def judge_all(pos, neg):
        return neg == 0

        # допускает элемент, если его допускают все функции (neg == 0)

    def __init__(self, l: Iterable, *args, pos=0, neg=0, judge=judge_any):
        # iterable - исходная последовательность
        # funcs - допускающие функции
        # judge - решающая функция

        self.l = l
        self.args = args  # args — уже кортеж!
        self.judge = judge

    def make_it(self):
        for item in self.l:
            pos = 0
            neg = 0
            for func in self.args:
                if func(item):
                    pos += 1
                else:
                    neg += 1
            if self.judge(pos, neg):
                yield item

    def __iter__(self):
        return self.make_it()

    # возвращает итератор по результирующей последовательности


def mul2(x):
    return x % 2 == 0


def mul3(x):
    return x % 3 == 0


def mul5(x):
    return x % 5 == 0


a = [i for i in range(31)]  # [0, 1, 2, ... , 30]

print(list(multifilter(a, mul2, mul3, mul5)))
# [0, 2, 3, 4, 5, 6, 8, 9, 10, 12, 14, 15, 16, 18, 20, 21, 22, 24, 25, 26, 27, 28, 30]

print(list(multifilter(a, mul2, mul3, mul5, judge=multifilter.judge_half)))
# [0, 6, 10, 12, 15, 18, 20, 24, 30]

print(list(multifilter(a, mul2, mul3, mul5, judge=multifilter.judge_all)))
# [0, 30]


def primes():
    a = 1
    while True:
        counter = 0
        a += 1
        b = 1
        while b <= a:
            b += 1
            if a % b == 0:
                counter += 1
        if counter == 1:
            yield a


print(list(itertools.takewhile(lambda x: x <= 31, primes())))
# [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31]
