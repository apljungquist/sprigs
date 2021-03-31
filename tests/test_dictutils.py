import pytest

import sprigs
from sprig import dictutils

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
@pytest.mark.parametrize("func", [sprigs.invert, dictutils.invert], ids=["rs", "py"])
def test_invert_does_not_mutate_imput(func, example):
    expected = example.copy()
    try:
        func(example)
    except Exception:
        pass
    assert example == expected


@pytest.mark.parametrize("example, expected", GOOD)
@pytest.mark.parametrize("func", [sprigs.invert, dictutils.invert], ids=["rs", "py"])
def test_returns_expected(benchmark, func, example, expected):
    actual = benchmark(func, example)
    assert actual == expected


@pytest.mark.parametrize("before, cls", BAD)
@pytest.mark.parametrize("func", [sprigs.invert, dictutils.invert], ids=["rs", "py"])
def test_raises_expected(func, before, cls):
    with pytest.raises(cls):
        print(func(before))
