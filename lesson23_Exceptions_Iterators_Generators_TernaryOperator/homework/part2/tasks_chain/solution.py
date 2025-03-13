class Town:
    def __init__(self, id, name, region):
        self.id = id
        self.name = name
        self.region = region

    def __repr__(self):
        return f'{self.region} - {self.name}'


towns = [Town(1, 'Балашиха', 'МО'), Town(2, 'Химки', 'МО'), Town(3, 'Тула', 'Тульская область')]

 
def get_ids(towns):
    res = filter(lambda t: t.region == 'МО', towns)
    res = sorted(res, key=lambda v: v.name)
    return list(map(lambda t: t.id, res))


if __name__ == "__main__":
    print(get_ids(towns))
