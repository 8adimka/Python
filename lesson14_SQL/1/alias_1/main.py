# Свежая подборка
# Попрактикуйтесь с использованием alias в названиях колонок таблицы
# Выведите ТОП 10 фильмов и сериалов которые были добавлены в базу данных самые последние (date_added)
# Название столбцов таблицы должны совпадать с образцом ниже.
#
# Пример результата:
# +---------------------+--------------------------------+---------------------+--------------------+
# |       Название      |            Режиссер            |   Время добавления  | Возрастной рейтинг |
# +---------------------+--------------------------------+---------------------+--------------------+
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
sqlite_query = ("""
SELECT title as 'Название', director as 'Режиссер', date_added as 'Время добавления', rating as 'Возрастной рейтинг'
FROM netflix 
WHERE date_added IS NOT NULL
ORDER BY date_added DESC
LIMIT 10
""")  # TODO измените код запроса
result = cur.execute(sqlite_query)

# не удаляйте код дальше, он нужен для вывода результата
# запроса в красивом формате

mytable = prettytable.from_db_cursor(result)
mytable.max_width = 30


if __name__ == '__main__':
    print(mytable)
