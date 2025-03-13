
def maximize_expression_operators (array:list):
    max_value = array[0]
    min_value = array[0]
    for indx in range (1, len(array)):
        res_array = [max_value+array[indx], max_value-array[indx], max_value*array[indx],
                      min_value+array[indx], min_value-array[indx], min_value*array[indx]]
        if array[indx] != 0:
            res_array.append(max_value/array[indx])
            res_array.append(min_value/array[indx])
        max_value = max(res_array)
        min_value = min(res_array)
    return max_value

print (maximize_expression_operators([1.5, 2, 3]))

