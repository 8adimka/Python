# У вас есть список городов towns. 
# Нужно написать функцию sort_towns, 
# которая должна отсортировать города (в алфавитном порядке) 
# по названию.
# На вход функция принимает список объектов Town, 
# на выходе функция возвращает отсортированный список названий городов.

class Town:
    def __init__(self, name, region):
        self.name = name
        self.region = region

    def __repr__(self):
        return f'{self.region} - {self.name}'


towns = [Town('Балашиха', 'МО'), Town('Химки', 'МО'), Town('Тула', 'Тульская область')]

 
def sort_towns(towns):
    # TODO напишите функцию здесь
    pass


if __name__ == "__main__":
    print(sort_towns(towns))
