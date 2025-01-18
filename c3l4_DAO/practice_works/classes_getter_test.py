import pytest

from c3l4_DAO.practice_works.classes_getter import TodoList
from c3l4_DAO.practice_works.classes_getter import Product
from c3l4_DAO.practice_works.classes_getter import Cart

class TestTodoList:

    def test_add_task(self):
        todo_list = TodoList()
        todo_list.add_task("Выключить свет")
        assert todo_list.count_active() == 1, "Ошибка в добавлении задачи"

    def test_remove_task(self):
        todo_list = TodoList()
        todo_list.add_task("Выключить свет")
        todo_list.remove_task("Выключить свет")
        assert todo_list.count == 1, "Ошибка в удалении задачи"

    def test_count_active(self):
        todo_list = TodoList()
        todo_list.add_task("Выключить свет")
        todo_list.add_task("Включить свет")
        todo_list.add_task("Купить хлеб")
        assert todo_list.count_active() == 3, "Ошибка в подсчете активных задач"

    def test_count_closed(self):
        todo_list = TodoList()
        todo_list.add_task("Выключить свет")
        todo_list.remove_task("Выключить свет")
        assert todo_list.count_closed() == 1, "Ошибка в подсчете выполненных задач"

    def test_count_done(self):
        todo_list = TodoList()
        todo_list.add_task("Выключить свет")
        todo_list.remove_task("Выключить свет")
        assert todo_list.count_done() == 1, "Ошибка в подсчете выполненных задач"

    def test_get_active(self):
        todo_list = TodoList()
        todo_list.add_task("Выключить свет")
        todo_list.add_task("Включить свет")
        todo_list.add_task("Купить хлеб")
        assert todo_list.get_active() == "1. Выключить свет, 2. Включить свет, 3. Купить хлеб", "Ошибка в получении активных задач"

    def test_get_closed(self):
        todo_list = TodoList()
        todo_list.add_task("Выключить свет")
        todo_list.remove_task("Выключить свет")
        assert todo_list.get_closed() == "1. Выключить свет", "Ошибка в получении выполненных задач"

    def test_check_status(self):
        todo_list = TodoList()
        todo_list.add_task("Выключить свет")
        assert todo_list.check_status("Выключить свет") == "Задача 'Выключить свет' - Активная", "Ошибка в проверке статуса задачи"


class TestProduct:

    def test_init(self):
        product = Product("Молоко", 50)
        assert product.name == "Молоко", "Ошибка в инициализации имени"
        assert product.price == 50, "Ошибка в инициализации цены"

    def test_str(self):
        product = Product("Молоко", 50)
        assert str(product.name) == "Молоко", "Ошибка в выводе имени"

    def test_repr(self):
        product = Product("Молоко", 50)
        assert repr(product) == "Product('Молоко', 50)", "Ошибка в выводе имени и цены"

class TestCart:

    def test_init(self):
        cart = Cart()
        assert cart.items == [], "Ошибка в инициализации корзины"

    def test_add(self):
        cart = Cart()
        product = Product("Молоко", 50)
        cart.add(product)
        assert cart.items == [product], "Ошибка в добавлении товара в корзину"

    def tesr_create_and_add (self):
        cart = Cart() 
        cart.create_and_add("waffles", 310)
        assert cart.items == [Product("waffles", 310)], "Ошибка в добавлении товара в корзину"
