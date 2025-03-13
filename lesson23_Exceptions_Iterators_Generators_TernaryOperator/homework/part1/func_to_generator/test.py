import sys
import unittest
from pathlib import Path
import os
import main
from types import GeneratorType

project_name = Path(os.path.abspath(__file__)).parent.parent.parent.name
cwd = Path.cwd()
parts = cwd.parts
basefolder_index = parts.index(project_name)
basepath = Path(*parts[: basefolder_index + 1])
sys.path.append(str(basepath))
from ttools.skyprotests.tests import SkyproTestCase  # noqa: E402


class IterTestCase(SkyproTestCase):
    def setUp(self):
        self.finder = main.find
        path = Path(__file__).parent
        self.path = path.joinpath("apache_logs.txt")

    def test_iter_works_correct(self):

        self.assertTrue(
            isinstance(self.finder(self.path, "image"), GeneratorType),
            "%@Проверьте, что функция find возвращает генератор",
        )

        gen = self.finder(self.path, "208.115.111.72")
        lst = [value for value in gen]

        self.assertTrue(
            len(lst) == 83,
            "%@Проверьте, что ваша функция правильно выбирает строки."
            "Мы попытались найти строки содержащие '208.115.111.72' и с помощью "
            f"Вашей функции получили {len(lst)} строки,  тогда как должно быть 83",
        )


if __name__ == "__main__":
    unittest.main()
