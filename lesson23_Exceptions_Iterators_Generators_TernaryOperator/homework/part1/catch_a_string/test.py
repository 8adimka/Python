import sys
import unittest
from pathlib import Path
import os

from main import cant_work

project_name = Path(os.path.abspath(__file__)).parent.parent.parent

sys.path.append(str(project_name))
from ttools.skyprotests.tests import SkyproTestCase  # noqa: E402


class ExceptionTestCase(SkyproTestCase):
    def test_init_returns_class_instances(self):
        test_list = [5]
        try:
            result = cant_work(test_list)
        except Exception as e:
            self.fail("%@Проверьте, что функция cant_work перехватывает исключение")

        self.assertTrue(
            result == "Исключение поймано",
            "%@Проверьте, что если в теле функции исключение перехвачено, тогда функция"
            "возвращает строку 'Исключение поймано'",
        )


if __name__ == "__main__":
    unittest.main()
