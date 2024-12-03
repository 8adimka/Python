# Болливуд
#
# Индийские фильмы одно время были очень популярны.
# Давайте проверим, как это отразилось на Нетфликсе!
# Нам нужно посчитать, сколько индийских фильмов и сериалов есть на платформе.
# Также считаются фильмы и сериалы которые были сняты совместно с Индией
#
# Пример результата:
#
# фильмы: 50 шт
# сериалы: 10 шт
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

with sqlite3.connect("/home/v/Python/lesson14_SQL/part1/netflix.db") as con:
    cur = con.cursor()
    sqlite_query = ("""
                    SELECT release_year, type, COUNT (show_id)
                    FROM netflix
                    WHERE country LIKE '%India%'
                    GROUP BY release_year, type
                    """)  # TODO измените код
    cur.execute(sqlite_query)
    executed_query = cur.fetchall()

    # TODO Результат запроса сохраните в переменной result
    # для последующей выдачи в требуемом формате

result = executed_query


if __name__ == '__main__':
    for row in result:
        print(row)
