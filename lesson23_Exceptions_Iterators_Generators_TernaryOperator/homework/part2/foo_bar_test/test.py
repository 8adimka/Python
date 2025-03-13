import sys
from types import GeneratorType
import unittest
from pathlib import Path
import os
from main import foo


project_name = Path(os.path.abspath(__file__)).parent.parent.parent.name
cwd = Path.cwd()
parts = cwd.parts
basefolder_index = parts.index(project_name)
basepath = Path(*parts[: basefolder_index + 1])
sys.path.append(str(basepath))
from ttools.skyprotests.tests import SkyproTestCase  # noqa: E402


class AverageAgeTestCase(SkyproTestCase):

    def setUp(self):
        self.func = foo

    def test_func_is_works_correct(self):
        self.assertTrue(
            self.func.__code__.co_name == '<lambda>',
            "%@Проверьте, является ли переменная foo lambda функцией"
        )
        
        self.assertTrue(
            isinstance(self.func(5), GeneratorType),
            "%@Проверьте, что ваша функция возвращает генератор значений"
        )

        self.assertEqual(
            [x for x in self.func(6)], [0, 1, 4, 9, 16, 25],
            "%@Проверьте, что принцип работы вашей функции остался прежним"
        )


if __name__ == "__main__":
    unittest.main()
