def like_decor(func):
    print("before func")
    func()
    print("after func")


# like_decor(func1)


def decor(func):
    def wrapper():
        print("before func")
        func()
        print("after func")

    return wrapper


@decor
def func1():
    print("Hello, world!")


func1()
