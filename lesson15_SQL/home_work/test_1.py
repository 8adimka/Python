import sqlite3

db_path = r"/home/v/Python/lesson15_SQL/home_work/animal.db"

#Исправляем таблицу animals и приводим её к нормальному виду
with sqlite3.connect (db_path) as connection:
    cursor = connection.cursor()

#Создаём таблицу outcome_information со всеми столбцами, которые нас интересуют
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS outcome_information(
                outcome_id integer PRIMARY KEY AUTOINCREMENT,
                animal_id VARCHAR (10) NOT NULL,
                age_upon_outcome VARCHAR (20),
                outcome_subtype VARCHAR (20),
                outcome_type VARCHAR (20),
                outcome_month INTEGER,
                outcome_year INTEGER,
                FOREIGN KEY (animal_id) REFERENCES animal (animal_id)
                   )""")
#Копируем столбцы из animals в outcome_information
    cursor.execute("""
    INSERT INTO outcome_information (
        animal_id,
        age_upon_outcome,
        outcome_subtype,
        outcome_type,
        outcome_month,
        outcome_year)
    SELECT
        animal_id,
        age_upon_outcome,
        outcome_subtype,
        outcome_type,
        outcome_month,
        outcome_year
    FROM animals""")

#Далее Удаляем лишние столбцы из таблицы animals
    #Можно удалять столбцы так - cursor.execute("""ALTER TABLE animals DROP COLUMN outcome_subtype""")
    query =     """    
    -- 1. Но рекомендуемый способ удалить лишние столбцы - создать новую таблицу без ненужных колонок
    CREATE TABLE animals_new AS
    SELECT animal_id, animal_type, name, breed, color1, color2, date_of_birth
    FROM animals;

    -- 2. Удаляем старую таблицу
    DROP TABLE animals;

    -- 3. Переименовываем новую таблицу
    ALTER TABLE animals_new RENAME TO animals;
    """

    cursor.executescript(query)



