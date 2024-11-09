# with open(r'C:\Users\m8adi\Desktop\Python\Test_2\shopping_list.txt', 'r', encoding='utf-8') as file:
#     # работа с файлом
#     secret_word = file.read()  # Читаем содержимое файла
#     print("Секретное слово:", secret_word)


while True:
    start = input ('Вы готовы ввести свой вес?\n1 - Да. 2 - Выйти\n->')
    if start == '1':
        with open (r'C:\Users\m8adi\Desktop\Python\Test_2\Weight', 'a', encoding='utf-8') as file:
            player_input = input ('Введите ваш вес: ')
            file.write (f'{player_input}\n')
    else:
        print ('Bye!')
        break

 

# with open(r'C:\Users\m8adi\Desktop\Python\Test_2\Weight', 'r', encoding='utf-8') as file:
#     # Читаем все строки и находим максимальный вес
#     weight_max = int(max(file.readlines()))
    
#     # Возвращаем указатель в начало файла
#     file.seek(0)

#     # Переменные для анализа постоянного сбрасывания веса
#     slim = True
    
#     # Проходим по строкам снова
#     for line in file:
#         if line.strip():  # Проверяем, что строка не пустая
#             current_weight = int(line.strip())  # Преобразуем строку в число
        
#         # Сравниваем с предыдущим весом
#         if current_weight < weight_max:
#             weight_max = current_weight
#         elif current_weight > weight_max:
#             print(f'Вес стал больше: до {current_weight} после {weight_max}')
#             weight_max = current_weight
#             slim = False
    
#     # Выводим результат
#     if slim:
#         print("Каждый раз получалось сбрасывать вес")


with open(r'C:\Users\m8adi\Desktop\Python\Test_2\Weight', 'r', encoding='utf-8') as file:
    # Читаем все строки один раз и сохраняем в переменную
    lines = file.readlines()

    # Найдем максимальный вес, игнорируя пустые строки
    weight_max = int(max(line.strip() for line in lines if line.strip()))

    # Переменные для анализа постоянного сбрасывания веса
    slim = True

    # Проходим по строкам снова, используя уже сохраненные строки
    for line in lines:
        if line.strip():  # Проверяем, что строка не пустая
            current_weight = int(line.strip())  # Преобразуем строку в число

            # Сравниваем с предыдущим весом
            if current_weight < weight_max:
                weight_max = current_weight
            elif current_weight > weight_max:
                print(f'Вес стал больше: до {current_weight} после {weight_max}')
                weight_max = current_weight
                slim = False

    # Выводим результат
    if slim:
        print("Каждый раз получалось сбрасывать вес")
    


