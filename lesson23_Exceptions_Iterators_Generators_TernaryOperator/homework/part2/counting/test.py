import sys
import unittest
from pathlib import Path
import os
import main
import inspect
from collections import namedtuple

project_name = Path(os.path.abspath(__file__)).parent.parent.parent.name
cwd = Path.cwd()
parts = cwd.parts
basefolder_index = parts.index(project_name)
basepath = Path(*parts[: basefolder_index + 1])
sys.path.append(str(basepath))
from ttools.skyprotests.tests import SkyproTestCase  # noqa: E402


class FuncTestCase(SkyproTestCase):

    def setUp(self):
        self.func = main.counter
        self.Town = namedtuple('Town', ['name', 'region'])
        self.towns = [
            self.Town('балашиха', 'test1'), 
            self.Town('химки', 'test3'), 
            self.Town('тула', 'test1'),
            self.Town('test2', 'test2'), 
            self.Town('test22', 'test2'), 
            self.Town('test44', 'test4'), 
            self.Town('test44', 'test4'), 
            ]

    def test_func__works_correct(self):
        result = self.func(self.towns)
        self.assertTrue(
            isinstance(result, dict),
            "%@Проверьте, что ваша функция возвращает данние в виде словаря"
        )

        self.assertTrue(
            len(result) == 4,
            "%@Проверьте, что словарь который возвращает Ваша функция содержить правильное количество"
            " элементов (количество элементов должно соответсвовать количеству регионов)"
        )

        self.assertTrue(
            result.get("test4") == 2,
            "%@Проверьте, что Ваша функция правильно рассчитывает количество городов в регионе"
        )

        self.assertIn(
            "defaultdict", inspect.getsource(self.func),
            "%@Проверьте, нам бы хотелось, чтобы вы использовали defaultdict в теле вашей функции"
        )

if __name__ == "__main__":
    unittest.main()
