from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from glue_utils.helpers import batched, generate_partitioned_path

if TYPE_CHECKING:
    from collections.abc import Generator


@pytest.mark.parametrize(
    ("partitions", "expected_path"),
    [
        (
            {"year": "2022", "month": "01", "day": "01"},
            "year=2022/month=01/day=01",
        ),
        (
            {"category": "electronics", "brand": "apple"},
            "category=electronics/brand=apple",
        ),
        (
            {"brand": "apple", "category": "electronics"},
            "brand=apple/category=electronics",
        ),
    ],
)
def test_generate_partitioned_path(
    partitions,
    expected_path,
) -> None:
    assert generate_partitioned_path(**partitions) == expected_path


class TestBatched:
    @pytest.mark.parametrize(
        ("iterable", "n", "expected"),
        [
            (
                [1, 2, 3, 4, 5, 6, 7, 8, 9],
                3,
                [(1, 2, 3), (4, 5, 6), (7, 8, 9)],
            ),
            (
                [],
                3,
                [],
            ),
            (
                [1, 2, 3],
                5,
                [(1, 2, 3)],
            ),
            (
                [1, 2, 3],
                1,
                [(1,), (2,), (3,)],
            ),
        ],
    )
    def test_batched(self, iterable, n, expected):
        assert list(batched(iterable, n)) == expected

    def test_batched_with_generator(self):
        def gen() -> Generator[int, None, None]:
            yield from range(5)

        iterable = gen()
        n = 2
        expected = [(0, 1), (2, 3), (4,)]
        assert list(batched(iterable, n)) == expected

    def test_batched_with_invalid_n(self):
        with pytest.raises(ValueError):  # noqa: PT011
            list(batched([1, 2, 3], 0))
