# Представьте, что у вас есть проект “город”.
# Один из модулей этого проекта умеет составлять
# словарь, где ключ - город, а значение - область.
# Например: {'балашиха': 'мо', 'химки': 'мо', 'тула': 'тульская область'}.
# Этот код приведен ниже.

# В какой-то момент руководитель проекта решает,
# что нужно “отрефакторить” код с list comprehensions
# на обычный код (for, if). Поэтому нужно переписать
# код с list comprehensions на обычный код (for, if).


class Town:
    def __init__(self, name, region):
        self.name = name
        self.region = region


towns = [Town("балашиха", "мо"), Town("химки", "мо"), Town("тула", "тульская область")]


def build_dict(towns):
    return {t.name: t.region for t in towns}


if __name__ == "__main__":
    print(build_dict(towns))
