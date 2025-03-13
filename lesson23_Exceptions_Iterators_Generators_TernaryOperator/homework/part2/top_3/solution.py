from collections import Counter


def top3(input_str):
    c = Counter(input_str)
    return [item[0] for item in c.most_common(3)]
