import pytest
from classes_testing import TodoList  # Предполагается, что класс TodoList находится в файле todo_list.py

def test_initial_tasks_empty():
    """Проверяет, что список задач пуст при инициализации."""
    todo_list = TodoList()
    assert todo_list.fetch_tasks() == [], "Список задач должен быть пустым при инициализации"

def test_add_task():
    """Проверяет добавление задач в список."""
    todo_list = TodoList()
    todo_list.add_task("Buy groceries")
    todo_list.add_task("Walk the dog")
    assert todo_list.fetch_tasks() == ["Buy groceries", "Walk the dog"], "Задачи добавлены неправильно"

def test_add_duplicate_tasks():
    """Проверяет добавление дублирующихся задач."""
    todo_list = TodoList()
    todo_list.add_task("Do homework")
    todo_list.add_task("Do homework")
    assert todo_list.fetch_tasks() == ["Do homework", "Do homework"], "Дублирующиеся задачи должны быть добавлены"
    