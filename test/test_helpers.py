from __future__ import annotations

import pytest
from glue_utils.helpers import generate_partitioned_path


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
    ],
)
def test_generate_partitioned_path(
    partitions,
    expected_path,
) -> None:
    assert generate_partitioned_path(**partitions) == expected_path
