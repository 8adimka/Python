from flask import Flask
import sqlite3
import csv

file_pathes = ['/home/v/Python/lesson16_flask_SQLAlchemy/for_Vadim_Barcelona/listings.csv',
               '/home/v/Python/lesson16_flask_SQLAlchemy/for_Vadim_Barcelona/reviews.csv',
               '/home/v/Python/lesson16_flask_SQLAlchemy/for_Vadim_Barcelona/calendar.csv']

data_base_name = "/home/v/Python/lesson16_flask_SQLAlchemy/for_Vadim_Barcelona/barcelona_vadim2.db"

# Подключение к базе данных
with sqlite3.connect(data_base_name) as connection:
    cursor = connection.cursor()   
    
    # Создаём таблицу
    for file_path in file_pathes:
        table_name = file_path.split('/')[-1].split('.')[0]

        # Открытие CSV файла
        with open(file_path, 'r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            header = next(csv_reader)  # Пропускаем заголовок, если он есть            
            
            # Формируем список столбцов таблицы и создаём таблицу
            columns = ' TEXT, '.join(header) + ' TEXT'
            query = f'CREATE TABLE IF NOT EXISTS {table_name} ({columns})'
            cursor.execute(query)
            connection.commit()
            
            # Формируем запрос к базе данных
            columns = ', '.join(header)
            placeholders = ', '.join(['?'] * len(header))
            insert_query = f'INSERT INTO {table_name} ({columns}) VALUES ({placeholders})'
            
            # Вставка данных из CSV в таблицу
            for row in csv_reader:
                cursor.execute(insert_query, row)
            connection.commit()


