import sys
import unittest
from pathlib import Path
import os
from main import calc_average_age
import json

project_name = Path(os.path.abspath(__file__)).parent.parent.parent
sys.path.append(str(project_name))
from ttools.skyprotests.tests import SkyproTestCase  # noqa: E402


class AverageAgeTestCase(SkyproTestCase):
    def test_func_is_works_correct(self):
        path = Path(__file__)
        with open(path.parent.joinpath("vk.json"), "r") as f:
            response_data = json.load(f)
        try:
            result = calc_average_age(response_data)
        except (KeyError, TypeError):
            self.fail(
                "%@Функция выбрасывает исключения KeyError и TypeError."
                "Возможно функция пытается обратиться к объекту словаря"
                "по несуществующему ключу."
            )
        except (ValueError, AttributeError):
            self.fail(
                "%@Функция выбрасывает исключения ValueError, AttributeError."
                "Возможно в код функции обращается к несуществующему аттрибуту"
                "или же неверен тип принимаемых данных."
            )


if __name__ == "__main__":
    unittest.main()
