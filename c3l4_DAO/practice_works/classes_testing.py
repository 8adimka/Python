import unittest

class TodoList:
    def __init__(self):
        self._tasks = []
      
    def add_task(self, new_task):
        self._tasks.append(new_task)
     
    def fetch_tasks(self):
        return self._tasks

class TestTodoList(unittest.TestCase):

    def setUp(self):
        """Создаем экземпляр TodoList перед каждым тестом."""
        self.todo_list = TodoList()

    def test_add_single_task(self):
        """Тестируем добавление одной задачи."""
        self.todo_list.add_task("Купить молоко")
        self.assertEqual(self.todo_list.fetch_tasks(), ["Купить молоко"])

    def test_add_multiple_tasks(self):
        """Тестируем добавление нескольких задач."""
        self.todo_list.add_task("Купить молоко")
        self.todo_list.add_task("Сделать домашку")
        self.assertEqual(self.todo_list.fetch_tasks(), ["Купить молоко", "Сделать домашку"])

    def test_add_empty_task(self):
        """Тестируем добавление пустой задачи."""
        self.todo_list.add_task("")
        self.assertEqual(self.todo_list.fetch_tasks(), [""])

    def test_add_task_with_spaces(self):
        """Тестируем добавление задачи с пробелами."""
        self.todo_list.add_task("     ")
        self.assertEqual(self.todo_list.fetch_tasks(), ["     "])

if __name__ == "__main__":
    unittest.main()
    