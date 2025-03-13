import pytest
from LeetCode_Stolyarov_training.maximize_expression_operators import maximize_expression_operators


parameters = (([0.1, -0.2, 0.6, 50.0, 0, 1.0, -0.2], 280.0), ([2.0, 1.0, -5.0, 0.1], 80.0,), ([1.0, 2.0, -6.0], 9.0))
@pytest.mark.parametrize('array, expected', parameters)
def test_maximize_expression_operators (array, expected):
    assert maximize_expression_operators(array) == expected
