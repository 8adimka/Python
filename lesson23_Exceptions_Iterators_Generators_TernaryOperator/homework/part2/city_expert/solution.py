class Town:
    def __init__(self, name, region):
        self.name = name
        self.region = region

    def __repr__(self):
        return f'{self.region} - {self.name}'


towns = [Town('Балашиха', 'МО'), Town('Химки', 'МО'), Town('Тула', 'Тульская область')]


def get_names(towns):
    return list(map(lambda v: v.name, towns))


if __name__ == "__main__":
    print(get_names(towns))
