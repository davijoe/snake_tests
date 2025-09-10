""" Explanation:
This OOP version of data_process.py follows SOLID principles: OCP / DIP / SRP.
i.e.
- Swap MeanStatistic for MedianStatistic or ModeStatistic without touching pipeline code (OCP/Strategy).
- Replace PrintPresenter with a LoggerPresenter or JsonPresenter (DIP).
- Each class has one responsibility (SRP).
"""

from abc import ABC, abstractmethod
from typing import Iterable, List, Any, Dict

import logging
import json
import time

#
# --- Loggin Utilities ---
#
def configure_logging(level: int = logging.INFO) -> None:
    """
    Simple, opinionated logging setup:
    - Human-readable format with timestamp + logger name.
    - You can swap to JSON by replacing the Formatter.
    """
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler.setFormatter(formatter)

    root = logging.getLogger()
    root.handlers.clear()
    root.addHandler(handler)
    root.setLevel(level)


class Loggable:
    """
    Mixin that provides a _log() helper for structured logging.
    Usage: self._log('INFO', 'event_name', key=value, ...)
    """
    def __init__(self, logger: logging.Logger | None = None) -> None:
        self._logger = logger or logging.getLogger(self.__class__.__name__)

    def _log(self, level: str, event: str, **fields: Any) -> None:
        lvl = getattr(logging, level.upper(), logging.INFO)
        payload: Dict[str, Any] = {"event": event, **fields}
        # Dump dict as JSON for easy parsing in logs
        self._logger.log(lvl, json.dumps(payload, ensure_ascii=False))

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
    def validate(self, numbers: Iterable[int]) -> list[int]:
        if not numbers:
            raise ValueError("No numbers to compute.")
        return numbers

    @abstractmethod
    def compute(self, numbers: Iterable[int]) -> float: ...

class Presenter(ABC):
    @abstractmethod
    def present(self, label: str, value: float) -> None: ...

#
# --- Concrete implementations ---
#
class WhitespaceCleaner(Loggable, Cleaner):
    def __init__(self, **kw) -> None:
        super().__init__(**kw)

    def clean(self, data: Iterable[str]) -> List[str]:
        t0 = time.perf_counter()
        # Clean: strip whitespace and drop falsy values (e.g., "", None)
        out = [x.strip() for x in data if x]
        duration_ms = (time.perf_counter() - t0) * 1000
        self._log("INFO", "clean_done", items_in=len(list(data)) if hasattr(data, "__len__") else None,
                  items_out=len(out), duration_ms=round(duration_ms, 3))
        return out


class DigitStringToIntExtractor(Loggable, Extractor):
    def __init__(self, **kw) -> None:
        super().__init__(**kw)

    def extract(self, data: Iterable[str]) -> List[int]:
        t0 = time.perf_counter()
        kept, dropped = 0, 0
        out: List[int] = []
        # Convert only pure digit strings (no signs, no decimals)
        for x in data:
            if x.isdigit():
                out.append(int(x))
                kept += 1
            else:
                dropped += 1
        duration_ms = (time.perf_counter() - t0) * 1000
        self._log("INFO", "extract_done",
                  kept=kept, dropped=dropped, items_out=len(out), duration_ms=round(duration_ms, 3))
        return out


class MeanStatistic(Loggable, Statistic):
    def __init__(self, **kw) -> None:
        super().__init__(**kw)

    def compute(self, numbers: Iterable[int]) -> float:
        t0 = time.perf_counter()
        nums = self.validate(numbers)
        value = sum(nums) / len(nums)
        duration_ms = (time.perf_counter() - t0) * 1000
        self._log("INFO", "compute_mean_done", count=len(nums), value=value, duration_ms=round(duration_ms, 3))
        return value


class MedianStatistic(Loggable, Statistic):
    def __init__(self, **kw) -> None:
        super().__init__(**kw)

    def compute(self, numbers: Iterable[int]) -> float:
        t0 = time.perf_counter()
        nums = self.validate(numbers)
        sorted_nums = sorted(nums)
        n = len(sorted_nums)
        mid = n // 2
        if n % 2 == 0:
            value = (sorted_nums[mid - 1] + sorted_nums[mid]) / 2
        else:
            value = float(sorted_nums[mid])
        duration_ms = (time.perf_counter() - t0) * 1000
        self._log("INFO", "compute_median_done", count=n, value=value, duration_ms=round(duration_ms, 3))
        return value

class PrintPresenter(Loggable, Presenter):
    def __init__(self, **kw) -> None:
        super().__init__(**kw)

    def present(self, label: str, value: float) -> None:
        t0 = time.perf_counter()
        print(f"{label}: {value}")
        duration_ms = (time.perf_counter() - t0) * 1000
        self._log("INFO", "present_print_done", label=label, value=value, duration_ms=round(duration_ms, 3))


class LoggerPresenter(Loggable, Presenter):
    """
    Presenter that logs the result as a structured event.
    Useful when you want machine-parsable results instead of stdout printing.
    """
    def __init__(self, level: str = "INFO", **kw) -> None:
        super().__init__(**kw)
        self._level = level

    def present(self, label: str, value: float) -> None:
        t0 = time.perf_counter()
        # Emit a single structured event (e.g., for ingestion by log pipeline)
        self._log(self._level, "present_result", label=label, value=value)
        duration_ms = (time.perf_counter() - t0) * 1000
        # Optional: emit a second event for timing
        self._log("INFO", "present_logger_done", label=label, duration_ms=round(duration_ms, 3))
#
# --- Pipeline orchestrator ---
#
class DataPipeline(Loggable):
    def __init__(self, cleaner: Cleaner, extractor: Extractor, statistic: Statistic,
                 presenter: Presenter | None = None, **kw) -> None:
        super().__init__(**kw)
        self.cleaner = cleaner
        self.extractor = extractor
        self.statistic = statistic
        self.presenter = presenter  # optional to keep presentation separate

    def run(self, raw: Iterable[str], label: str = "Result") -> float:
        self._log("INFO", "pipeline_start", label=label)
        t0 = time.perf_counter()
        try:
            cleaned = self.cleaner.clean(raw)
            numbers = self.extractor.extract(cleaned)
            value = self.statistic.compute(numbers)
            if self.presenter:
                self.presenter.present(label, value)
            duration_ms = (time.perf_counter() - t0) * 1000
            self._log("INFO", "pipeline_success", label=label, duration_ms=round(duration_ms, 3))
            return value
        except Exception as e:
            duration_ms = (time.perf_counter() - t0) * 1000
            self._log("ERROR", "pipeline_error", label=label, error=repr(e), duration_ms=round(duration_ms, 3))
            raise




#
# --- Usage example ---
#

if __name__ == "__main__":
    configure_logging(logging.INFO)

    pipeline = DataPipeline(
        cleaner=WhitespaceCleaner(),
        extractor=DigitStringToIntExtractor(),
        statistic=MeanStatistic(),      # Can swap for MedianStatistic
        presenter=LoggerPresenter(),    # Or PrintPresenter() / None
    )

    result = pipeline.run([" 12", "abc", " 5", " 20 "], label="Average")
    # Result is still returned; presentation is logged.