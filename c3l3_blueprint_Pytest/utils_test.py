import pytest
from utils import ticket_price
from utils import get_circle_square
from utils import get_verbal_grade
from utils import get_period

ticket_price_parameters = [(0, "Бесплатно"), (0.5, "Бесплатно"), (6, "Бесплатно"), (7, "100 рублей"), (17, "100 рублей"), (18, "200 рублей"), (24, "200 рублей"), (25, "300 рублей"), (59, "300 рублей"), (60, "Бесплатно"), (100, "Бесплатно"), (-1, "Ошибка")]
@pytest.mark.parametrize("age, expected", ticket_price_parameters)
def test_ticket_price(age, expected):
    assert ticket_price(age) == expected



@pytest.mark.parametrize("radius, expected", [(0, 0),(1, 3.14), (2, 12.57), (3, 28.27), (4, 50.27), (5, 78.54), (6, 113.10), (7, 153.94), (8, 201.06), (9, 254.47)])
def test_get_circle_square(radius, expected):
    assert get_circle_square(radius) == expected

def test_get_circle_square_value_error():
    with pytest.raises(ValueError):
        get_circle_square(-2)

def test_get_circle_square_type_error():
    with pytest.raises(TypeError):
        get_circle_square("2")



grade_parameters = [
    (2, "Плохо"),
    (3, "Удовлетворительно"),
    (4, "Хорошо"),
    (5, "Отлично"),
]
@pytest.mark.parametrize("grade, expected",grade_parameters)
def test_get_verbal_grade(grade, expected):
    assert get_verbal_grade(grade) == expected

grade_exceptions = [
    (1, ValueError),
    (6, ValueError),
    ("5", TypeError),
    (5.0, TypeError),
]
@pytest.mark.parametrize("grade, exception", grade_exceptions)
def test_get_verbal_grade_exceptions(grade, exception):
    with pytest.raises(exception):
        get_verbal_grade(grade)



period_parameters = [(0, "ночь"), (6, "ночь"), (7, "утро"), (11, "утро"), (12, "день"), (17, "день"), (18, "вечер"), (23, "вечер"), (1, "ночь")]
@pytest.mark.parametrize("hour, expected", period_parameters)
def test_get_period(hour, expected):
    assert get_period(hour) == expected

period_exceptions = [(25, ValueError), (-1, ValueError), ("5", TypeError), (5.0, TypeError)]
@pytest.mark.parametrize("hour, exception", period_exceptions)
def test_get_period_exceptions(hour, exception):
    with pytest.raises(exception):
        get_period(hour)
