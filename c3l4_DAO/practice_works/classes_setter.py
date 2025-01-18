
class Product:
    # Общий счётчик для всех объектов класса
    _id_counter = 1

    # Допустимые категории
    categories = ["fruits", "veggies", "sweets", "stuff"]

    def __init__(self, name="", price=0, category="stuff"):
        self.__name = name
        self.__price = price

        # Проверка категории
        if category not in Product.categories:
            print(f"Категория '{category}' отсутствует в списке.")
            self.add_category(category)

        self.__category = category

        # Присваиваем уникальный pk и увеличиваем счётчик
        self.pk = Product._id_counter
        Product._id_counter += 1

    @classmethod # @classmethod - используется для создания методов класса, которые привязаны к самому классу, а не к конкретному экземпляру
    def add_category(cls, category):
        """Добавляет новую категорию после подтверждения пользователя."""
        answer = input(f"Хотите добавить новую категорию '{category}'?\n(y/n) -> ")
        if answer.lower() == 'y':
            cls.categories.append(category)
            print(f"Категория '{category}' добавлена.")
        else:
            raise ValueError(f"Категория '{category}' недопустима. Выберите из {cls.categories}.")

    # Setters (сеттеры)    
    def set_category (self, category):
        if category not in Product.categories:
            print(f"Категория '{category}' отсутствует в списке.")
            self.add_category(category)

        self.__category = category

    # Getters (геттеры) - позволяют получать __приватные параметры и значения
    @property
    def name(self):
        return self.__name

    @property
    def price(self):
        return self.__price
    
    @property
    def category(self):
        return self.__category


# Примеры
p_1 = Product("cheesecake", 200, "stuff")  # Категория существует
p_2 = Product("milk", 150)                  # Используется категория по умолчанию
p_3 = Product("apple", 50, "fruits")        # Категория существует

p_1.set_category ("sweets")
p_1.__category = "somestuff" # Приватный - установится только через сеттер set_category
print(p_1.name, p_1.category)  # Вывод: 1

p_2.set_category ("milk")
print(p_2.name, p_2.category)
print(p_3.name, p_3.pk)  # Вывод: 3


try:
    p_4 = Product("choriso", 200, "carne")  # Запрос на добавление категории
except ValueError as e:
    print(e)
print(p_4.name, p_4.category)



