import re
from functools import wraps
from typing import Callable, Optional

text_1 = """1.181.2.178 [17/May/2015:20:05:36] "GET / HTTP/1.1" 200
1.125.2.148 [17/May/2015:20:05:19] "GET /?flav=rss20 HTTP/1.1" 200
1.170.2.204 [17/May/2015:20:05:03] "POST /?flav=atom HTTP/1.1" 200
1.163.30.77 [17/May/2015:20:05:36] "GET /images/gle.png HTTP/1.1" 200
1.163.30.77 [17/May/2015:20:05:37] "GET /blog/dot.html HTTP/1.1" 200"""

text_2 = "Команда regex принимает в качестве аргумента регулярное выражение, по которой нужно будет фильтровать строки входных данных. -> посчитай колличество слов"


reg_exp_1 = r"\d{1,3}\.\d{3}\.\d{1,3}\.\d{1,3}"

result = re.findall(reg_exp_1, text_1)
ip = re.match(reg_exp_1, text_1)

print(result)
if ip:
    print(ip.group())

reg_exp_2 = r"\b\w+\b"

res = re.findall(reg_exp_2, text_2)

print(len(res))


def compose(*args, res=None):
    for f in reversed(args):
        if callable(f):
            res = f(res)

    return res


def right_compose(*args):
    def inner(*args_inner):
        for f in reversed(args):
            if callable(f):
                x = f(*args_inner)
        return x

    return inner


def calllimit(limit: int = 1, callback: Optional[Callable] = None):
    def outer(func: Callable):
        counter = 0

        @wraps(func)
        def inner(*args):
            nonlocal counter
            if counter < limit:
                counter += 1
                return func(*args)
            elif callback and callable(callback):
                return callback()
            else:
                return "no result"

        return inner

    return outer


def other_foo():
    return "other_result"


@calllimit(2, other_foo)
def foo():
    return "get_result"


print(foo())
print(foo())
print(foo())
print(foo())


def editable(str_1, str_2):
    if abs(len(str_1) - len(str_2)) > 1:
        return False

    elif len(str_1) == len(str_2):
        counter = [1 for a, b in zip(str_1, str_2) if a != b]
        if len(counter) > 1:
            return False
        return True

    elif len(str_1) + 1 == len(str_2):
        i = 0
        while i < len(str_1):
            if str_1[i] != str_2[i]:
                str_2 = str_2[:i] + str_2[i + 1 :]
                if str_1 == str_2:
                    return True
                return False
            i += 1
        return True

    elif len(str_1) == len(str_2) + 1:
        return editable(str_2, str_1)


print(editable("pale", "ple"))
print(editable("pales", "pale"))
print(editable("pale", "bale"))
print(editable("pale", "bake"))
print(editable("pale", "bakeesad"))
print(editable("bakeesad", "pale"))


def compress(nums: list) -> str:
    if not nums:
        return ""

    res = f"{nums[0]}"

    i = 0
    solo = True

    for num in nums[1:]:
        if num != nums[i] + 1:
            if solo:
                res += f",{num}"
                i += 1
            else:
                res += f"-{nums[i]},{num}"
                solo = True
                i += 1
        else:
            i += 1
            solo = False
            if i == len(nums) - 1:
                res += f"-{nums[i]}"

    return res


print(compress([1, 2, 3, 5, 6, 8, 9, 10, 11, 12, 14]))
print(compress([2, 4, 1, 2, 3, 11, 12]))
print(compress([1, 3, 5, 6]))
