list_array = [1, 2, 3, 4, 0, 5, 0]

res2 = [item**2 for item in list_array if 0 < item < 4] # Используем list-comprehension
print (res2) # [1, 4, 9]

res1 = [item if item else -1 for item in list_array] # Используем ternary оператор, если нужно "добавь ТО, else добавь ЭТО"
print (res1) # [1, 2, 3, 4, -1, 5, -1]




