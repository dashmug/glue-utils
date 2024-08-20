"""Module containing small-utility functions that can be useful when working with Glue jobs."""

from __future__ import annotations

from typing import Any


def generate_partitioned_path(**kwargs: Any) -> str:  # noqa: ANN401
    """Generate a partitioned path by joining key-value pairs with separators.

    Parameters
    ----------
    **kwargs : Any
        Key-value pairs representing the partitions.

    Returns
    -------
    str
        The generated partitioned path.

    Examples
    --------
    >>> generate_partitioned_path(year=2022, month=10, day=15)
    'year=2022/month=10/day=15'
    >>> generate_partitioned_path(category='electronics', brand='apple')
    'category=electronics/brand=apple'

    """
    return "/".join(f"{key}={value}" for key, value in kwargs.items())
