# 1. Есть json-структура, типа
# data = """{
# "name": "Alex",
# "age": 25,
# "address": "",
# "phone_number": null
# }"""
# Написать функцию, которая вернет строку, где поля не содержат пустых и null значений
# 2. Написать функцию, которая принимает строку с текстом и возвращает самое часто встречающееся слово (игнорируя регистр и пунктуацию)

import json

data = """{
"name": "Alex",
"age": 25,
"address": "",
"phone_number": null
}"""


def clearer(data: str) -> str:
    obj = json.loads(data)
    result = {k: v for k, v in obj.items() if v not in ("", None)}
    return json.dumps(result)


print(clearer(data))

import re
from collections import Counter


def common_word(s: str) -> str:
    words = re.findall(r"\b\w+\b", s.lower())
    print(words)
    counter = Counter(words)
    print(counter)
    if counter:
        return counter.most_common(1)[0][0]
    return ""


text = "Написать функцию,которая принимает строку с текстом.и. возвращает самое часто встречающееся слово (игнорируя регистр.и.пунктуацию"

print(common_word(text))
