import copy

some_dict = {'green':'go', 'yellow':'go faster', 'red':['stop', 'smile']}

print (some_dict)

some_dict_copy1 = some_dict.copy()
some_dict_copy1['red'][1] = 'not smile'

print(some_dict)

# some_dict_copy2 = some_dict[:] -> Не работает!

red_copy = some_dict['red']
red_copy[0] = 'gogogo'

print(red_copy)

print(some_dict)

def buggy1 (a, res = []):
    res.append(a)
    print(res)
    return res

buggy1('to_list')
r = buggy1('5')

print(r)

def buggy2 (a, res = [1,'in_list']):
    res.append(a)
    print(res)
    return res

buggy2('to_list')
r = buggy2('5')

print(r)

def not_buggy (arg, result=None):
    if result is None:
        result = []
    result.append(arg)
    print (result)
    return result

not_buggy('to_list')
not_buggy(1)
not_buggy(2)
r = not_buggy('5')

print(r)


class Buggy ():
    def __init__ (self, res=[1, '2']):
        self.res = res

    def add_some (self, a):
        self.res.append(a)
        print(self.res)
        return self.res

class Not_buggy ():
    def __init__ (self, res=None):
        self.res = res if res is not None else []

    def add_some (self, a):
        self.res.append(a)
        print(self.res)
        return self.res

not_bug = Not_buggy()
not_bug.add_some('to_list')
not_bug.add_some('to_list2')
not_bug.add_some('3')
r=not_bug.add_some(4)

print (not_bug.res)
print ('_________________________________________________')


from functools import wraps

def my_decorator (arg):
    def real_decorator (func):
        @wraps(func)  # 🎯 копирует имя, докстринг, аннотации и т.д.
        def wrapper (*args, **kwargs):
            print ('До вызова функции')
            func(*args, **kwargs)
            print(f'После вызова функции печатаем аргумент декоратора - {arg}')
        return wrapper
    return real_decorator

@my_decorator("🎉 Это аргумент декоратора!")
def some_func (a,b):
    print(f'Во время выполнения функции,\nпечатаем {a} и {b}')

some_func('Аргументы', 5)


print ('_________________________________________________')

def real_decorator (func):
    @wraps(func)  # 🎯 копирует имя, докстринг, аннотации и т.д.
    def wrapper (*args, **kwargs):
        print ('До вызова функции')
        func(*args, **kwargs)
        print(f'После вызова функции!')
    return wrapper


@real_decorator
def some_func (a,b=5):
    print(f'Во время выполнения функции,\nпечатаем {a} и {b}')

some_func('Аргументы')

def repeat(n=5):
    def decorator(func):
        @wraps(func)  # 🎯 копирует имя, докстринг, аннотации и т.д.
        def wrapper(*args, **kwargs):
            for i in range(n):
                func(*args, **kwargs)
        return wrapper
    return decorator

@repeat(2)
def hello(name):
    print(f"Hello, {name}!")

hello("Vadim")

def hello(name='Julia'):
    print(f"Hello, {name}!")

repeat(1)(hello)()
repeat(3)(hello)("Max")

# 🔄 Разовая обёртка — вызови декоратор вручную:
wrapped_hello = repeat(3)(hello)  # сначала repeat(3) → вернёт декоратор → вызываем с hello

# вызов
wrapped_hello()

