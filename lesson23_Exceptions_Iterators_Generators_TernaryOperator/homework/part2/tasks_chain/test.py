import sys
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


class AverageAgeTestCase(SkyproTestCase):

    def setUp(self):
        self.func = main.get_ids
        self.towns_list = [
            main.Town(3, "ctest1", "МО"),
            main.Town(1, "btest2", "test-region"),
            main.Town(2, "atest3", "МО")
        ]

        self.towns_list2 = [
            main.Town(3, "ctest1", "МО"),
            main.Town(1, "btest2", "test-region"),
            main.Town(2, "atest3", "МО"),
            main.Town(4, "gtest2", "test-region"),
            main.Town(5, "ftest2", "МО")
        ]

    def test_func__works_correct(self):
        self.assertTrue(
            isinstance(self.func(self.towns_list), list),
            "%@Проверьте, что ваша функция возвращает список"
        )
        result_list = self.func(self.towns_list)
        
        self.assertTrue(
            result_list == [2, 3],
            "%@Проверьте что Ваша функция возвращает корректный результат"
        )

        result_list = self.func(self.towns_list2)
        
        self.assertTrue(
            result_list == [2, 3, 5],
            "%@Проверьте что Ваша функция возвращает корректный результат"
        )


if __name__ == "__main__":
    unittest.main()
