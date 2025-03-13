def arr_generator(arr):
    for item in arr:
        yield item


arr = [1, 2, 3, 4, 5]

it = iter(arr)
print(next(it))
print(next(it))
print(next(it))

gen = arr_generator(arr)
print(next(gen))
print(next(gen))
print(next(gen))
