class Town:
    def __init__(self, name, region):
        self.name = name
        self.region = region

    def __repr__(self):
        return f'{self.region} - {self.name}'


towns = [Town('Балашиха', 'МО'), Town('Химки', 'МО'), Town('Тула', 'Тульская область')]


def filter_towns(towns):
    return [x.name for x in filter(lambda v: v.region == 'МО', towns)]


if __name__ == "__main__":
    print(filter_towns(towns))
