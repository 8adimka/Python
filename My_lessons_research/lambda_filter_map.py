# # lambda, map, filter, zip, enumerate, decorators

# # Lambda function example

# lambda x: x**2


# def square2(x):
#     return x**2


# print(square2(5))  # Output: 25

# data = "8asd@mail.ru , example@gmail.com,  test@example.com "

# map_r = map(lambda x: x.strip(), data.split(","))

# new_lst = list(map_r)

# print(new_lst)  # Output: ['8asd@mail.ru', 'example@gmail.com', 'test@example.com']

# my_lst = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# filter_r = filter(lambda x: x > 5, my_lst)

# new_filter_lst = list(filter_r)

# print(new_filter_lst)  # Output: [6, 7, 8, 9, 10]

# lastnames = ["Романов", "Иванов", "Сидоров"]

# res_samples = [31, 26, 42, 15, 18]

# zipped_r = zip(lastnames, res_samples)

# print(list(zipped_r))

# i = 1

# for name in lastnames:
#     print(i, name)
#     i += 1

# ______________________________________________________________________________


from functools import wraps


def decor(count=1):
    def inner(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print("Before calling the function")
            print(func(*args, **kwargs) * count)
            print("After calling the function")

        return wrapper

    return inner


@decor(count=3)
def my_func(*args, **kwargs):
    return f"Inside the function: we got {len(args)}"


my_func(4, 5, 6, 7, val=10)
