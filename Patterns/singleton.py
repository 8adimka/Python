import datetime
import time


class Singleton(object):
    _instance = None
    _vault: dict = {}  # Приватный атрибут для хранения данных

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance

    @property
    def vault(self) -> dict:
        """Геттер: возвращает весь словарь."""
        return self._vault

    @vault.setter
    def vault(self, value: dict):
        """Сеттер: заменяет весь словарь."""
        if not isinstance(value, dict):
            raise ValueError("Только словарь!")
        self._vault = value

    def set_value(self, key, value):
        """Отдельный метод для установки значения по ключу."""
        self._vault[key] = value

    def get_value(self, key):
        """Отдельный метод для получения значения по ключу."""
        return self._vault.get(key)

    def check(self, key):
        """Проверка наличия ключа."""
        return key in self._vault


class Source:
    def get_something(self, key):
        time.sleep(5)
        return "result"


class App:
    def __init__(self):
        self.cache = Singleton()
        self.source = Source()

    def process(self, key):
        start_time = datetime.datetime.now()
        if self.cache.check(key):
            result = self.cache.get_value(key)
        else:
            result = self.source.get_something(key)
            self.cache.set_value(key, result)
        print(datetime.datetime.now() - start_time)

        return result


# Создаём экземпляр Singleton
app1 = App()
app2 = App()
print(app1 is app2)  # False (это разные объекты)
print(app1.cache is app2.cache)  # True (это один и тот же объект)

# Работа с vault:
app1.cache.set_value("secret", 42)  # Устанавливаем значение
print(app1.cache.get_value("secret"))  # 42
print(app2.cache.check("secret"))  # True

# Через property (геттер/сеттер):
print(app1.cache.vault)  # {'secret': 42} (возвращает весь словарь)
app1.cache.vault = {"new_key": 100}  # Заменяем весь словарь (сеттер)

print(app1.cache.get_value("new_key"))
print(app2.cache.vault["new_key"])

app1.process(1)
app1.process(1)

app1.process(3)
app2.process(1)
