#  В этом задании давайте выведем всех артистов (name)
#  и названия их альбомов (album_title), которые содержатся в базе
#  (Вам потребуются таблицы Artists и Albums) а также конструкция с JOIN.
#  Ознакомится со схемой базы данных можно в файле db_schema.png
import sqlite3
import prettytable

con = sqlite3.connect(r"/home/v/Python/lesson15_SQL/part2/music.db")
cur = con.cursor()
sqlite_query = ("""
                SELECT albums.album_title, artists.name
                FROM albums
                INNER JOIN artists ON albums.artist_id = artists.ID
                WHERE artists.name NOT NULL
                """)  # TODO составьте запрос на создание таблицы


# Не удаляйте код ниже, он используется
# для вывода заголовков созданной таблицы
table = cur.execute(sqlite_query)
mytable = prettytable.from_db_cursor(table)
mytable.max_width = 30

if __name__ == "__main__":
    print(mytable)
