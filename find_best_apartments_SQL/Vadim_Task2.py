from flask import Flask
import sqlite3
import csv

file_path = '/home/v/Python/lesson16_flask_SQLAlchemy/for_Vadim_Barcelona/listings.csv'

# Подключение к базе данных
with sqlite3.connect("/home/v/Python/lesson16_flask_SQLAlchemy/for_Vadim_Barcelona/barcelona_vadim3.db") as connection:
    cursor = connection.cursor()
    # Создаём таблицу
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
        
file_pathes = ['/home/v/Python/lesson16_flask_SQLAlchemy/for_Vadim_Barcelona/reviews.csv',
               '/home/v/Python/lesson16_flask_SQLAlchemy/for_Vadim_Barcelona/calendar.csv']

# Подключение к базе данных
with sqlite3.connect("/home/v/Python/lesson16_flask_SQLAlchemy/for_Vadim_Barcelona/barcelona_vadim3.db") as connection:
    cursor = connection.cursor()   
    
    # Создаём таблицу
    for file_path in file_pathes:
        table_name = file_path.split('/')[-1].split('.')[0]

        # Открытие CSV файла
        with open(file_path, 'r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            header = next(csv_reader)  # Пропускаем заголовок, если он есть            
            
            # Формируем список столбцов таблицы и создаём таблицу
            columns = ' TEXT, '.join(header) + ' TEXT, FOREIGN KEY (listing_id) REFERENCES listings(id)'
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
                
            index_query = """CREATE INDEX id_indx ON listings (id); CREATE INDEX price_indx ON listings (price);"""
            cursor.executescript(index_query)
            connection.commit()
            
print ('Данные успешно добавлены в Базу Данных')
            
# После создалия базы данных находим ТОП-10 предложений
with sqlite3.connect("/home/v/Python/lesson16_flask_SQLAlchemy/for_Vadim_Barcelona/barcelona_vadim3.db") as connection:
    cursor = connection.cursor()
    query = """SELECT DISTINCT listings.id, 
                listings.name,
                listings.number_of_reviews,
                listings.price,
                CAST(REPLACE(REPLACE(listings.price, '$', ''), ',', '') AS REAL) AS listing_price,
                calendar.price,
                CAST(REPLACE(REPLACE(calendar.price, '$', ''), ',', '') AS REAL) AS calendar_price,
                listings.review_scores_rating AS review_rating
                FROM listings
                JOIN reviews ON listings.id = reviews.listing_id
                JOIN calendar ON listings.id = calendar.listing_id
                WHERE listings.review_scores_rating IS NOT NULL 
                AND listings.price != '' 
                AND listings.price IS NOT NULL 
                AND calendar.price IS NOT NULL 
                AND listings.price NOT LIKE '0.0%' 
                AND calendar.price NOT LIKE '0.0%'
                AND CAST(REPLACE(REPLACE(listings.price, '$', ''), ',', '') AS REAL) < 800
                AND CAST(REPLACE(REPLACE(listings.price, '$', ''), ',', '') AS REAL) > 25
                ORDER BY listings.review_scores_rating DESC, CAST(listings.number_of_reviews AS REAL) DESC,
                CAST(REPLACE(REPLACE(listings.price, '$', ''), ',', '') AS REAL) ASC
                LIMIT 10"""
    cursor.execute(query)
    
    for row in cursor.fetchall():
        print (row)
        
# WHERE listings.review_scores_rating IS NOT NULL AND listings.price != '' AND listings.price IS NOT NULL AND calendar.price IS NOT NULL AND listings.price NOT LIKE '0.0%' AND calendar.price NOT LIKE '0.0%'

# """SELECT DISTINCT listings.id, 
#                 listings.name,
#                 listings.price AS listing_price,
#                 calendar.price AS calendar_price,
#                 listings.review_scores_rating AS review_rating
#                 FROM listings
#                 JOIN reviews ON listings.id = reviews.listing_id
#                 JOIN calendar ON listings.id = calendar.listing_id
#                 WHERE listings.review_scores_rating IS NOT NULL AND listings.price != '' AND listings.price IS NOT NULL AND calendar.price IS NOT NULL AND listings.price NOT LIKE '0.0%' AND calendar.price NOT LIKE '0.0%'
#                 AND CAST(listings.price AS REAL) < 800
#                 ORDER BY listings.review_scores_rating DESC, listings.price ASC
#                 LIMIT 10"""

        