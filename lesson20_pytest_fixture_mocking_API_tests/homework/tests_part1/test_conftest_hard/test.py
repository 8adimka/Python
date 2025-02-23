import sys
from pathlib import Path
import os
import unittest
import main_multiplicator_test
import main_summer_test
from functools import reduce

project_name = Path(os.path.abspath(__file__)).parent.parent.parent.name
cwd = Path.cwd()
parts = cwd.parts
basefolder_index = parts.index(project_name)
basepath = Path(*parts[:basefolder_index + 1])
sys.path.append(str(basepath))
from ttools.skyprotests.tests import SkyproTestCase  # noqa: E402

def error_check_summer(*args):
    return sum(args) + 1

def error_check_multiplicator(*args):
    return reduce(lambda x, y: x*y, args) + 1

class DecorTestCase(SkyproTestCase):
    def setUp(self):
        self.testfunc_sum = main_summer_test.test_sum_numbers
        self.testfunc_mult = main_multiplicator_test.test_multiplicator
        self.args = [1, 2, 3, 4, 5]
        self.checkpath = basepath.joinpath('tests_part1', 'test_conftest_hard')

    def test_file_conftest_is_created(self):
        file = 'conftest.py'
        
        self.assertTrue(os.path.exists(self.checkpath.joinpath(file)),
        f"%@ Проверьте что создали файл {file}")

    def conftest_has_exists(self):
        import conftest
        self.assertTrue(
            hasattr(conftest, 'list_creator'),
            "%@Проверьте, что файл conftest.py содержит фикстуру list_creator"
         )

    def test_sum_selfcheck(self):
        main_multiplicator_test.multiplicator = error_check_multiplicator
        with self.assertRaises(AssertionError, 
            msg=("%@Проверьте что Ваш тест проверяет функцию multiplicator"
                 " в соответствии с условием задания")):
            self.testfunc_mult(self.args)

    def test_one_selfcheck(self):
        main_summer_test.summer = error_check_summer
        with self.assertRaises(AssertionError, 
            msg=("%@Проверьте что Ваш тест проверяет функцию"
                 " summer в соответствии условием задания")):
            self.testfunc_sum(self.args)


if __name__ == "__main__":
    unittest.main()