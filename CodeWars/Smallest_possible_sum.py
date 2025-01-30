from math import gcd # Находит Наибольший общий делитель (среди всех ПЕРЕДАННЫХ чисел) math.gcd (9,6,12,18)

def solution(lst):
    return gcd(*lst) * len(lst)

# def solution(lst):
#     while min(lst) < max(lst):
#         for i in (range (len(lst))):
#             while lst[i] > min(lst):
#                 lst[i] = lst[i] - min(lst)
#     return sum(lst)


# from math import gcd
# from functools import reduce

# def solution(X):
#     # Находим НОД (наибольший общий делитель) всех чисел в массиве
#     common_gcd = reduce(gcd, X)
#     # Возвращаем сумму НОД, умноженного на длину массива
#     return common_gcd * len(X)


print (solution([9])) #== 9
print (solution([6, 9, 21])) #== 9
print (solution([1, 21, 55])) #== 3
print (solution([55, 21, 1])) #== 3
print (solution([12, 12, 12, 12, 12, 24, 24, 12, 36, 36, 48])) #== 132
num = solution([3, 6, 1, 7, 6, 98, 8, 99])
print (num)
print('_____________________')
print(gcd (9,6,12,18))