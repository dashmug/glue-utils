"""Module containing small-utility functions that can be useful when working with Glue jobs."""

from __future__ import annotations

from collections import OrderedDict
from warnings import warn


class UnorderedDictWarning(UserWarning):
    """Warning when using a regular dict instead of OrderedDict."""


def generate_partitioned_path(
    partitions: dict[str, str],
    partition_separator: str = "/",
    key_value_separator: str = "=",
) -> str:
    """e.g. Given an ordered dictionary of strings, return a partitioned path."""
    if isinstance(partitions, dict) and not isinstance(partitions, OrderedDict):
        warn(
            "Regular dictionaries are unordered and may not produce the expected path. Use collections.OrderedDict instead.",
            UnorderedDictWarning,
            stacklevel=2,
        )

    return partition_separator.join(
        key_value_separator.join([key, value]) for key, value in partitions.items()
    )
