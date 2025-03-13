input_str = "hello my friend"


def convert(input_str):
    return {item: ord(item) for item in input_str}


if __name__ == "__main__":
    print(convert(input_str))
