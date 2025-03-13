import sys
import unittest
from pathlib import Path
import os
import main
import inspect

project_name = Path(os.path.abspath(__file__)).parent.parent.parent.name
cwd = Path.cwd()
parts = cwd.parts
basefolder_index = parts.index(project_name)
basepath = Path(*parts[: basefolder_index + 1])
sys.path.append(str(basepath))
from ttools.skyprotests.tests import SkyproTestCase  # noqa: E402


class IterTestCase(SkyproTestCase):
    def setUp(self):
        self.fib_gen = main.fib

    def test_iter_works_correct(self):
        self.assertTrue(
            inspect.isgeneratorfunction(self.fib_gen),
            "%@Проверьте, что функция fib является функцией-генератором",
        )
        answers = [
            (1, [0]),
            (2, [0, 1]),
            (3, [0, 1, 1]),
            (4, [0, 1, 1, 2]),
            (5, [0, 1, 1, 2, 3]),
            (10, [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]),
        ]
        for case in answers:
            input_value = case[0]
            expected = case[1]
            result = self.fib_gen(input_value)

            self.assertTrue(
                [x for x in result] == expected,
                f"%@Проверьте что при входном значении {input_value} и преобразовании "
                f"итератора в список результат равен {expected}",
            )


if __name__ == "__main__":
    unittest.main()
