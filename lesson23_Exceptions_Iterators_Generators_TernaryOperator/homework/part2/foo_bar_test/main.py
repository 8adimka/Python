# Вам дана обычная функция foo, перепишите ее на лямбду функцию.

def foo(n):
    for i in range(n):
        yield i**2

if __name__ == "__main__":
    print([x for x in foo(5)])
