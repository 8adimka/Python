# def calculate_total(*params):
#     return sum(params)


# print(calculate_total(5, 10))

# print(calculate_total(5, 10, 5))


# def display_info(**kwargs):
#     return f"name: {kwargs.get('name', 'Unknown')}, age: {kwargs.get('age', 0)}."


# print(display_info(profession="programmer", range="middle", name="Alice", age=30))

# a = {"name": "Bob", "age": 25}

# print(a["name"])


# def print_func(required_param=None, *args, **kwargs):
#     if required_param:
#         print(f"Required param accepted: {required_param}")

#         for arg in args:
#             print(arg)

#         for key, value in kwargs.items():
#             print(f"{key}: {value}")

#     else:
#         print("No required param provided.")


# print_func(True, 1, 2, 3, name="Charlie", age=28)

# print_func(1)
# print_func()


def some_func(a, b, c):
    return a + b + c


# my_list1 = (1, 2, 3)
my_list2 = {"a": 5, "b": 2, "c": 3}

# print(some_func(*my_list1))
# print(some_func(my_list1[0], my_list1[1], my_list1[2]))

# print(some_func(*my_list1))

print(some_func(**my_list2))
print(some_func(a=my_list2["a"], b=my_list2["b"], c=my_list2["c"]))
