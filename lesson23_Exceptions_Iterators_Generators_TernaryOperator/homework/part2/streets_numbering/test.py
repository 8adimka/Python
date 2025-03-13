import sys
from typing import Tuple
import unittest
from pathlib import Path
import os
import main

project_name = Path(os.path.abspath(__file__)).parent.parent.parent.name
cwd = Path.cwd()
parts = cwd.parts
basefolder_index = parts.index(project_name)
basepath = Path(*parts[: basefolder_index + 1])
sys.path.append(str(basepath))
from ttools.skyprotests.tests import SkyproTestCase  # noqa: E402


class FuncTestCase(SkyproTestCase):

    def setUp(self):
        self.func = main.get_tuples

    def test_func__works_correct(self):
        result = self.func(['test1', 'test2'])
        long_result = self.func(['test1','test2','test3'])
        self.assertTrue(
            isinstance(result, list),
            "%@Проверьте, что ваша функция возвращает данные в виде списка"
        )

        self.assertTrue(
            len(result) == 2,
            "%@Проверьте, что Ваша функция возвращает столько же элементов "
            "сколько передано в списке"
        )
        self.assertTrue(
            len(long_result) == 3,
            "%@Проверьте, что Ваша функция возвращает столько же элементов "
            "сколько передано в списке"
        )
        self.assertTrue(
            isinstance(result[0], tuple) and isinstance(result[1], tuple),
            "%@Проверьте, что результат, который возвращает Ваша функция состоит из кортежей"
        )

        self.assertTrue(
            result[0][1] == 1,
            "%@Проверьте, что нумерация улиц начинается с единицы"
        )

        self.assertTrue(
            result[0][0] == 'test1' and result[0][1] == 1,
            "%@Проверьте, что список состоит из кортежей а каждый кортеж состоит из названия улицы"
            " и её порядкового номера"
        )

        self.assertTrue(
            result[1][0] == 'test2' and result[1][1] == 2,
            "%@Проверьте, что номера улиц в кортежах идут по порядку"
        )

if __name__ == "__main__":
    unittest.main()
