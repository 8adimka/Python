import sqlite3

db_path = r"/home/v/Python/lesson15_SQL/home_work/animal.db"

#Продолжаем приводить таблицы к нормальному виду
#Далее надо избавится от повторяющихся значений в столбах по типу -Cat-Cat-Cat-Cat

with sqlite3.connect (db_path) as connection:
    cursor = connection.cursor()

#  1. Создаём таблицу animal_types
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS animal_types (
        animal_type_id INTEGER PRIMARY KEY AUTOINCREMENT,
        animal_type VARCHAR (20) NOT NULL UNIQUE
    );
    """)

# 2. Заполняем таблицу animal_types уникальными значениями из animals
    cursor.execute("""
    INSERT INTO animal_types (animal_type)
    SELECT DISTINCT animal_type
    FROM animals;
    """)


    # 3. Создаём новую таблицу animals с внешним ключом на animal_types
    cursor.execute("""
    CREATE TABLE animals_new (
        animal_id VARCHAR (20),
        animal_type_id INTEGER NOT NULL,
        name VARCHAR (20),
        breed VARCHAR (20),
        color1 VARCHAR (20),
        color2 VARCHAR (20),
        date_of_birth VARCHAR (20),
        FOREIGN KEY (animal_type_id) REFERENCES animal_types (animal_type_id)
    );
    """)

    # 4. Переносим данные из старой таблицы animals в animals_new
    cursor.execute("""
    INSERT INTO animals_new (animal_id, animal_type_id, name, breed, color1, color2, date_of_birth)
    SELECT 
        a.animal_id,
        at.animal_type_id,
        a.name,
        a.breed,
        a.color1,
        a.color2,
        a.date_of_birth
    FROM animals AS a
    JOIN animal_types AS at ON a.animal_type = at.animal_type;
    """)

    # 5. Удаляем старую таблицу animals
    cursor.execute("DROP TABLE animals;")

    # 6. Переименовываем новую таблицу animals_new в animals
    cursor.execute("ALTER TABLE animals_new RENAME TO animals;")

    connection.commit()

