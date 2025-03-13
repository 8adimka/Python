import sys
import unittest
from pathlib import Path
import os
import main

project_name = Path(os.path.abspath(__file__)).parent.parent.parent

sys.path.append(str(project_name))
from ttools.skyprotests.tests import SkyproTestCase  # noqa: E402


def ordering():
    suite = unittest.TestSuite()
    suite.addTest(ExceptionTestCase("test_parse_error_is_exists"))
    suite.addTest(ExceptionTestCase("test_init_returns_class_instances"))
    return suite


class ExceptionTestCase(SkyproTestCase):
    def test_parse_error_is_exists(self):
        self.assertTrue(
            hasattr(main, "ParseError"),
            "%@Проверьте что вы создали в модуле исключение ParseError",
        )

    def test_parse_func_raises_expected_exception(self):
        exception = main.ParseError
        with self.assertRaises(
            exception,
            msg="%@Проверьте если значение часов превышает 25 тогда срабабатывает исключение ParseError",
        ):
            main.parse(25, 1)
        with self.assertRaises(
            exception,
            msg="%@Проверьте если значение часов меньше нуля тогда срабатывает исключение ParseError",
        ):
            main.parse(-1, 1)
        with self.assertRaises(
            exception,
            msg="%@Проверьте если значение часов превышает 59 тогда срабатывает исключение ParseError",
        ):
            main.parse(23, 60)
        with self.assertRaises(
            exception,
            msg="%@Проверьте если значение минут меньше нуля тогда срабатывает исключение ParseError",
        ):
            main.parse(1, -1)

        try:
            main.parse(1, 1) == None,
        except:
            self.fail(
                "%@Проверьте, что функция не вызывает ошибок, если данные корректны"
            )


if __name__ == "__main__":
    unittest.main()
