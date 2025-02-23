import sys
from pathlib import Path
import os
import unittest
import main_params_test

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
        self.testfunc_sum = main_params_test.test_sum_numbers
        self.args = [
            [(5, 7, 9), 21],
            [(302, ), "Мало аргументов"], 
            [(260, 70), "Большое число"],
            [("Qwe",), "ОШИБКА"], 
        ]
    
    def test_sum_selfcheck(self):
        main_params_test.summer = sum_wrong_summer
        with self.assertRaises(AssertionError, 
            msg="%@Проверьте что Ваш тест проверяет первое условие задания"):
            self.testfunc_sum(*self.args[0])

    def test_one_selfcheck(self):
        main_params_test.summer = none_args_summer
        with self.assertRaises(AssertionError, 
            msg="%@Проверьте что Ваш тест проверяет второе условие задания"):
            self.testfunc_sum(*self.args[1])

    def test_many_selfcheck(self):
        main_params_test.summer = big_number_wrong_summer
        with self.assertRaises(AssertionError, 
            msg="%@Проверьте что Ваш тест проверяет третье условие задания"):
            self.testfunc_sum(*self.args[2])
        
    def test_error_selfcheck(self):
        main_params_test.summer = error_check_summer
        with self.assertRaises(AssertionError, 
            msg="%@Проверьте что Ваш тест проверяет четвёртое условие задания"):
            self.testfunc_sum(*self.args[3])

if __name__ == "__main__":
    unittest.main()