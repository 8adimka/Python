def sum_strings(a, b):
    # Удаляем начальные нули, если они есть
    a = a.lstrip('0')
    b = b.lstrip('0')
    
    # Делаем строки одинаковой длины, добавляя ведущие нули к более короткой строке
    max_len = max(len(a), len(b))
    a = a.zfill(max_len)
    b = b.zfill(max_len)
    
    carry = 0  # Перенос
    result = []
    
    # Сложение с конца к началу
    for i in range(max_len - 1, -1, -1):
        digit_sum = int(a[i]) + int(b[i]) + carry
        carry = digit_sum // 10  # Вычисляем перенос
        result.append(str(digit_sum % 10))  # Добавляем последнюю цифру суммы в результат
    
    # Если после завершения сложения остался перенос
    if carry:
        result.append(str(carry))
    
    # Переворачиваем список и объединяем в строку
    if result == []:
        return '0'
    return ''.join(result[::-1])

# Пример использования:
print(sum_strings('123456789123456789', '987654321987654321'))  # => '1111111111111111110'

print(sum_strings('0', '000'))
print(sum_strings('02', '0003'))

print(sum_strings('', ''))


def sum_strings(x, y):
    print(f"{x} {y}")
    if x == "":
        x = 0
    else:
        x = int(x)
    if y == "":
        y = 0
    else: 
        y = int(y)
    return str(x+y)


# Пример использования:
print(sum_strings('123456789123456789', '987654321987654321'))  # => '1111111111111111110'

print(sum_strings('0', '000'))
print(sum_strings('02', '0003'))

print(sum_strings('', ''))
