def my_generator(max_c):
    c = 0
    while c < max_c:
        print(f"before {c}")
        yield "________________some\n"
        print("after")
        c += 1


gen = my_generator(3)

print(gen)
try:
    while True:  # Бесконечный цикл
        print(next(gen))  # Будет получать значения, пока генератор не исчерпается
except StopIteration:
    print("Генератор завершен.")

foo = lambda *args, **kwargs: len(args)
print(foo(1, 2, 3, var=1))  # Считает тут 3 позиционных аргумента


print_kwargs = lambda *args, **kwargs: print(kwargs)
print_kwargs(
    1, 2, 3, var1=1, var2=0.5
)  # Функция напечатает словарь - {'var1': 1, 'var2': 0.5}


my_func = lambda *args, **kwargs: print(len(args))

my_func(1, 2, 3, lam1=1, lam2=3.5)
my_func(1, 2, 3, 2, 3, 5, lam1=2)


def simple_gen():
    print("some1")
    yield
    print("some2")
    yield
    print("some3")
    yield


next(simple_gen())
s = iter(simple_gen())  # или при простом вызове функции тоже вернётся обьект итератора
next(s)
next(s)


s2 = (x for x in range(1, 5) if x % 2 == 0)
print(next(s2))
print(s2.__next__())
try:
    print(next(s2))
except StopIteration as e:
    print(
        f"The End of the Iteration raise the error -> {StopIteration.__name__}, it's need to be cached!"
    )
