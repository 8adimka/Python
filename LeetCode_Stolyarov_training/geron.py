from math import sqrt


def geron(a: int, b: int, c: int) -> float:
    p = (a + b + c) / 2
    return sqrt(p * (p - a) * (p - b) * (p - c))


print(geron(3, 4, 5))


def remove_symbols(string, *symbols):
    for sym in symbols:
        string = string.replace(sym, "")
    return string


print(remove_symbols("Hello, World!", ",", "!"))  # Hello World

print(remove_symbols("Hello, World!", *",! WHl"))  # Hello World
