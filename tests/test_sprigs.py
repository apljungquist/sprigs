from typing import Dict, TypeVar

import pytest

import sprigs


def fib(n):
    if n >= 2:
        return fib(n - 1) + fib(n - 2)
    return 1


@pytest.mark.parametrize(
    "index, expected",
    [(0, 1), (1, 1), (2, 2), (3, 3), (4, 5), (5, 8), (6, 13), (18, 4181), (19, 6765)],
)
@pytest.mark.parametrize("func", [sprigs.fib, fib,], ids=["rs", "py"])
def test_fib(benchmark, func, index, expected):
    assert benchmark(func, index) == expected


T = TypeVar("T")
V = TypeVar("V")


# Reference implementation
# Copied from sprig.dictutils
def invert(mapping: Dict[T, V]) -> Dict[V, T]:
    """Invert dictionary

    Trivial function but good for two reasons:
    * it gives the operation a name, and
    * it catches an edge case that is easily forgotten.
    """
    result: Dict[V, T] = {v: k for (k, v) in mapping.items()}
    if len(result) != len(mapping):
        raise ValueError("Duplicate values in mapping")
    return result


GOOD = [
    ({}, {}),
    ({"a": "alpha", "b": "beta"}, {"alpha": "a", "beta": "b"}),
    ({"a": 0, 0: "a"}, {"a": 0, 0: "a"}),
    ({i: str(i) for i in range(100)}, {str(i): i for i in range(100)}),
]
BAD = [
    ({"a": "x", "b": {}}, TypeError),
    ({"a": "x", "b": "x"}, ValueError),
]


@pytest.mark.parametrize("example", [vs[0] for vs in GOOD + BAD])
@pytest.mark.parametrize("func", [sprigs.invert, invert,], ids=["rs", "py"])
def test_invert_does_not_mutate_imput(func, example):
    expected = example.copy()
    try:
        func(example)
    except Exception:
        pass
    assert example == expected


@pytest.mark.parametrize("example, expected", GOOD)
@pytest.mark.parametrize("func", [sprigs.invert, invert], ids=["rs", "py"])
def test_returns_expected(benchmark, func, example, expected):
    actual = benchmark(func, example)
    assert actual == expected


@pytest.mark.parametrize("before, cls", BAD)
@pytest.mark.parametrize("func", [sprigs.invert, invert], ids=["rs", "py"])
def test_raises_expected(func, before, cls):
    with pytest.raises(cls):
        print(func(before))
