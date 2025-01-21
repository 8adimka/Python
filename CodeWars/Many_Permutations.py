from itertools import permutations

def unique_permutations(s):
    # Генерируем все уникальные перестановки
    return list (set(''.join(p) for p in permutations(s)))

print (unique_permutations('abbcdd'))
print (len(unique_permutations('abbcdd')))

print (unique_permutations('abcd'))
print (len(unique_permutations('abcd')))
