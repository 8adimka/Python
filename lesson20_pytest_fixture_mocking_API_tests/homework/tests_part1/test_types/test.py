import sys
from pathlib import Path
import os
import unittest
import test_types

project_name = Path(os.path.abspath(__file__)).parent.parent.parent.name
cwd = Path.cwd()
parts = cwd.parts
basefolder_index = parts.index(project_name)
basepath = Path(*parts[:basefolder_index + 1])
sys.path.append(str(basepath))
from ttools.skyprotests.tests import SkyproTestCase  # noqa: E402


def wrong_len_summer(*args):
    if len(args) == 1:
        return 0
    for arg in args:
        if not isinstance(arg, int):
            return "ОШИБКА"
    if sum(args) > 300:
        return "Большое число"
    return sum(args)
    

def wrong_type_summer(*args):
    if len(args) == 1:
        return "Мало аргументов"
    for arg in args:
        if not isinstance(arg, int):
            return 0
    if sum(args) > 300:
        return "Большое число"
    return sum(args)

def wrong_sum_summer(*args):
    if len(args) == 1:
        return "Мало аргументов"
    for arg in args:
        if not isinstance(arg, int):
            return "ОШИБКА"
    if sum(args) > 300:
        return 0
    return sum(args)

def wrong_result_summer(*args):
    if len(args) == 1:
        return "Мало аргументов"
    for arg in args:
        if not isinstance(arg, int):
            return "ОШИБКА"
    if sum(args) > 300:
        return "Большое число"
    return "qwe"

def wrong_type_divider(a, b):
    for arg in [a, b]:
        if not isinstance(arg, int):
            return 0
    if b == 0:
        return "Делить на ноль нельзя"
    return a / b

def wrong_second_arg_divider(a,b):
    for arg in [a, b]:
        if not isinstance(arg, int):
            return "ОШИБКА"
    if b == 0:
        return 0
    return a / b

def wrong_divide_divider(a,b):
    for arg in [a, b]:
        if not isinstance(arg, int):
            return "ОШИБКА"
    if b == 0:
        return "Делить на ноль нельзя"
    return "QWE"

class DecorTestCase(SkyproTestCase):
    def setUp(self):
        self.testfunc_devider = test_types.test_divider
        self.testfunc_summer = test_types.test_summer
    
    def test_sum_1(self):
        test_types.summer = wrong_len_summer
        with self.assertRaises(AssertionError,
            msg="%@Проверяют ли Ваше тесты условие когда summer принимает один аргумент"):
            self.testfunc_summer()

    def test_sum_2(self):
        test_types.summer = wrong_type_summer
        with self.assertRaises(AssertionError,
            msg="%@Проверяют ли Ваше тесты условие когда summer принимает в качестве аргумента тот тип"):
            self.testfunc_summer()

    def test_sum_3(self):
        test_types.summer = wrong_sum_summer
        with self.assertRaises(AssertionError,
            msg="%@Проверяют ли Ваше тесты условие когда summer вместо результата выдаёт не тот тип данных"):
            self.testfunc_summer()

    def test_sum_4(self):
        test_types.summer = wrong_result_summer
        with self.assertRaises(AssertionError,
            msg="%@Проверяют ли Ваше тесты условие когда divider вместо результата возвращает строку"):
            self.testfunc_summer()

    def test_div_1(self):
        test_types.divider = wrong_type_divider
        with self.assertRaises(AssertionError,
            msg="%@Проверяют ли Ваше тесты условие когда divider в качестве аргумента принимает не то число"):
            self.testfunc_devider()

    def test_div_2(self):
        test_types.divider = wrong_second_arg_divider
        with self.assertRaises(AssertionError,
            msg="%@Проверяют ли Ваше тесты условие когда divider вторым аргументом принимает ноль"):
            self.testfunc_devider()

    def test_div_3(self):
        test_types.divider = wrong_divide_divider
        with self.assertRaises(AssertionError,
            msg="%@Проверяют ли Ваше тесты условие когда summer вместо числа выдаёт что-то другое"):
            self.testfunc_devider()

if __name__ == "__main__":
    unittest.main()