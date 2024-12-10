import sqlite3

db_path = r"/home/v/Python/lesson15_SQL/home_work/animal.db"

#Продолжаем приводить таблицы к нормальному виду
#Далее нас не устраивает вид ячейки date_of_birth изменим его на тип DATE

with sqlite3.connect(db_path) as con:
    cur = con.cursor ()

    #1. Добавляем новый столбец с типом DATE для хранения отформатированных данных
    cur.execute("""ALTER TABLE animals
                ADD COLUMN date_of_birth_formatted DATE""")
    
    #2. Меняем тип данных из старого столбца и обновляем данные в новом столбце 
    cur.execute("""UPDATE animals
                SET date_of_birth_formatted = DATE (date_of_birth)""")
    
    #3. Удалим старый столбец и переименуем новый
    # Для этого создадим новую таблицу без старого столбца и перенесем данные
    cur.execute("""CREATE TABLE animals_new AS
                SELECT 
                animal_id, 
                animal_type_id,
                name,
                breed_id,
                color1,
                color2,
                date_of_birth_formatted AS date_of_birth
                FROM animals""")

    #4. Удаляем старую таблицу и переименовываем новую
    cur.executescript("""DROP TABLE animals;
    ALTER TABLE animals_new RENAME TO animals;""")


