from calculator import sum
import pytest

@pytest.fixture(scope="class")
def numbers():
    return [1, 2, 3]

class TestSum:
    def test_sum_all(self, numbers):
        assert sum(numbers) == 6

    def test_sum_extra(self, numbers):
        assert sum(numbers + [4, 5]) == 15

    def test_sum_empty(self):
        assert sum([]) == 0

    def test_sum_negative(self):
        assert sum([-1, -2, -3]) == -6
    
