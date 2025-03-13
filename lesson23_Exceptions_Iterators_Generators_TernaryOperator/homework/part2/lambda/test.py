import sys
import unittest
from pathlib import Path
import os
from main import foo
import inspect

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
        self.assertFalse(
            self.func.__code__.co_name == '<lambda>',
            "%@Проверьте, что ваша функция не является lambda-объектом"
        )

        self.assertNotIn(
            "lambda", inspect.getsource(self.func),
            "%@Проверьте, что вы не использовали lambda в вашей функции"
        )
        
        self.assertTrue(
            isinstance(self.func(a=1, b=2), dict),
            "%@Проверьте, что ваша функция возвращает словарь"
        )

        try:
            self.func(a=1, b=2, c=4, qwexyz=50, testtest=20)
        except:
            self.fail("%@Проверьте, что ваша функция может принимать любое количество именованных аргументов")



if __name__ == "__main__":
    unittest.main()
