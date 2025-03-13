import sys
import unittest
from pathlib import Path
import os
import main
import inspect
from types import GeneratorType

project_name = Path(os.path.abspath(__file__)).parent.parent.parent.name
cwd = Path.cwd()
parts = cwd.parts
basefolder_index = parts.index(project_name)
basepath = Path(*parts[: basefolder_index + 1])
sys.path.append(str(basepath))
from ttools.skyprotests.tests import SkyproTestCase  # noqa: E402


class IterTestCase(SkyproTestCase):
    def setUp(self):
        self.finder = main.build_dict
        self.towns = main.towns

    def test_iter_works_correct(self):

        self.assertTrue(
            isinstance(self.finder(self.towns), dict),
            "%@Проверьте, что функция build_dict возвращает генератор",
        )

        self.assertFalse(
            len(self.finder.__code__.co_names) == 0,
            "%@Проверьте, что после рефакторинга функция имеет цикл for",
        )


if __name__ == "__main__":
    unittest.main()
