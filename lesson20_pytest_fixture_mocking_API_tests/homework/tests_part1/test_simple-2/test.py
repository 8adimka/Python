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

def error_check_divider(*args):
    for arg in args:
        if not isinstance(arg, int):
            return "ОШБКА"

def wrong_result_divider(a , b):
    return a / b + 1

def zero_divider(a, b):
    if b == 0:
        return 500


class DecorTestCase(SkyproTestCase):
    def setUp(self):
        self.testfunc_sum = test_simple.test_result
        self.testfunc_one_arg = test_simple.test_zero_divide_error
        self.testfunc_big_number = test_simple.test_error
    
    def test_sum_selfcheck(self):
        test_simple.divider = wrong_result_divider
        with self.assertRaises(AssertionError,
            msg="%@Проверьте что Ваш тест проверяет первое условие задания"):
            self.testfunc_sum()

    def test_one_selfcheck(self):
        test_simple.divider = zero_divider
        with self.assertRaises(AssertionError,
            msg="%@Проверьте что Ваш тест проверяет второе условие задания"):
            self.testfunc_big_number()

    def test_many_selfcheck(self):
        test_simple.divider = error_check_divider
        with self.assertRaises(AssertionError,
            msg="%@Проверьте что Ваш тест проверяет второе условие задания"):
            self.testfunc_one_arg()


if __name__ == "__main__":
    unittest.main()