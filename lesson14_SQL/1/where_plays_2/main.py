# Где играет - 2
# Выведите название и возрастной рейтинг всех фильмов,
# в которых играет Хоакин Феникс (Joaquin Phoenix) – победитель
# номинации за лучшую мужскую роль.
#
# Пример результата:
# +------------+--------+
# |   title    | rating |
# +------------+--------+
# |   Movie    |   R    |
# |   Movie    |   R    |
# +------------+--------+
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
sqlite_query = ("SELECT title, rating FROM netflix WHERE `cast` LIKE '%Joaquin Phoenix%' AND type='Movie'")  # TODO измените код запроса
result = cur.execute(sqlite_query)

# не удаляйте код дальше, он нужен для вывода результата
# запроса в красивом формате

mytable = prettytable.from_db_cursor(result)
mytable.max_width = 30


if __name__ == '__main__':
    print(mytable)
