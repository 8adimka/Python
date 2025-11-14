from functools import wraps


def my_decorator(arg):
    def real_decorator(func):
        @wraps(func)  # 🎯 копирует имя, докстринг, аннотации и т.д.
        def wrapper(
            *args, **kwargs
        ):  # Мы не передаём func в wrapper напрямую, но она содержится в enclosure, поэтому исп. как free variable
            # free variable — переменная, которая не определена внутри функции, но используется в ней т.к. содержится в enclosure
            print("До вызова функции")
            func(*args, **kwargs)
            print(f"После вызова функции печатаем аргумент декоратора - {arg}")

        return wrapper

    return real_decorator


@my_decorator("🎉 Это аргумент декоратора!")
def some_func(a, b):
    print(f"Во время выполнения функции,\nпечатаем {a} и {b}")


some_func("Аргументы", 5)


print("_________________________________________________")


def real_decorator(func):
    @wraps(func)  # 🎯 копирует имя, докстринг, аннотации и т.д.
    def wrapper(*args, **kwargs):
        print("До вызова функции")
        func(*args, **kwargs)
        print("После вызова функции!")
        # Если func ничего не возвращает, то Ок, но если надо вернуть результат func, то
        # return func(*args, **kwargs)
        # далее возвращаем return wrapper, который подменяет собой декорируемую func
        # my_func = real_decorator(my_func) -> эквивалентно декорации my_func через @real_decorator

    return wrapper


# @real_decorator
# def some_func(a, b=5):
#     print(f"Во время выполнения функции,\nпечатаем {a} и {b}")


# some_func("Аргументы")


def repeat(n=5):
    def decorator(func):
        @wraps(func)  # 🎯 копирует имя, докстринг, аннотации и т.д.
        def wrapper(*args, **kwargs):
            for i in range(n):
                res = func(*args, **kwargs)
                return res

        return wrapper

    return decorator


# @repeat(2)
# def hello(name):
#     print(f"Hello, {name}!")

# hello("Vadim")


def hello(name="Julia"):
    print(f"Hello, {name}!")


repeat(1)(hello)()
repeat(3)(hello)("Max")

# 🔄 Разовая обёртка — вызовет декоратор вручную:
wrapped_hello = repeat(3)(
    hello
)  # сначала repeat(3) → вернёт декоратор → вызываем с hello

# вызов
wrapped_hello()


@real_decorator
def hello1(name):
    print(f"Привет, {name}!")


# Эквивалентно прямому переопределению функции
hello1 = real_decorator(hello1)

print("______________________________________________")


def like_decor(func, *args, **kwargs):
    return func(*args, **kwargs)


# some_func = like_decor(some_func("arg1", "arg2"))
# Ты говоришь вызови сейчас же функцию like_decor(some_func) с параметром передавая функцию, но не передав аргументы! И результат её выполнения сохрани в переменную some_func.
# Будет ошибка и это не декоратор! Для декоратора нужна функция wrapper внутри декоратора, которая подменит декорируемую собой.
# Правильно будет так:


def decor(func):
    def wrapper(*args, **kwargs):
        print("Before call")
        result = func(*args, **kwargs)
        print("After call")
        return result

    return wrapper


# ручное применение
some_func = decor(some_func)


# Или лучше при определении функции так -
@decor
def some_func():
    print("Doing something")
