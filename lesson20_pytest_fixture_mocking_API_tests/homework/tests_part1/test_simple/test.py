import sys
from pathlib import Path
import os
import unittest
import test_simple

project_name = Path(os.path.abspath(__file__)).parent.parent.parent.name
cwd = Path.cwd()
parts = cwd.parts
basefolder_index = parts.index(project_name)
basepath = Path(*parts[:basefolder_index + 1])
sys.path.append(str(basepath))
from ttools.skyprotests.tests import SkyproTestCase  # noqa: E402

def error_check_summer(*args):
    for arg in args:
        if not isinstance(arg, int):
            return "ОШБКА"

def sum_wrong_summer(*args):
    return sum(args) + 1

def big_number_wrong_summer(*args):
    if sum(args) < 300:
        return "Большое число"

def none_args_summer(*args):
    if len(args) != 1:
        return "Мало аргументов"


class DecorTestCase(SkyproTestCase):
    def setUp(self):
        self.testfunc_sum = test_simple.test_sum
        self.testfunc_one_arg = test_simple.test_one_arg
        self.testfunc_big_number = test_simple.test_big_number
        self.testfunc_wrong_arg = test_simple.test_wrong_arg
    
    def test_sum_selfcheck(self):
        test_simple.summer = sum_wrong_summer
        with self.assertRaises(AssertionError,
            msg="%@Проверьте что Ваш тест проверяет первое условие задания"):
            self.testfunc_sum()

    def test_one_selfcheck(self):
        test_simple.summer = big_number_wrong_summer
        with self.assertRaises(AssertionError,
            msg="%@Проверьте что Ваш тест проверяет второе условие задания"):
            self.testfunc_big_number()

    def test_many_selfcheck(self):
        test_simple.summer = none_args_summer
        with self.assertRaises(AssertionError,
            msg="%@Проверьте что Ваш тест проверяет второе условие задания"):
            self.testfunc_one_arg()
        
    def test_error_selfcheck(self):
        test_simple.summer = error_check_summer
        with self.assertRaises(AssertionError,
            msg="%@Проверьте что Ваш тест проверяет второе условие задания"):
            self.testfunc_wrong_arg()

if __name__ == "__main__":
    unittest.main()