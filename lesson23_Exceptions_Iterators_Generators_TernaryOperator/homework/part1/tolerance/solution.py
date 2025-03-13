input_str = "привет чао мой друг брат товарищ знакомый"


def filter_rrr(input_str):
    res = (item for item in input_str.split(" ") if "р" not in item.lower())
    return " ".join(res)


if __name__ == "__main__":
    print(filter_rrr(input_str))
