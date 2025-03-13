class Town:
    def __init__(self, name, region):
        self.name = name
        self.region = region


towns = [Town("балашиха", "мо"), Town("химки", "мо"), Town("тула", "тульская область")]


def find(towns, region):
    return (t.name for t in towns if t.region == region)


if __name__ == "__main__":
    print([x for x in find(towns, "мо")])
