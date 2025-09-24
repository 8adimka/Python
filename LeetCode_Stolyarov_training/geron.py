# from math import sqrt


# def geron(a: int, b: int, c: int) -> float:
#     p = (a + b + c) / 2
#     return sqrt(p * (p - a) * (p - b) * (p - c))


# print(geron(3, 4, 5))


# def remove_symbols(string, *symbols):
#     for sym in symbols:
#         string = string.replace(sym, "")
#     return string


# print(remove_symbols("Hello, World!", ",", "!"))  # Hello World

# print(remove_symbols("Hello, World!", *",! WHl"))  # Hello World


expenses = {"еда": 500, "транспорт": 200, "развлечения": 300}
user_str = input("Введите категорию и сумму в формате 'категория:сумма_покупки'\n->")
if ":" in user_str:
    user_lst = user_str.split(":")
    if user_lst[0].lower() in expenses:
        expenses[user_lst[0].lower()] += int(user_lst[1])
    else:
        expenses[user_lst[0].lower()] = int(user_lst[1])
else:
    print("Неверный формат ввода")

total = sum(expenses.values())
print(f"Итоговая сумма: {total}")
print(expenses)
