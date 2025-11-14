class Enimal:
    def make_sound(self):
        return "Some generic sound"


class Dog(Enimal):
    def __init__(self, name):
        self._name = name

    def __repr__(self):
        return f"Dog named {self._name}"

    @property
    def name(self):
        return self._name + " the Dog"

    def set_name(self, new_name):
        self._name = new_name


dog1 = Dog("Buddy")

print(dog1)

print(dog1.name)

dog1.set_name("Max")
print(dog1.name)
