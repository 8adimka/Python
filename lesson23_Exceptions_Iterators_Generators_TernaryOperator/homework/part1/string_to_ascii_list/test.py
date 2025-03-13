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
        self.convert = main.convert

    def test_iter_works_correct(self):
        self.assertTrue(
            inspect.isfunction(self.convert),
            "%@Проверьте, что переменная convert является функцией",
        )

        self.assertTrue(
            isinstance(self.convert("hello world!"), list),
            "%@Проверьте, что функция convert возвращает данные типа list",
        )

        answers = [
            (
                "hello world!",
                [104, 101, 108, 108, 111, 32, 119, 111, 114, 108, 100, 33],
            ),
            (
                "afsskdisPOAFNPOSAIN",
                [
                    97, 102, 115, 115, 107, 100, 105, 115, 80, 79, 65, 70, 78, 80, 79, 83, 65, 73, 78,
                ],
            ),
        ]
        for case in answers:
            input_value = case[0]
            expected = case[1]
            self.assertTrue(
                self.convert(input_value) == expected,
                f"%@Проверьте что при входном значении {input_value} "
                f"результат равен {expected}",
            )


if __name__ == "__main__":
    unittest.main()
