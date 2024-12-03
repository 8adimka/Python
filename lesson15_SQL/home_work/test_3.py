import sqlite3

db_path = r"/home/v/Python/lesson15_SQL/home_work/animal.db"

#Продолжаем приводить таблицы к нормальному виду
#Далее надо избавится от повторяющихся значений в столбце порода (breed)


with sqlite3.connect (db_path) as connection:
    cursor = connection.cursor()

    #  1. Создаём таблицу breed_types
    cursor.execute ("""CREATE TABLE IF NOT EXISTS breed_types(
                    breed_type_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    breed_type VARCHAR (20) NOT NULL UNIQUE)
                    """)
    
    # 2. Заполняем таблицу breed_types уникальными значениями из animals
    cursor.execute ("""INSERT INTO breed_types (breed_type)
                    SELECT DISTINCT breed
                    FROM animals
                    """)
    
    # 3. Создаём новую таблицу animals с внешним ключом на breed_types
    cursor.execute ("""CREATE TABLE new_animals (animal_id VARCHAR (20),
        animal_type_id INTEGER NOT NULL,
        name VARCHAR (20),
        breed_id INTEGER NOT NULL,
        color1 VARCHAR (20),
        color2 VARCHAR (20),
        date_of_birth VARCHAR (20),
        FOREIGN KEY (animal_type_id) REFERENCES animal_types (animal_type_id),
        FOREIGN KEY (breed_id) REFERENCES breed_types (breed_type_id))
""")    

    # 4. Переносим данные из старой таблицы animals в animals_new
    cursor.execute ("""
                    INSERT INTO new_animals (animal_id, animal_type_id, name, breed_id, color1, color2, date_of_birth)
                    SELECT
                        a.animal_id,
                        a.animal_type_id,
                        a.name,
                        bt.breed_type_id,
                        a.color1,
                        a.color2,
                        a.date_of_birth
                    FROM animals AS a
                    JOIN breed_types AS bt 
                    ON a.breed = bt.breed_type;
                    """)
    
        # 5. Удаляем старую таблицу animals
    cursor.execute("DROP TABLE animals;")

    # 6. Переименовываем новую таблицу animals_new в animals
    cursor.execute("ALTER TABLE new_animals RENAME TO animals;")


    connection.commit()

    # connection.commit() используется чтобы зафиксировать все изменения.
    # До этого момента изменения происходят в рамках транзакции и могут быть отменены (при вызове rollback())