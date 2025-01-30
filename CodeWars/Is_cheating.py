def remov_nb(n):
    num_list = [num for num in range (1,n+1)]
    sum_list = sum(num_list)
    result_list = []
    for a in num_list:
        for b in num_list:
            if a != b:
                if (sum_list-a-b) == a*b:
                    result_list.append((a, b))
    return result_list

print (remov_nb(101))
print (remov_nb(2))
print (remov_nb(26))
