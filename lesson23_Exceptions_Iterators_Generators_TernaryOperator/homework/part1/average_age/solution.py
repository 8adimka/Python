import datetime
import json
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
        except (KeyError, TypeError):
            continue
        if city_id not in cities:
            cities[city_id] = {"title": item["city"]["title"], "count": 0, "age": 0}
        city_info = cities[city_id]
        try:
            d, m, y = item["bdate"].split(".")
        except (ValueError, AttributeError):
            continue
        d, m, y = int(d), int(m), int(y)
        td = datetime.date.today() - datetime.date(y, m, d)
        city_info["count"] += 1
        city_info["age"] += td.days // 365
    result = []
    for v in cities.values():
        average = v["age"] / v["count"]
        city = v["title"]
        result.append(f"{city} {average}")
    return "\n".join(result)


if __name__ == "__main__":
    print(calc_average_age(response_data))
