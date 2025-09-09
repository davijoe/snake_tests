from calculator import sum
import pytest

@pytest.fixture(scope="class")
def numbers():
    return [1, 2, 3]

# Don't do this
""" numbers = [1, 2, 3]
class TestSumBasic:
    def test_sum_extra(self):
        numbers.append(4)
        assert sum(numbers) == 10

    def test_sum_basic(self):
        assert sum(numbers) == 6 """
    

class TestSumFixture:
    def test_sum_extra(self, numbers):
        assert sum(numbers + [4, 5]) == 15
    
    def test_sum_all(self, numbers):
        assert sum(numbers) == 6

    def test_sum_empty(self):
        assert sum([]) == 0

    def test_sum_negative(self):
        assert sum([-1, -2, -3]) == -6
    
