from prime import is_prime
import pytest

#
# Positive test cases
#
@pytest.mark.parametrize("num, expected", [
    (1, False),
    (2, True),
    (3, True),
    (4, False),
    (5, True),
    (16, False),
    (17, True),
    (18, False),
    (19, True),
    (20, False),
    (23, True),
])
def test_is_prime(num, expected):
    assert is_prime(num) == expected

#
# Edge cases
#



#
# Negative test cases
#

@pytest.mark.parametrize("num, expected", [
    (0, False),
    (-1, False),
    ("a", False), # Will fail. Handle this TypeError in is_prime
])
def test_is_prime_negative(num, expected):
    assert is_prime(num) == expected

