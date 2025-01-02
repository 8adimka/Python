# def my_max(items):
#     current_max = items[0]

#     for index in range(1, len(items)):
#         item = items[index]
#         if item > current_max:
#             current_max = item

#     return current_max

# the_max = my_max([99, 1, 0, -99, -1])
# print(the_max)

a = True

if a:
    print("Значение Истина")
else:
    print("Значение Ложь")


try:
	user_input = int(input('Введите  число: '))
	result = 1 / user_input
except ValueError:
	print("Неверный ввод")
except ZeroDivisionError:
	print("Деление на ноль")
else:
	print(f"Результат: {result}")
finally:
	print("Выполнить в любом случае")


