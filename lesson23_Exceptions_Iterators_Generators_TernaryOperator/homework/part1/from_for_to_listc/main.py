# Представьте, что у вас есть проект “город”.
# Один из модулей этого проекта умеет находить
# названия городов россии, которые находятся в
# московской области. Этот код приведен ниже.
#
# В какой-то момент руководитель проекта решает,
# что нужно “отрефакторить” код на list comprehensions.
# Поэтому нужно переписать код, приведенный ниже,
# с обычных конструкций (for if yield) на list comprehensions.


class Town:
    def __init__(self, name, region):
        self.name = name
        self.region = region


towns = [Town("балашиха", "мо"), Town("химки", "мо"), Town("тула", "тульская область")]


def find(towns, region):
    for t in towns:
        if t.region == region:
            yield t.name


if __name__ == "__main__":
    print([x for x in find(towns, "мо")])
