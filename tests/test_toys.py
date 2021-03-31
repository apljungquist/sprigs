import pytest

import sprigs


def fib(n):
    if n > 1:
        return fib(n - 1) + fib(n - 2)
    if n == 1:
        return 1
    if n == 0:
        return 0
    raise ValueError


@pytest.mark.parametrize(
    "index, expected",
    [(0, 0), (1, 1), (2, 1), (3, 2), (5, 5), (8, 21), (13, 233), (21, 10_946)],
)
@pytest.mark.parametrize("func", [sprigs.fib, fib,], ids=["rs", "py"])
def test_fib(benchmark, func, index, expected):
    assert benchmark(func, index) == expected
