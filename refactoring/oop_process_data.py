""" Explanation:
This OOP version of data_process.py follows SOLID principles: OCP / DIP / SRP.
i.e.
- Swap MeanStatistic for MedianStatistic or ModeStatistic without touching pipeline code (OCP/Strategy).
- Replace PrintPresenter with a LoggerPresenter or JsonPresenter (DIP).
- Each class has one responsibility (SRP).
"""

from abc import ABC, abstractmethod
from typing import Iterable, List

#
# --- Roles / Interfaces ---
#
class Cleaner(ABC):
    @abstractmethod
    def clean(self, data: Iterable[str]) -> List[str]: ...

class Extractor(ABC):
    @abstractmethod
    def extract(self, data: Iterable[str]) -> List[int]: ...

class Statistic(ABC):
    def validate(self, numbers: Iterable[int]) -> None:
        if not numbers:
            raise ValueError("No numbers to compute statistic.")
        return numbers

    @abstractmethod
    def compute(self, numbers: Iterable[int]) -> float: ...

class Presenter(ABC):
    @abstractmethod
    def present(self, label: str, value: float) -> None: ...

#
# --- Concrete implementations ---
#
class WhitespaceCleaner(Cleaner):
    def clean(self, data: Iterable[str]) -> List[str]:
        return [x.strip() for x in data if x]

class DigitStringToIntExtractor(Extractor):
    def extract(self, data: Iterable[str]) -> List[int]:
        return [int(x) for x in data if x.isdigit()]

class MeanStatistic(Statistic):
    def compute(self, numbers: Iterable[int]) -> float:
        nums = list(numbers)
        if not nums:
            raise ValueError("No numbers to compute statistic.")
        return sum(nums) / len(nums)

class MedianStatistic(Statistic):
    def compute(self, numbers):
        sorted_nums = sorted(numbers)
        n = len(sorted_nums)
        mid = n // 2
        if n % 2 == 0:
            return (sorted_nums[mid - 1] + sorted_nums[mid]) / 2
        return sorted_nums[mid]

class PrintPresenter(Presenter):
    def present(self, label: str, value: float) -> None:
        print(f"{label}: {value}")

#
# --- Pipeline orchestrator ---
#
class DataPipeline:
    def __init__(self, cleaner: Cleaner, extractor: Extractor, statistic: Statistic, presenter: Presenter | None = None):
        self.cleaner = cleaner
        self.extractor = extractor
        self.statistic = statistic
        self.presenter = presenter  # optional to keep presentation separate

    def run(self, raw: Iterable[str], label: str = "Result") -> float:
        cleaned = self.cleaner.clean(raw)
        numbers = self.extractor.extract(cleaned)
        value = self.statistic.compute(numbers)
        if self.presenter:
            self.presenter.present(label, value)
        return value

#
# --- Usage ---
#
pipeline = DataPipeline(
    cleaner=WhitespaceCleaner(),
    extractor=DigitStringToIntExtractor(),
    statistic=MeanStatistic(), # Can be swapped for MedianStatistic
    presenter=PrintPresenter(),  # or None if you want pure compute
)

result = pipeline.run([" 12", "abc", " 5", " 20 "], label="Average")