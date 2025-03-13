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
        self.filter = main.filter_rrr

    def test_iter_works_correct(self):
        self.assertTrue(
            inspect.isfunction(self.filter),
            "%@Проверьте, что переменная filter_rrr является функцией",
        )

        self.assertTrue(
            isinstance(self.filter("Хорошо учиться новому"), str),
            "%@Проверьте, что функция filter_rrr возвращает данные типа String",
        )

        answers = [
            ("Без труда не выманишь и рыбку из пруда", "Без не выманишь и из"),
            ("Хороший плохой добрый злой молодой старый", "плохой злой молодой"),
        ]
        for case in answers:
            input_value = case[0]
            expected = case[1]
            answer = self.filter(input_value)
            self.assertTrue(
                answer == expected,
                f"%@Ваша функция работает неправильно мы передали ей текст {input_value} "
                f" и получили {answer}, тогда как результат должен быть {expected}",
            )


if __name__ == "__main__":
    unittest.main()
