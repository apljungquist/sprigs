from random import Random

import pytest

from sprig import intervals, intervals_naive
import sprigs


def _rng(seed):
    if isinstance(seed, Random):
        return seed
    else:
        return Random(seed)


def _rand_intervals(seed, num_interval, min_pitch):
    rng = _rng(seed)
    result = {}
    if num_interval is None:
        num_interval = rng.randrange(1, 10)
    if min_pitch is None:
        min_pitch = 0.5

    left = 0.0
    for i in range(num_interval):
        left += min_pitch + rng.random()
        right = left + rng.random()
        result[i] = (int(100 * left), int(100 * right))
    return result


def _rand_factors(seed, num_factor=None, num_interval=None, min_pitch=None):
    rng = _rng(seed)
    if num_factor is None:
        num_factor = rng.randrange(2, 5)
    return [_rand_intervals(rng, num_interval, min_pitch) for i in range(num_factor)]


EXAMPLES = [
    ([{0: (1, 7)}], {(0,): (1, 7)}),
    ([{0: (1, 7)}, {1: (3, 9)}], {(0, 1): (3, 7)}),
    ([{0: (1, 7)}, {1: (3, 9)}, {2: (0, 2), 3: (0, 4)}], {(0, 1, 3): (3, 4)}),
    # works not only with numbers
    (
        [{"a": ([1, 2], [3, 4])}, {"b": ([2, 3], [4, 5])}],
        {("a", "b"): ([2, 3], [3, 4])},
    ),
] + [
    (factors, intervals.intersecting_products(factors))
    for factors in [
        _rand_factors(1, num_factor=1, num_interval=1),
        _rand_factors(1, num_factor=2, num_interval=1),
        _rand_factors(1, num_factor=2, num_interval=10),
        _rand_factors(1, num_factor=2, num_interval=100),
        _rand_factors(1, num_factor=2, num_interval=1000),
        _rand_factors(1, num_factor=4, num_interval=1000),
    ]
]


# Naive implementation is not even included since it quickly becomes too slow
@pytest.mark.parametrize("i", list(range(len(EXAMPLES))))
@pytest.mark.parametrize(
    "func",
    [sprigs.intersecting_products, intervals.intersecting_products,],
    ids=["rs", "py"],
)
def test_intersecting_products_by_example(benchmark, func, i):
    example = EXAMPLES[i]
    args = example[:-1]
    expected = example[-1]

    assert benchmark(func, *args) == expected
