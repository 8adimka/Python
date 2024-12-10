# JOIN из трех таблиц
#
#  JOIN также возможно использовать для трех и более таблиц.
#  Давайте посмотрим в каких жанрах работают артисты.
#  Выведите две колонки в одной из которых будет содержаться имя артиста(name), а в другой жанр(genre).
#  Ознакомится со схемой базы данных можно в файле db_schema.png
#  Подсказка: После первого JOIN аналогичным образом можно
#  использовать такую конструкцию и для других таблиц
#
#
#
import sqlite3
import prettytable

con = sqlite3.connect(r"/home/v/Python/lesson15_SQL/part2/music.db")
cur = con.cursor()
sqlite_query = ("""SELECT DISTINCT artists.name, genres.name
                FROM tracks
                INNER JOIN genres ON tracks.genre_id = genres.ID
                INNER JOIN albums ON tracks.album_id = albums.ID
                LEFT JOIN artists ON albums.artist_id = artists.ID""")  # TODO составьте JOIN запрос здесь


# table = cur.execute(sqlite_query)
# mytable = prettytable.from_db_cursor(table)
# mytable.max_width = 30

# if __name__ == "__main__":
#     print(mytable)

result = cur.execute(sqlite_query)
for row in result:
    if __name__ == "__main__":
        print(row)
