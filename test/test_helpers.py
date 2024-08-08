from __future__ import annotations

from collections import OrderedDict

import pytest
from glue_utils.helpers import UnorderedDictWarning, generate_partitioned_path


class TestHelpers:
    @pytest.mark.parametrize(
        ("partitions", "expected_path"),
        [
            (
                OrderedDict([("year", "2022"), ("month", "01"), ("day", "01")]),
                "year=2022/month=01/day=01",
            ),
            (
                OrderedDict([("category", "electronics"), ("brand", "apple")]),
                "category=electronics/brand=apple",
            ),
        ],
    )
    def test_generate_partitioned_path_with_ordered_dict(
        self,
        partitions,
        expected_path,
    ):
        assert generate_partitioned_path(partitions) == expected_path

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
    def test_generate_partitioned_path_with_regular_dict(
        self,
        partitions,
        expected_path,
    ):
        with pytest.warns(UnorderedDictWarning):
            assert generate_partitioned_path(partitions) == expected_path
