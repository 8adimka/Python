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
            main.Town("atest1", "МО"),
            main.Town("ctest2", "test-region"),
            main.Town("btest3", "МО")
        ]

    def test_func__works_correct(self):
        self.assertTrue(
            isinstance(main.sort_towns(self.towns_list), list),
            "%@Проверьте, что ваша функция возвращает список"
        )
        result_list = main.sort_towns(self.towns_list)
        
        self.assertTrue(
            result_list == ["atest1", "btest3", "ctest2"],
            "%@Проверьте что Ваша функция возвращает корректный результат"
        )

if __name__ == "__main__":
    unittest.main()
