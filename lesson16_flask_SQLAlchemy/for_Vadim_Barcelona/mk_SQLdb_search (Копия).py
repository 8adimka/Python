from flask import Flask
import sqlite3

# with open ('/home/v/Python/lesson16_flask_SQLAlchemy/for_Vadim_Barcelona/calendar.csv') as file:
#     calendar_dict = {}
#     calendar_list = []
#     for row in file:
#         calendar_list.append(row.replace('\n', ''))
        
#     for i in range (0, len(calendar_list)):
#         if i == 0:
#             column_list = calendar_list[0].split(',')
#             for num in range (0,len(column_list)):
#                 calendar_dict [column_list[num]] = ''
                
#         else:
#             inner_list = calendar_list[i].split(',')
#             for num in range (7):
#                 calendar_dict [column_list[num]] += f", {calendar_list[num]}"

#     print (calendar_dict)
    
import csv

# Интересно, но начнём сначала!
# Подключение к базе данных
conn = sqlite3.connect('/home/v/Python/lesson16_flask_SQLAlchemy/for_Vadim_Barcelona/barcelona_vadim.db')
cursor = conn.cursor()

# Создайте таблицу (обновите столбцы под ваши данные)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS table_barcelona (
        if INTEGER, PRIMARY KEY, AUTOINCREMENT,
        column2 INTEGER,
        column3 REAL
    )
''')

# Открытие CSV файла
with open('your_file.csv', 'r', encoding='utf-8') as file:
    csv_reader = csv.reader(file)
    header = next(csv_reader)  # Пропускаем заголовок, если он есть

    # Вставка данных из CSV в таблицу
    for row in csv_reader:
        cursor.execute('''
            INSERT INTO table_name (column1, column2, column3)
            VALUES (?, ?, ?)
        ''', row)

# Сохранение изменений и закрытие
conn.commit()
conn.close()

print("Данные успешно импортированы!")
        