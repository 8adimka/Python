# with open (r'C:\Users\m8adi\Desktop\Python\Curs 2.Lecture 1\test_3.txt', 'r') as file:
#     list_num = [int(line.strip()) for line in file]
#     sum_ = sum(list_num)
#     media_ = sum_/len(list_num)
#     print (f'Сумма: {sum_}\nСреднее: {media_}')


# def load_list_from_file(file_name):
#     with open (file_name, 'r') as file:
#         return [int(line.strip()) for line in file]
# print (load_list_from_file(r'C:\Users\m8adi\Desktop\Python\Curs 2.Lecture 1\test_3.txt'))


# def load_list_from_file_2(file_name):
#     with open (file_name, 'r') as file:
#         dict_lines = {}
#         for line in file:
#             parts = line.strip().split()
#             dict_lines [int(parts[0])] = parts[-1]
#     return dict_lines
# print (load_list_from_file_2 (r'C:\Users\m8adi\Desktop\Python\Curs 2.Lecture 1\test_4.txt'))


# with open (r'C:\Users\m8adi\Desktop\Python\Curs 2.Lecture 1\user_input.txt', 'a') as file:
#     for i in range (3):
#         file.write (input('Введите, то, что запишем в файл: ') + '\n')


# with open (r'C:\Users\m8adi\Desktop\Python\Curs 2.Lecture 1\test_3.txt', 'r') as file:
#     lines = file.readlines()


# with open (r'C:\Users\m8adi\Desktop\Python\Curs 2.Lecture 1\info.txt', 'a') as file:
#     number_list = [int(line.strip()) for line in lines]
#     file.write (str(min(number_list))+'\n')
#     file.write (str(max(number_list))+'\n')
#     file.write (str(sum(number_list))+'\n')   
# with open (r'C:\Users\m8adi\Desktop\Python\Curs 2.Lecture 1\info.txt', 'r') as file:
#     for mile in file.readlines():
#         print (mile)



# for i in range (3):
#     with open (r'C:\Users\m8adi\Desktop\Python\Curs 2.Lecture 1'+f'\{str(i+1)}'+'.txt', 'w') as file:
#         file.write ('файл создан')

# user_name = input ('Введите название файла: ')

# try:
#     with open (fr'C:\Users\m8adi\Desktop\Python\Curs 2.Lecture 1\{user_name}.txt') as file:
#         print ('файл существует')

# except FileNotFoundError:
#     print ('не существует')



# import os

# # Создание файлов
# base_path = r'C:\Users\m8adi\Desktop\Python\Curs 2.Lecture 1'

# for i in range(3):
#     file_path = os.path.join(base_path, f'{i+1}.txt')
#     with open(file_path, 'w') as file:
#         file.write('файл создан')

# # Получение названия файла от пользователя
# user_name = input('Введите название файла: ')

# # Формируем путь к файлу
# file_path = os.path.join(base_path, f'{user_name}.txt')

# # Проверка на существование файла
# if os.path.exists(file_path):
#     print('файл существует')
# else:
#     print('не существует')


# with open (r'C:\Users\m8adi\Desktop\Python\Curs 2.Lecture 1\exp_1.txt', 'w') as file:
#     file.write ('''1500
# 750''')
# with open (r'C:\Users\m8adi\Desktop\Python\Curs 2.Lecture 1\exp_2.txt', 'w') as file:
#     file.write ('''1350
# 1100
# 800''')

# with open (r'C:\Users\m8adi\Desktop\Python\Curs 2.Lecture 1\exp_1.txt', 'r') as file:
#     sum_list = [int(line.strip()) for line in file]

# with open (r'C:\Users\m8adi\Desktop\Python\Curs 2.Lecture 1\exp_2.txt', 'r') as file:
#     for line in file:
#         sum_list.append (int(line.strip()))

# sum_total = sum(sum_list)
# print (sum_total)



# Запись данных в файлы и их создание
path = r'C:\Users\m8adi\Desktop\Python\Curs 2.Lecture 1\\'
with open(fr'{path}exp_1.txt', 'w') as file:
    file.write('''1500
750''')

with open(fr'{path}exp_2.txt', 'w') as file:
    file.write('''1350
1100
800''')

# Чтение расходов из файлов и получение общей суммы
files = [fr'{path}exp_1.txt', 
         fr'{path}exp_2.txt']

sum_list = []
for file_path in files:
    with open(file_path, 'r') as file:
        sum_list.extend([int(line.strip()) for line in file])

sum_total = sum(sum_list)
print(f'Общая сумма расходов: {sum_total}')
