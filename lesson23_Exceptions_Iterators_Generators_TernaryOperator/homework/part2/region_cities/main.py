# У вас есть список городов towns. 
# Нужно написать функция filter_towns, 
# которая будет фильтровать города.
# Необходимо отфильтровать только те города, которые
# находятся в московской области (region == "МО").

# На вход функция принимает список объектов Town, 
# на выходе должна вернуть отфильтрованный список названий городов.

class Town:
    def __init__(self, name, region):
        self.name = name
        self.region = region

    def __repr__(self):
        return f'{self.region} - {self.name}'


towns = [Town('Балашиха', 'МО'), Town('Химки', 'МО'), Town('Тула', 'Тульская область')]

 
def filter_towns(towns):
    # TODO напишите свой код здесь
    pass


if __name__ == "__main__":
    print(filter_towns(towns))
