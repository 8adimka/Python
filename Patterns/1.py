import json
from functools import wraps
from typing import Callable

# Написать функцию, которая вернет строку, где поля не содержат пустых и null значений

data = """{
"name": "Alex",
"age": 25,
"address": "",
"phone_number": null
}"""


def clearer(data: str) -> str:
    obj = json.loads(data)
    res = {k: v for k, v in obj.items() if v not in ["", None]}

    return json.dumps(res)


print(clearer(data))


def get_fitst_match(func, objects: list = None) -> int:
    if objects == None:
        objects = []
    matching_obj = (obj for obj in objects if func(obj))

    res = next(matching_obj, None)
    return res


print(get_fitst_match(lambda x: x in [1, 7], [2, 3, 4, 7, 1, 6]))


def decorator(exceptions: list[tuple[Exception, Callable[[], None]]]):
    def decor(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                res = func()
            except Exception as error:
                for exception in exceptions:
                    if error in exception:
                        error[1]()
                        raise error
            return res

        return wrapper

    return decor


class Stack:
    def __init__(self):
        self.min_stack = []
        self.stack = []

    def push(self, value):
        if value:
            self.stack.append(value)
            if not self.min_stack or self.min_stack[-1] >= value:
                self.min_stack.append(value)

    def top(self):
        return self.stack[-1] if self.stack else None

    def pop(self):
        if self.stack:
            res = self.stack.pop()
            m = self.min_stack[-1]
            if res == m:
                del self.min_stack[-1]
            return res

    def get_min(self):
        return self.min_stack[-1]


s = Stack()

s.push(2)
s.push(2)
s.push(3)
s.push(4)
s.push(5)
s.push(2)
s.push(1)
print(f"Min_value: {s.get_min()}")
print(f"remove {s.pop()}")
print(f"remove {s.pop()}")
print(f"remove {s.pop()}")
print(f"Min_value: {s.get_min()}")

l = [1, 0, 2, 3, 4, 0, 5, 6]
clear_l_gen = (i if i != 0 else -1 for i in l)

print(list(clear_l_gen))


def even_nums(n: int) -> list[int] | list[None]:
    if n:
        return [x for x in range(n + 1) if x % 2 == 0 and x != 0]
    return []


print(even_nums(7))
print(even_nums(6))
print(even_nums(0))
print(even_nums(1))
