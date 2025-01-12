import math

class Circle:

    def __init__(self, radius):
        if type(radius) not in [int, float]:
            raise TypeError("Радиус должен быть числом, int или float")
        if radius < 0:
            raise ValueError("Радиус должен быть положительным")

        self.radius = radius

    def get_radius(self):
        return self.radius

    def get_diameter(self):
        return self.radius * 2

    def get_perimeter(self):
        return 2 * self.radius * math.pi
    
class Player:

    def __init__(self, name):
        self.name = name
        self.points = 0

    def change_name(self, new_name):
        self.name = new_name

    def add_points(self, number):
        self.points += number

    def get_points(self):
        return self.points
    