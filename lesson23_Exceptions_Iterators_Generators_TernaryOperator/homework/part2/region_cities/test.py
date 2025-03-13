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


class AverageAgeTestCase(SkyproTestCase):

    def setUp(self):
        self.towns_list = [
            main.Town("test1", "МО"),
            main.Town("test2", "test-region"),
            main.Town("test3", "МО")
        ]

    def test_func__works_correct(self):
        self.assertTrue(
            isinstance(main.filter_towns(self.towns_list), list),
            "%@Проверьте, что ваша функция возвращает список"
        )
        result_list = main.filter_towns(self.towns_list)
        
        self.assertTrue(
            result_list == ["test1", "test3"],
            "%@Проверьте что Ваша функция возвращает корректный результат"
        )

if __name__ == "__main__":
    unittest.main()
