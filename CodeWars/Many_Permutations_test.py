from Many_Permutations import unique_permutations

def test_1 ():
    value = unique_permutations('aabb')
    for i in value:
        if i in ['aabb', 'abab', 'abba', 'baab', 'baba', 'bbaa']:
            b = True
        else:
            b = False
    assert b == True, f'test_1 -> "aabb" should return "[aabb, abab, abba, baab, baba, bbaa]", but return {value}'

def test_2 ():
    value = unique_permutations('ab')
    for i in value:
        if i in ['ab', 'ba']:
            b = True
        else:
            b = False
    assert b == True, f'test_2 -> "ab" should return "[ab, ba]", but return {value}'
