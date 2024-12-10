from flask import Flask
import sqlite3
import csv

with open ('/home/v/Python/lesson16_flask_SQLAlchemy/for_Vadim_Barcelona/reviews.csv') as file:
    calendar_dict = {}
    calendar_list = []
    for row in file:
        calendar_list.append(row.replace('\n', ''))
        
    for i in range (0, len(calendar_list)):
        if i == 0:
            column_list = calendar_list[0].split(',')
            print (column_list)
            for num in range (0,len(column_list)):
                calendar_dict [column_list[num]] = ''
                
        else:
            inner_list = calendar_list[i].split(',')
            for num in range (7):
                calendar_dict [column_list[num]] += f", {calendar_list[num]}"

    print (calendar_dict)

# Интересно (можно и так доделать), но начнём сначала по уму!


# Создаём listings. Подключение к базе данных
with sqlite3.connect("/home/v/Python/lesson16_flask_SQLAlchemy/for_Vadim_Barcelona/barcelona_vadim.db") as connection:
    cursor = connection.cursor()
    
    # cursor.execute("""DROP TABLE calendar""") #удаляем таблицу calendar, если нужно пересоздать
    # cursor.execute("""DROP TABLE listings""") #удаляем таблицу listings
    # cursor.execute("""DROP TABLE reviews""") #удаляем таблицу reviews
    
    # Создаём таблицу
    query = """
    CREATE TABLE IF NOT EXISTS listings (
        id INTEGER PRIMARY KEY,
        listing_url TEXT,
        scrape_id INTEGER,
        last_scraped TEXT,
        source TEXT,
        name TEXT,
        description TEXT,
        neighborhood_overview TEXT,
        picture_url TEXT,
        host_id INTEGER,
        host_url TEXT,
        host_name TEXT,
        host_since TEXT,
        host_location TEXT,
        host_about TEXT,
        host_response_time TEXT,
        host_response_rate TEXT,
        host_acceptance_rate TEXT,
        host_is_superhost TEXT,
        host_thumbnail_url TEXT,
        host_picture_url TEXT,
        host_neighbourhood TEXT,
        host_listings_count INTEGER,
        host_total_listings_count INTEGER,
        host_verifications TEXT,
        host_has_profile_pic TEXT,
        host_identity_verified TEXT,
        neighbourhood TEXT,
        neighbourhood_cleansed TEXT,
        neighbourhood_group_cleansed TEXT,
        latitude REAL,
        longitude REAL,
        property_type TEXT,
        room_type TEXT,
        accommodates INTEGER,
        bathrooms REAL,
        bathrooms_text TEXT,
        bedrooms INTEGER,
        beds INTEGER,
        amenities TEXT,
        price TEXT,
        minimum_nights INTEGER,
        maximum_nights INTEGER,
        minimum_minimum_nights INTEGER,
        maximum_minimum_nights INTEGER,
        minimum_maximum_nights INTEGER,
        maximum_maximum_nights INTEGER,
        minimum_nights_avg_ntm REAL,
        maximum_nights_avg_ntm REAL,
        calendar_updated TEXT,
        has_availability TEXT,
        availability_30 INTEGER,
        availability_60 INTEGER,
        availability_90 INTEGER,
        availability_365 INTEGER,
        calendar_last_scraped TEXT,
        number_of_reviews INTEGER,
        number_of_reviews_ltm INTEGER,
        number_of_reviews_l30d INTEGER,
        first_review TEXT,
        last_review TEXT,
        review_scores_rating REAL,
        review_scores_accuracy REAL,
        review_scores_cleanliness REAL,
        review_scores_checkin REAL,
        review_scores_communication REAL,
        review_scores_location REAL,
        review_scores_value REAL,
        license TEXT,
        instant_bookable TEXT,
        calculated_host_listings_count INTEGER,
        calculated_host_listings_count_entire_homes INTEGER,
        calculated_host_listings_count_private_rooms INTEGER,
        calculated_host_listings_count_shared_rooms INTEGER,
        reviews_per_month REAL
    )
    """
    cursor.execute(query)
    
    # Открытие CSV файла
    with open('/home/v/Python/lesson16_flask_SQLAlchemy/for_Vadim_Barcelona/listings.csv', 'r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        header = next(csv_reader)  # Пропускаем заголовок, если он есть

        # Вставка данных из CSV в таблицу
        for row in csv_reader:
            cursor.execute('''
                INSERT INTO listings (
                    id, listing_url, scrape_id, last_scraped, source, name, description, 
                    neighborhood_overview, picture_url, host_id, host_url, host_name, host_since, 
                    host_location, host_about, host_response_time, host_response_rate, 
                    host_acceptance_rate, host_is_superhost, host_thumbnail_url, host_picture_url, 
                    host_neighbourhood, host_listings_count, host_total_listings_count, 
                    host_verifications, host_has_profile_pic, host_identity_verified, 
                    neighbourhood, neighbourhood_cleansed, neighbourhood_group_cleansed, 
                    latitude, longitude, property_type, room_type, accommodates, bathrooms, 
                    bathrooms_text, bedrooms, beds, amenities, price, minimum_nights, 
                    maximum_nights, minimum_minimum_nights, maximum_minimum_nights, 
                    minimum_maximum_nights, maximum_maximum_nights, minimum_nights_avg_ntm, 
                    maximum_nights_avg_ntm, calendar_updated, has_availability, availability_30, 
                    availability_60, availability_90, availability_365, calendar_last_scraped, 
                    number_of_reviews, number_of_reviews_ltm, number_of_reviews_l30d, first_review, 
                    last_review, review_scores_rating, review_scores_accuracy, 
                    review_scores_cleanliness, review_scores_checkin, review_scores_communication, 
                    review_scores_location, review_scores_value, license, instant_bookable, 
                    calculated_host_listings_count, calculated_host_listings_count_entire_homes, 
                    calculated_host_listings_count_private_rooms, 
                    calculated_host_listings_count_shared_rooms, reviews_per_month
                )
                VALUES (
                    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 
                    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 
                    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
                )
            ''', row)
        connection.commit()
    
    
    # Альтернативный вариант    # Открытие CSV файла
    # with open('/home/v/Python/lesson16_flask_SQLAlchemy/for_Vadim_Barcelona/listings.csv', 'r', encoding='utf-8') as file:
    #     csv_reader = csv.reader(file)
    #     header = next(csv_reader)  # Пропускаем заголовок, если он есть

    #     # Проверим, что количество колонок в заголовке совпадает с таблицей
    #     if len(header) != 75:
    #         raise ValueError(f"Ожидается 75 столбцов, но в заголовке {len(header)} столбцов")

    #     # Вставка данных из CSV в таблицу
    #     for row in csv_reader:
    #         if len(row) == 75:  # Проверим, что строка содержит ровно 75 значений
    #             cursor.execute('''
    #                 INSERT INTO listings (
    #                     id, listing_url, scrape_id, last_scraped, source, name, description, 
    #                     neighborhood_overview, picture_url, host_id, host_url, host_name, host_since, 
    #                     host_location, host_about, host_response_time, host_response_rate, 
    #                     host_acceptance_rate, host_is_superhost, host_thumbnail_url, host_picture_url, 
    #                     host_neighbourhood, host_listings_count, host_total_listings_count, 
    #                     host_verifications, host_has_profile_pic, host_identity_verified, 
    #                     neighbourhood, neighbourhood_cleansed, neighbourhood_group_cleansed, 
    #                     latitude, longitude, property_type, room_type, accommodates, bathrooms, 
    #                     bathrooms_text, bedrooms, beds, amenities, price, minimum_nights, 
    #                     maximum_nights, minimum_minimum_nights, maximum_minimum_nights, 
    #                     minimum_maximum_nights, maximum_maximum_nights, minimum_nights_avg_ntm, 
    #                     maximum_nights_avg_ntm, calendar_updated, has_availability, availability_30, 
    #                     availability_60, availability_90, availability_365, calendar_last_scraped, 
    #                     number_of_reviews, number_of_reviews_ltm, number_of_reviews_l30d, first_review, 
    #                     last_review, review_scores_rating, review_scores_accuracy, 
    #                     review_scores_cleanliness, review_scores_checkin, review_scores_communication, 
    #                     review_scores_location, review_scores_value, license, instant_bookable, 
    #                     calculated_host_listings_count, calculated_host_listings_count_entire_homes, 
    #                     calculated_host_listings_count_private_rooms, 
    #                     calculated_host_listings_count_shared_rooms, reviews_per_month
    #                 )
    #                 VALUES (
    #                     ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 
    #                     ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 
    #                     ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
    #                 )
    #             ''', row)
    #         else:
    #             print(f"Пропущена строка: {row} - неправильное количество значений")
    #     connection.commit()



# Создаём reviews. Подключение к базе данных
with sqlite3.connect("/home/v/Python/lesson16_flask_SQLAlchemy/for_Vadim_Barcelona/barcelona_vadim.db") as connection:
    cursor = connection.cursor()
    
    # cursor.execute("""DROP TABLE calendar""") #удаляем таблицу calendar, если нужно пересоздать
    
    # Создаём таблицу
    query = """
    CREATE TABLE IF NOT EXISTS reviews (
        listing_id INTEGER,
        id INTEGER PRIMARY KEY,
        date DATE,
        reviewer_id INTEGER,
        reviewer_name VARCHAR (255),
        comments TEXT,
        FOREIGN KEY (listing_id) REFERENCES listing(id))
    )
    """
    cursor.execute(query)
    
    # Открытие CSV файла
    with open('/home/v/Python/lesson16_flask_SQLAlchemy/for_Vadim_Barcelona/reviews.csv', 'r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        header = next(csv_reader)  # Пропускаем заголовок, если он есть

        # Вставка данных из CSV в таблицу
        for row in csv_reader:
            cursor.execute('''
                INSERT INTO reviews (
                    listing_id, id, date, reviewer_id, reviewer_name, comments
                )
                VALUES (
                    ?, ?, ?, ?, ?, ?
                )
            ''', row)
        connection.commit()


   
# Подключение к базе данных
conn = sqlite3.connect('/home/v/Python/lesson16_flask_SQLAlchemy/for_Vadim_Barcelona/barcelona_vadim.db')
cursor = conn.cursor()

# Создаём таблицу
cursor.execute('''
    CREATE TABLE IF NOT EXISTS calendar (
        listing_id INTEGER,
        date DATE,
        available VARCHAR (20),
        price DECIMAL,
        adjusted_price FLOAT,
        minimum_nights INTEGER,
        maximum_nights INTEGER,
        FOREIGN KEY (listing_id) REFERENCES listing(id))
''')

# Открытие CSV файла
with open('/home/v/Python/lesson16_flask_SQLAlchemy/for_Vadim_Barcelona/calendar.csv', 'r', encoding='utf-8') as file:
    csv_reader = csv.reader(file)
    header = next(csv_reader)  # Пропускаем заголовок, если он есть

    # Вставка данных из CSV в таблицу
    for row in csv_reader:
        cursor.execute('''
            INSERT INTO calendar (listing_id, date, available, price, adjusted_price, minimum_nights, maximum_nights)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', row)

# Сохранение изменений и закрытие
conn.commit()
conn.close()

print("Данные успешно импортированы!")



        