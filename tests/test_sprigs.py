from typing import Dict, TypeVar

import pytest

import sprigs


@pytest.mark.parametrize(
    "index, expected", [(0, 1), (1, 1), (2, 2), (3, 3), (4, 5), (5, 8), (6, 13)]
)
def test_fib(index, expected):
    assert sprigs.fib(index) == expected


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
]
BAD = [
    ({"a": "x", "b": {}}, TypeError),
    ({"a": "x", "b": "x"}, ValueError),
]


@pytest.mark.parametrize("example", [good[0] for good in GOOD])
@pytest.mark.parametrize("func", [sprigs.invert, invert])
def test_invert_does_not_mutate_imput(func, example):
    expected = example.copy()
    func(example)
    assert example == expected


@pytest.mark.parametrize("example, expected", GOOD)
@pytest.mark.parametrize("func", [sprigs.invert, invert])
def test_returns_expected(func, example, expected):
    assert func(example) == expected


@pytest.mark.parametrize("before, cls", BAD)
@pytest.mark.parametrize("func", [sprigs.invert, invert])
def test_raises_expected(func, before, cls):
    with pytest.raises(cls):
        func(before)
