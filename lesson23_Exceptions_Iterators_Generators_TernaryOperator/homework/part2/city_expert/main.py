# У вас есть список городов towns.
# Нужно написать функцию get_names,
# которая вернет список всех названий городов.
# В качестве аргумента функция принимает список
# городов - список объектов Town и в результате
# должна вывести список названий
# (поле name у объекта Town).


class Town:
    def __init__(self, name, region):
        self.name = name
        self.region = region

    def __repr__(self):
        return f'{self.region} - {self.name}'


towns = [Town('Балашиха', 'МО'), Town('Химки', 'МО'), Town('Тула', 'Тульская область')]


def get_names(towns):
    # TODO опишите логику функции здесь
    pass


if __name__ == "__main__":
    print(get_names(towns))
