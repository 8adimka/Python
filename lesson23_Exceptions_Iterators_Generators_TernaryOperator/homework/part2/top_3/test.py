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


class FuncTestCase(SkyproTestCase):

    def setUp(self):
        self.func = main.top3

    def test_func__works_correct(self):
        result = self.func('qqqqqqqqqwwwwwwwwwwweeeeeeeeeeetttttest')
        self.assertTrue(
            isinstance(result, list),
            "%@Проверьте, что ваша функция возвращает данные в виде списка"
        )

        self.assertTrue(
            len(result) == 3,
            "%@Проверьте, что Ваша функция возвращает только первые три элемента"
        )

        self.assertTrue(
            result[0] == 'e',
            "%@Проверьте, что элемент с индексом 0 в Вашем списке наиболее повторяемый"
        )

        self.assertTrue(
            result[1] == 'w',
            "%@Проверьте, что элемент с индексом 1 в Вашем списке на втором месте по частоте использования"
        )

        self.assertTrue(
            result[2] == 'q',
            "%@Проверьте, что элемент с индексом 2 в Вашем списке на третьем месте по частоте использования"
        )

        self.assertIn(
            "Counter", inspect.getsource(self.func),
            "%@Проверьте, нам бы хотелось, чтобы вы использовали Counter в теле вашей функции"
        )


if __name__ == "__main__":
    unittest.main()
