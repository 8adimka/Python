from itertools import permutations

def unique_permutations(s):
    # Генерируем все уникальные перестановки
    return list (set(''.join(p) for p in permutations(s)))
