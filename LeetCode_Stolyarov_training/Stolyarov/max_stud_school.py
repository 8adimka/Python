import os

def max_students_school ():
    # script_dir = os.getcwd()  # Текущая рабочая директория
    script_dir = os.path.dirname(__file__)  # Получаем папку скрипта
    file_path = os.path.join (script_dir, 'students.txt')

    with open (file_path, 'r', encoding='utf-8') as file:
        schools_list = [0 for i in range (67)]

        for line in file:
            num = int(line.split(' ')[0])//100
            if num <= 67:
                schools_list[(num)-1] += 1
            else:
                return 'Обнаружена Ошибка ввода!'

    return schools_list.index(max(schools_list))+1

print (max_students_school())
        



