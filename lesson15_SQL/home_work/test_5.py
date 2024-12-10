import sqlite3

db_path = r"/home/v/Python/lesson15_SQL/home_work/animal.db"

with sqlite3.connect(db_path) as con:
    cur = con.cursor ()

    cur.execute("""SELECT animals.name, animal_types.animal_type, breed_types.breed_type, outcome_information.outcome_month
                FROM animals
                JOIN outcome_information ON animals.animal_id = outcome_information.animal_id
                JOIN breed_types ON animals.breed_id = breed_types.breed_type_id
                JOIN animal_types ON animals.animal_type_id = animal_types.animal_type_id
                WHERE animals.animal_id LIKE '%6785%'
                """)
    
    # print (type(cur.fetchall()[0]))
    for row in cur.fetchall():
        print (row)