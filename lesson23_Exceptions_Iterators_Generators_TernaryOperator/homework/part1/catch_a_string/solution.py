a = [1, 2, 3]


def cant_work():
    try:
        value = a[4]
    except:
        value = "Исключение поймано"
    return value
