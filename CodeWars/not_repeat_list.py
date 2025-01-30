unique_in_order = lambda l: [z for i, z in enumerate(l) if i == 0 or l[i - 1] != z]

def unique_in_order (iterable):
    return [val for i, val in enumerate(iterable) if i == 0 or iterable[i-1] != val]
