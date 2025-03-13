streets = ['ленина', 'советская', 'краснооктябрьская', 'первомайская']


def get_tuples(input_arr):
    return list(zip(input_arr, range(1, len(input_arr) + 1)))


if __name__ == "__main__":
    print(get_tuples(streets))
