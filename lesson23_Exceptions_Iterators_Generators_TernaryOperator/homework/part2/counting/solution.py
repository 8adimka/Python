from collections import namedtuple, defaultdict

Town = namedtuple('Town', ['name', 'region'])
 
towns = [Town('балашиха', 'мо'), Town('химки', 'мо'), Town('тула', 'тульская область')]


def counter(towns):
    d = defaultdict(lambda: 0)
    for t in towns:
        d[t.region] += 1
    return dict(d)


if __name__ == "__main__":
    print(counter(towns))