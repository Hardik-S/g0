"""Utility functions for selecting and summing small prime numbers."""

from __future__ import annotations

import random

PRIMES_UNDER_30: tuple[int, ...] = (
    2,
    3,
    5,
    7,
    11,
    13,
    17,
    19,
    23,
    29,
)
"""A tuple containing all prime numbers less than 30."""


def pick_two_primes(random_seed: int | None = None) -> tuple[int, int]:
    """Return a deterministic pair of distinct primes under 30.

    Args:
        random_seed: Optional seed value to initialize the pseudorandom number
            generator. Providing a seed guarantees deterministic output across
            invocations, which is especially useful in unit tests.

    Returns:
        A tuple of two distinct prime numbers.

    Raises:
        ValueError: If the global prime pool is empty or contains fewer than two
            primes, making selection impossible.
    """

    if len(PRIMES_UNDER_30) < 2:
        raise ValueError("At least two primes are required for selection.")

    rng = random.Random(random_seed)
    selection = rng.sample(PRIMES_UNDER_30, k=2)
    return selection[0], selection[1]


def sum_primes(prime_pair: tuple[int, int]) -> int:
    """Return the sum of a pair of prime numbers.

    Args:
        prime_pair: The pair of prime numbers to be summed.

    Returns:
        The arithmetic sum of the provided prime numbers.
    """

    first, second = prime_pair
    return first + second


__all__ = ["PRIMES_UNDER_30", "pick_two_primes", "sum_primes"]
