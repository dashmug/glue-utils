"""Module containing small-utility functions that can be useful when working with Glue jobs."""

from __future__ import annotations

from itertools import islice
from typing import TYPE_CHECKING, Any, TypeVar

if TYPE_CHECKING:
    from collections.abc import Iterable


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


T = TypeVar("T")


def batched(iterable: Iterable[T], n: int) -> Iterable[tuple[T, ...]]:
    """Yield successive n-sized chunks from an iterable.

    Note: This is a simple port of itertools.batched() from Python 3.12.
    https://docs.python.org/3/library/itertools.html#itertools.batched

    Parameters
    ----------
    iterable : Iterable[T]
        The iterable to be batched.
    n : int
        The number of items per batch. Must be at least 1.

    Yields
    ------
    Iterable[tuple[T, ...]]
        An iterable of tuples, each containing up to n items from the input iterable.

    Raises
    ------
    ValueError
        If n is less than 1.

    """
    if n < 1:
        msg = "n must be at least one"
        raise ValueError(msg)
    iterator = iter(iterable)
    while batch := tuple(islice(iterator, n)):
        yield batch
