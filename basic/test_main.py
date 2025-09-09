from main import add, subtract, multiply, divide
import pytest

#
# Positive Tests
#

def test_add_2_and_2_is_5():
    assert add(2, 3) == 5

def test_add_minus_1_and_1_is_0():
    assert add(-1, 1) == 0

def test_add_0_and_0_is_0():
    assert add(0, 0) == 0

def test_subtract_5_and_3_is_2():
    assert subtract(5, 3) == 2

def test_multiply_4_and_3_is_12():
    assert multiply(4, 3) == 12

def test_divide_10_and_2_is_5():
    assert divide(10, 2) == 5

def test_divide_by_zero_raises_value_error():
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        divide(10, 0)
#
# Negative Tests
#