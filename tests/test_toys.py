import pytest

from sprig import toys
import sprigs


@pytest.mark.parametrize(
    "index, expected",
    [(0, 0), (1, 1), (2, 1), (3, 2), (5, 5), (8, 21), (13, 233), (21, 10_946)],
)
@pytest.mark.parametrize("func", [sprigs.fib, toys.fib], ids=["rs", "py"])
def test_fib(benchmark, func, index, expected):
    assert benchmark(func, index) == expected
