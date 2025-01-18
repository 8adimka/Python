import math

"""Разберёмся что такое геттеры - достователи"""

# class TodoList:
#     def __init__(self):
#         self.active = []
#         self.closed = []
      
#     def add_task(self, task):
#         self.active.append(task)

#     def remove_task(self, task):
#         if task not in self.active:
#             return 
#         self.active.remove(task)
#         self.closed.append(task)
    
#     def count_active(self):
#         return len(self.active)
    
#     def count_closed(self):
#         return len(self.closed)
    
#     count_done = count_closed  # Псевдоним

#     def check_status(self, task):
#         if task in self.active:
#             return f"Задача '{task}' - Активная"
#         elif task in self.closed:
#             return f"Задача '{task}' - Закрытая"
#         return "Такой задачи нет"
    
#     def get_active (self):
#         return ', '.join(f"{i}. {task}" for i, task in enumerate(self.active, 1))
    
#     def get_closed (self):
#         return ', '.join([f"{i}. {task}" for i, task in enumerate(self.closed, 1)])

# # Проверка
# todo_list = TodoList()

# todo_list.add_task("Выключить свет")
# todo_list.add_task("Поменять лампочку")
# todo_list.add_task("Включить свет")
# todo_list.add_task("Купить хлеб")

# todo_list.remove_task("Поменять лампочку")

# print(" ".join(todo_list.active))  # Вывод: "Выключить свет Включить свет"
# print(" ".join(todo_list.closed))  # Вывод: "Поменять лампочку"
# print("Количество активных задач -", todo_list.count_active())   # Вывод: 2
# print("Количество выполненных и закрытых задач -", todo_list.count_closed())  # Вывод: 1
# print("и оно же равно -", todo_list.count_done())    # Вывод: 1
# print(todo_list.get_active())  # Вывод: "Выключить свет, Включить свет"
# print(todo_list.get_closed())  # Вывод: "Поменять лампочку"
# print(todo_list.check_status("Выключить свет"))  # Вывод: "Активная"


print ("______________________________________________________________________________\n\n____________________________________________________________")

"""
Сперва перепишем класс и сделаем поля класса __приватными

Напишем метод `restore(task)` , переводит задачу из `__closed` в `__active`

Напишием метод `is_empty()` который проверит все ли задачи выполнены (True если список closed пустой)
Изменения:
Поля __active и __closed стали приватными.
Метод restore() добавляет задачу обратно в активные.
Метод is_empty() проверяет, пуст ли список активных задач.

+Добавим новую property `count` для экземпляра класса.
Значение равно **сумме** активных и выполненных

Добавим новую property `latest` для  экземпляра класса.
Значение равно **последнему** добавленному элементу из `__active` или `None`

Добавим новую property `completion_rate` для экземпляра класса.
Значение равно **количеству** **выполненных** деленному на **количество** **всех** элементов, например `0.3`"""

class TodoList:
    def __init__(self):
        self.__active = []
        self.__closed = []
      
    def add_task(self, task):
        self.__active.append(task)

    def remove_task(self, task):
        if task not in self.__active:
            return 
        self.__active.remove(task)
        self.__closed.append(task)
    
    def count_active(self):
        return len(self.__active)
    
    def count_closed(self):
        return len(self.__closed)
    
    count_done = count_closed  # Псевдоним

    def check_status(self, task):
        if task in self.__active:
            return f"Задача '{task}' - Активная"
        elif task in self.__closed:
            return f"Задача '{task}' - Закрытая"
        return "Такой задачи нет"
    
    def get_active(self):
        return ', '.join(f"{i}. {task}" for i, task in enumerate(self.__active, 1))
    
    def get_closed(self):
        return ', '.join(f"{i}. {task}" for i, task in enumerate(self.__closed, 1))
    
    def restore(self, task):
        """Переводит задачу из закрытых в активные."""
        if task in self.__closed:
            self.__closed.remove(task)
            self.__active.append(task)
        else:
            print(f"Задача '{task}' отсутствует в закрытых.")
    
    def is_empty(self):
        """Проверяет, выполнены ли все задачи (True, если __active пустой)."""
        return len(self.__active) == 0

    @property
    def count(self):
        """Возвращает сумму активных и выполненных задач."""
        return len(self.__active) + len(self.__closed)

    @property
    def latest(self):
        """Возвращает последний добавленный активный элемент или None."""
        return self.__active[-1] if self.__active else None

    @property
    def completion_rate(self):
        """Возвращает долю выполненных задач относительно всех задач."""
        total = len(self.__active) + len(self.__closed)
        return f'{(len(self.__closed) / total)*100}%' if total > 0 else '0%'

# # Проверка
todo_list = TodoList()

todo_list.add_task("Выключить свет")
todo_list.add_task("Поменять лампочку")
# todo_list.add_task("Включить свет")
# todo_list.add_task("Купить хлеб")

# todo_list.remove_task("Поменять лампочку")
# print("Суммарное количество задач:", todo_list.count)  # Вывод: 4

print("Количество активных задач -", todo_list.count_active())   # Вывод: 3
# print("Количество выполненных и закрытых задач -", todo_list.count_closed())  # Вывод: 1
# print("и оно же равно -", todo_list.count_done())    # Вывод: 1
# print(todo_list.get_active())  # Вывод: "1. Выключить свет, 2. Включить свет, 3. Купить хлеб"
# print(todo_list.get_closed())  # Вывод: "1. Поменять лампочку"
# print(todo_list.check_status("Выключить свет"))  # Вывод: "Задача 'Выключить свет' - Активная"

# # Восстановление задачи
# todo_list.restore("Поменять лампочку")
# print(todo_list.get_active())  # Вывод: "1. Выключить свет, 2. Включить свет, 3. Купить хлеб, 4. Поменять лампочку"
# print(todo_list.get_closed())  # Вывод: ""

# # Проверка, все ли задачи выполнены
# print("Все задачи выполнены?", todo_list.is_empty())  # Вывод: False

# # Убираем все активные задачи
# todo_list.remove_task("Выключить свет")
# todo_list.remove_task("Включить свет")
# todo_list.remove_task("Купить хлеб")
# todo_list.remove_task("Поменять лампочку")
# print("А теперь?", todo_list.is_empty())  # Вывод: True

# todo_list.add_task("Выключить свет")
# todo_list.add_task("Поменять лампочку")
# todo_list.add_task("Включить свет")
# print("Суммарное количество задач:", todo_list.count)  # Вывод: 7

# print("Последняя активная задача:", todo_list.latest)  # Вывод: "Включить свет"

# todo_list.add_task("Купить хлеб")

# print("Процент выполнения:", todo_list.completion_rate)  # Вывод: 0.0

# todo_list.remove_task("Поменять лампочку")

# print("Суммарное количество задач:", todo_list.count)  # Вывод: 8
# print("Последняя активная задача:", todo_list.latest)  # Вывод: "Купить хлеб"
# print("Процент выполнения:", todo_list.completion_rate)  # Вывод: 0.333...

# todo_list.remove_task("Выключить свет")
# todo_list.remove_task("Включить свет")
# todo_list.remove_task("Купить хлеб")

# print("Суммарное количество задач:", todo_list.count)  # Вывод: 3
# print("Последняя активная задача:", todo_list.latest)  # Вывод: None
# print("Процент выполнения:", todo_list.completion_rate)  # Вывод: 1.0

print ("______________________________________________________________________________\n\n____________________________________________________________")


class Product:
    def __init__(self,name="", price=0):
        self.name = name
        self.price = price

    def __repr__ (self):
        return f"Product('{self.name}', {self.price})"

class Cart:
    def __init__(self):
        self.items = []

    def add (self, product):
        self.items.append(product)

    def create_and_add (self, name, price):
        product = Product(name, price)
        self.add(product)

    @property
    def count_items (self):
        return len (self.items)

    @property
    def count_summ(self):
        # Генерируем список цен из объектов items
        prices = [item.price for item in self.items]

        # Определяем рекурсивную лямбда-функцию для суммирования
        lambda_sum = lambda *args: 0 if not args else args[0] + lambda_sum(*args[1:])

        # Вызываем функцию с распакованными аргументами
        return lambda_sum(*prices)

        #Или можно так, но не так интересно
        return sum ([item.price for item in self.items])

    @property
    def as_list(self):
        return [item.name for item in self.items]

    @property
    def as_dict(self):
        item_dict = {item.name : item.price for item in self.items}
        return item_dict

    @property
    def max_price(self):
        return max ([item.price for item in self.items])

    @property
    def last_item (self):
        return self.items[-1]


p_1 = Product("cheese", 200)
p_2 = Product("milk", 150)

cart = Cart()

cart.add(p_1)
cart.add(p_2)


cart.create_and_add("waffles", 310)
for item in cart.items:
    print(item.name, item.price)

print (cart.count_items)
print (cart.count_summ)

print (cart.as_list)
print (type(cart.as_dict))

print (cart.last_item.name, cart.last_item.price)
print (cart.max_price)



#Сложное решение простой задачи ->
items_list = [(1, 2, 3), (4, 5), (6, 7, 8, 9)]

# Определяем лямбда-функцию, аналогичную sum
lambda_sum = lambda *args: 0 if not args else args[0] + lambda_sum(*args[1:])

# Применяем лямбда-функцию, распаковывая элементы кортежей
counter = map(lambda x: lambda_sum(*x), items_list)

# Результат
print(list(counter))  # Вывод: [6, 9, 30]



class Point:
    def __init__ (self, x=0, y=0):
        self.x = x
        self.y = y


point_a = Point(x=2,y=3)
point_b = Point(x=5,y=7)


class Line:
    def __init__(self, point_1, point_2):
        self.point_1 = point_1
        self.point_2 = point_2

    @property
    def get_length(self):
        lenght = math.sqrt((self.point_1.x-self.point_1.x)**2 + (self.point_1.y-self.point_2.y)**2)
        return round(lenght,1)

line_1 = Line (point_a, point_b)

print (line_1.get_length)

