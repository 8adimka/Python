def high_and_low(numbers):
    # num_list = [int(x) for x in numbers.split(' ')]
    num_list = list (map (int, numbers.split(' ')))
    return f"{max(num_list)} {min(num_list)}"

print (high_and_low("8 3 -5 42 -1 0 0 -9 4 7 4 -4"))
print (high_and_low("1 2 3"))
