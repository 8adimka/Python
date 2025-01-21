#128.32.10.1 == 10000000.00100000.00001010.00000001
#2149583361 ==> "128.32.10.1"

def int32_to_ip(int32):
    bites = f'{int32:032b}'
    num_list = [f'{bites[0:8]}',f'{bites[8:16]}',f'{bites[16:24]}', f'{bites[24:32]}']
    number_list = []
    for num in num_list:
        number = 0
        for index, letter in enumerate(num):
            number += int(letter) * (2 ** (7 - index))
        number_list.append(number)
    return '.'.join(map(str, number_list))

print (int32_to_ip(2149583361))