import pytest 

# app.py
def sum_func(a, b):
    return a + b

def call_method():
    raise Exception()


# test_app.py
class TestSumFunc:
    def test_sum_positive(self):
        c = sum_func(1, 1)
        assert c > 0
        assert c == 2

    def test_sum_positive_and_negative(self):
        c = sum_func(1, -1)
        assert c == 0

    def test_sum_negative(self):
        c = sum_func(-30, -10)
        assert c < 0
        assert c == -40


    parameters = [(1, 2, 3), (3, 4, 7), (-3, -4, -7)]

    @pytest.mark.parametrize('numbers', parameters)
    def test_sum_numbers(self, numbers: list[tuple]):
        assert sum_func(numbers[0], numbers[1]) == numbers[2]

    def test_has_to_fail(self):
        with pytest.raises(Exception):
            call_method()

    @pytest.mark.skip(reason="I know what I'm doing")
    def test_skip(self):
        raise Exception()

