# Вы решили посчитать средний возраст
# своих друзей в ВК по городам. Для этого вы обратились
# в VK API и получили ответ vk_resp. Но у некоторых
# пользователей не указана дата рождения и город.
# Нужно учесть особенности API и доработать функцию
# calc_average_age, чтобы она обрабатывала исключения,
# то есть сделать так, чтобы код работал и не падал.
#
# Подробно изучите сообщения об ошибках и оберните те строки кода
# которые их вызывают в конструкцию try-except и продолжите выполнение кода с
# новым элементом списка если было вызвано исключение (использовав continue)
#
import datetime
import json
import os
from pathlib import Path

path = Path(__file__)



# Загружаем ответ из VK, он у нас хранится в json-формате
with open(path.parent.joinpath("vk.json"), "r") as f:
    response_data = json.load(f)


def calc_average_age(response_data):
    items = response_data["response"]["items"]
    cities = {}
    for item in items:
        try:
            city_id = item["city"]["id"]
        
            if city_id not in cities:
                cities[city_id] = {"title": item["city"]["title"], "count": 0, "age": 0}
            city_info = cities[city_id]

            d, m, y = item["bdate"].split(".")
            d, m, y = int(d), int(m), int(y)
            td = datetime.date.today() - datetime.date(y, m, d)
            city_info["count"] += 1
            city_info["age"] += td.days // 365
        except:
            continue
    result = []
    for v in cities.values():
        average = v["age"] / v["count"]
        city = v["title"]
        result.append(f"{city} {average}")
    return "\n".join(result)


if __name__ == "__main__":
    print(calc_average_age(response_data))
