def prime_factors(n):
    divider = 2
    result_list = []
    result_string = ''
    while n > 1:
        if n%divider == 0:
            n = n//divider
            result_list.append(divider)
        else:
            divider += 1

    degree = 0
    current = result_list[0]

    for i in range(len(result_list)):
        if result_list[i] == current:
            degree += 1
        else:
            if degree > 1:
                result_string += '({}**{})'.format(current, degree)
                degree = 1
                current = result_list[i]
            else:
                result_string += '({})'.format(current)
                degree = 1
                current = result_list[i]
    if degree > 1:
        return result_string + '({}**{})'.format(current, degree)
    return result_string + '({})'.format(current)
         

print (prime_factors (2))


