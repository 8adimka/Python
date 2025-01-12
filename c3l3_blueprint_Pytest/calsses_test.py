import pytest

from classes import Circle
from classes import Player

class TestCircle:

    def test_get_radius(self):
        circle = Circle(1)
        assert circle.get_radius() == 1, "Ошибка в  радиусе"

    def test_get_diameter(self):
        circle = Circle(1)
        assert circle.get_diameter() == 2, "Ошибка в диаметре"

    def test_get_perimeter(self):
        circle = Circle(1)
        assert round(circle.get_perimeter(), 2) == 6.28, "Ошибка в периметре"

    def test_init_type_error(self):
        with pytest.raises(TypeError):
            circle = Circle("1")

    def test_init_value_error(self):
        with pytest.raises(ValueError):
            circle = Circle(-1)

class TestPlayer:

    def test_change_name(self):
        player = Player("Вася")
        player.change_name("Петя")
        assert player.name == "Петя", "Ошибка в изменении имени"

    def test_add_points(self):
        player = Player("Вася")
        player.add_points(10)
        assert player.get_points() == 10, "Ошибка в добавлении очков"

    def test_get_points(self):
        player = Player("Вася")
        assert player.get_points() == 0, "Ошибка в получении очков"

    players_parameters = [("Вася", 10), ("Петя", -5), ("Маша", 30)] 
    @pytest.mark.parametrize("name, points", players_parameters)
    def test_players(self, name, points):
        player = Player(name)
        player.add_points(points)
        assert player.get_points() == points, "Ошибка в добавлении очков"      
