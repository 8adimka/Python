input_str = "hello my friend"


def convert(input_str):
    return (ord(item) for item in input_str)


if __name__ == "__main__":
    for letter in convert(input_str):
        print(letter)
