from typing import Any, Dict, List


def get_user_list(source: str) -> List[Dict[str, Any]]:
    """Длинный метод (код- smell: Long Method).

    Функция длинная и смешивает парсинг, логику и вывод.
    """

    # --- Этап 1: получение и разбор данных из строки ---
    users_raw = []
    # ожидаем, что каждая запись в source — новая строка 'name,age' или 'name:age'
    # lines = [ln.strip() for ln in source.splitlines() if ln.strip()]
    lines = []

    for ln in source.splitlines():
        if ln.strip():
            lines.append(ln.strip())

    for ln in lines:
        # поддерживаем несколько разделителей и защищаемся от ошибок
        if "," in ln:
            parts = ln.split(",")
        elif ":" in ln:
            parts = ln.split(":")
        else:
            # если формат неизвестен — пропускаем
            continue

        name = parts[0].strip() if parts else ""
        age_raw = parts[1].strip() if len(parts) > 1 else ""
        try:
            age = int(age_raw)
        except Exception:
            # неверный возраст — считаем 0 и продолжаем
            print(
                f"Не удалось распарсить возраст '{age_raw}' для '{name}', устанавливаю 0"
            )
            age = 0

        users_raw.append({"name": name, "age": age})

    # --- Этап 2: сортировка по возрасту ---
    new_data = []
    used_person = set()
    min_age_person = None

    while len(new_data) < len(users_raw):
        for person in users_raw:
            if person["name"] in used_person:
                continue
            elif min_age_person is None:
                min_age_person = person
            elif person["age"] < min_age_person["age"]:
                min_age_person = person
        if min_age_person is not None:
            new_data.append(min_age_person)
            used_person.add(min_age_person["name"])
            min_age_person = None

    # --- Этап 3: фильтрация — только пользователи старше 10 лет ---
    result = []

    for user in new_data:
        if user["age"] > 10:
            result.append(user)

    return result


sample = """Alice,12
Bob,9
Charlie:15
Daisy,6
EmptyLine, 100
Eve,30
"""

result = get_user_list(sample)

for u in result:
    print(f"{u['name']} — {u['age']} лет")

print("____________________________________")


def get_data_from_lines(lines: List[str]) -> List[Dict[str, Any]]:
    data = []
    for ln in lines:
        if "," in ln:
            parts = ln.split(",")
        elif ":" in ln:
            parts = ln.split(":")
        else:
            continue

        name = parts[0].strip() if parts else ""
        age_raw = parts[1].strip() if len(parts) > 1 else ""
        try:
            age = int(age_raw)
        except Exception:
            print(
                f"Не удалось распарсить возраст '{age_raw}' для '{name}', устанавливаю 0"
            )
            age = 0

        data.append({"name": name, "age": age})

    return data


def get_user_list_refactored(source: str) -> List[Dict[str, Any]]:
    lines = [ln.strip() for ln in source.splitlines() if ln.strip()]
    data = get_data_from_lines(lines)
    data.sort(key=lambda x: x["age"])
    result = [u for u in data if u["age"] > 10]
    return result


res = get_user_list_refactored(sample)

for u in res:
    print(f"{u['name']} — {u['age']} лет")
