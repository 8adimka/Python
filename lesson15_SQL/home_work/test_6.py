import sqlite3
from flask import Flask, render_template

db_path = r"/home/v/Python/lesson15_SQL/home_work/animal.db"
app = Flask (__name__)

@app.route ('/<int:item_id>')
def db_search_page (item_id):
    with sqlite3.connect(db_path) as con:
        cur = con.cursor()
        cur.execute(f"""
                SELECT animals.name, animal_types.animal_type, breed_types.breed_type, outcome_information.outcome_month
                FROM outcome_information
                JOIN animals ON animals.animal_id = outcome_information.animal_id
                JOIN breed_types ON animals.breed_id = breed_types.breed_type_id
                JOIN animal_types ON animals.animal_type_id = animal_types.animal_type_id
                WHERE outcome_information.outcome_id = {item_id}
                    """)
        result = cur.fetchall()
        return (str(result[0]))
            

if __name__ == '__main__':
    app.run()