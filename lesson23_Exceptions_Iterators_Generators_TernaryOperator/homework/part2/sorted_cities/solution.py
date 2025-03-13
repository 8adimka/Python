class Town:
    def __init__(self, name, region):
        self.name = name
        self.region = region

    def __repr__(self):
        return f'{self.region} - {self.name}'


towns = [Town('Балашиха', 'МО'), Town('Химки', 'МО'), Town('Тула', 'Тульская область')]


def sort_towns(towns):
    towns = sorted(towns, key=lambda v: v.name)
    return [town.name for town in towns]


if __name__ == "__main__":
    print(sort_towns(towns))
