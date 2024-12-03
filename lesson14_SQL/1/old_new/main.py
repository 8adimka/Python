# Старый и новый
# Найдите фильмы, снятые режиссером Guy Ritchie до 2010 года включительно.
# Выведите название и список актеров в каждом фильме.
#
# Пример результата:
# +--------------------------------+--------------------------------+
# |             title              |              cast              |
# +--------------------------------+--------------------------------+
# |  Lock, Stock and Two Smoking   |     Jason Flemyng, Dexter      |
# |            Barrels"            |  Fletcher, Nick Moran, Jason   |
# |                                |  Statham, Steven Mackintosh,   |
# |                                |   Nicholas Rowe, Nick Marcq,   |
# |                                | Charles Forbes, Vinnie Jones,  |
# |                                |          Lenny McLean          |
# +--------------------------------+--------------------------------+
#
# Структура таблицы
# -----------------------
# show_id — id тайтла
# type — фильм или сериал
# title — название
# director — режиссер
# cast — основные актеры
# country — страна производства
# date_added — когда добавлен на Нетфликс
# release_year — когда выпущен в прокат
# rating — возрастной рейтинг
# duration — длительность
# duration_type — минуты или сезоны
# listed_in — список жанров и подборок
# description — краткое описание
# -----------------------
import sqlite3
import prettytable

con = sqlite3.connect("/home/v/Python/lesson14-and-tests/part1/netflix.db")
cur = con.cursor()
sqlite_query = ("SELECT title, director, release_year FROM netflix WHERE director = 'Guy Ritchie' AND release_year <= 2009")  # TODO измените код запроса
result = cur.execute(sqlite_query)

# не удаляйте код дальше, он нужен для вывода результата
# запроса в красивом формате

for row in result.fetchall ():
    print (row)


# if __name__ == '__main__':
#     print(mytable)
