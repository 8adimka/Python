class MyClass:
    cls_var = 42  # class variable

    def __init__(self, x=[]):  # x initialize here and all class_instansec will share it
        self.x = x  # instance variable (object attribute for all instances)


class MyClass:
    cls_var = 42  # class variable

    def __init__(self, x=None):
        if x is None:
            x = []
        self.x = x  # instance variable


VALUES2: list[int] = [1, 2, 3]


def extend_me2[T](values: list[T]):
    values = values.extend(values)


extend_me2(VALUES2)
print(VALUES2)
