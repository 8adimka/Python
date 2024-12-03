import sqlite3, json
from flask import Flask, render_template, jsonify

# app = Flask (__name__)

# @app.route('/<title>/')
# def movie_page (title):
#     with sqlite3.connect ("/home/v/Python/lesson14_SQL/project/netflix.db") as con:
#         curs = con.cursor()    
#         query = (f"""
#                     SELECT title, director, country, release_year
#                     FROM netflix
#                     WHERE title LIKE '%{title}%'
#                     ORDER BY release_year DESC
#                     LIMIT 1
#                     """)
#         curs.execute(query)
#         result = curs.fetchall()
    
#     if result:
#         for_page = f'"title": {result[0][0]}\n"country": {result[0][2]}\n"release_year":{result[0][3]}'
#     else:
#         for_page = "No results found"
    
#     # print (f'"title": {result[0][0]}\n"country": {result[0][2]}\n"release_year":{result[0][3]}')
#     return for_page


# def between_years (year_start, year_end):
#     with sqlite3.connect ("/home/v/Python/lesson14_SQL/project/netflix.db") as connection:
#         cursor = connection.cursor()
#         query = f"""
#         SELECT title, release_year
#         FROM netflix
#         WHERE release_year BETWEEN {year_start} AND {year_end}
#         ORDER BY release_year DESC
#         LIMIT 100
#         """
#         cursor.execute(query)
#         result = cursor.fetchall()
#         data = []
#         for i in range (0, len (result)):
#             data.append ({"title":result[i][0],"release_year": result[i][1]})
#     return data

# @app.route('/movie/<year1>/<year2>')
# def serch_years (year1, year2):
#     data = between_years(year1, year2)
#     return jsonify(data)

# @app.route('/favicon.ico')
# def favicon():
#     return '', 204  # Отвечаем пустым содержимым без ошибок

# def family_choice (age):
#     with sqlite3.connect ("/home/v/Python/lesson14_SQL/project/netflix.db") as con:
#         cursor = con.cursor()

#         if age == 'children':
#             query = f"""SELECT title, rating, description
#             FROM netflix
#             WHERE rating='G'
#             ORDER BY release_year DESC
#             LIMIT 10
#             """
#             cursor.execute(query)
#             result = cursor.fetchall()
#             data = []
#             for i in range (0, len (result)):
#                 data.append ({"title":result[i][0],"rating": result[i][1],"description": result[i][2]})

#         elif age == 'family':
#             query = f"""SELECT title, rating, description
#             FROM netflix
#             WHERE rating='G' OR rating='PG' OR rating='PG-13'
#             ORDER BY release_year DESC
#             LIMIT 10
#             """
#             cursor.execute(query)
#             result = cursor.fetchall()
#             data = []
#             for i in range (0, len (result)):
#                 data.append ({"title":result[i][0],"rating": result[i][1],"description": result[i][2]})

#         elif age == 'adult':
#             query = f"""SELECT title, rating, description
#             FROM netflix
#             WHERE rating='R' OR rating='NC-17'
#             ORDER BY release_year DESC
#             LIMIT 10
#             """
#             cursor.execute(query)
#             result = cursor.fetchall()
#             data = []
#             for i in range (0, len (result)):
#                 data.append ({"title":result[i][0],"rating": result[i][1],"description": result[i][2]})
#     return data

# @app.route('/rating/<age_choice>')
# def age_choice_page (age_choice):
#     return family_choice (age_choice)


# def top_new (listed_in):
#     with sqlite3.connect ("/home/v/Python/lesson14_SQL/project/netflix.db") as connection:
#         cursor = connection.cursor()
#         query = f"""
#         SELECT title, description
#         FROM netflix
#         WHERE listed_in LIKE '%{listed_in}%'
#         ORDER BY release_year DESC
#         LIMIT 10
#         """
#         cursor.execute(query)
#         result = cursor.fetchall()
#         with open ('/home/v/Python/lesson14_SQL/project/result.json', 'w', encoding='utf-8') as file:
#                 json.dump (result, file)


# @app.route('/genre/<genre>')
# def top_new_page (genre):
#     top_new (genre)
#     result_string = ''
#     with open ('/home/v/Python/lesson14_SQL/project/result.json', 'r', encoding='utf-8') as file:
#         result = json.load (file)
#     for i in range (0, len (result)):
#         result_string += "title: " + str(result[i][0]) + ", description: " + str(result[i][1]).replace('\n', '') + '<br>'
#     return str(result_string)

# if __name__ == '__main__':
#     app.run()

def actors_friends (actor_1, actor_2):
     with sqlite3.connect ("/home/v/Python/lesson14_SQL/project/netflix.db") as con:
        curs = con.cursor()
        query = f"""
        SELECT `cast`
        FROM netflix
        WHERE `cast` LIKE '%{actor_1}%' AND `cast` LIKE '%{actor_2}%'
        """
        curs.execute (query)
        result = curs.fetchall()
        friends_set = set()
        friends_list = []
        for i in result:
            friends_list += i[0].split(', ')

        for friend in friends_list:
            if friends_list.count(friend) > 2:
                friends_set.add(friend)

        friends_set.discard(actor_1)
        friends_set.discard(actor_2)
        for friend in friends_set:
            print (friend)

# actors_friends ('Jack Black', 'Dustin Hoffman')
# print ('')
# actors_friends ('Rose McIver', 'Ben Lamb')

def serch_film (type, release_year, listed_in):
    with sqlite3.connect ("/home/v/Python/lesson14_SQL/project/netflix.db") as con:
        curs = con.cursor()
        query = f"""
        SELECT title, description
        FROM netflix
        WHERE `listed_in` LIKE '%{listed_in}%' AND `type` LIKE '%{type}%' AND `release_year` = {release_year}
        """
        curs.execute (query)
        result = curs.fetchall()
        with open ('/home/v/Python/lesson14_SQL/project/result.json', 'w') as file:
            json.dump (result, file)


serch_film ('Movie', 2006, 'horror')

with open ('/home/v/Python/lesson14_SQL/project/result.json', 'r') as file:
    res = json.load (file)
    for i in res:
        print (i)

