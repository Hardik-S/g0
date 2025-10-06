"""Tests for the prime selection utilities."""

from __future__ import annotations

import pytest

from contribution_adder import primes


def test_pick_two_primes_is_deterministic_with_seed() -> None:
    """Repeated calls with the same seed should return the same ordered pair."""

    first_selection = primes.pick_two_primes(random_seed=42)
    second_selection = primes.pick_two_primes(random_seed=42)

    assert first_selection == second_selection
    assert all(prime in primes.PRIMES_UNDER_30 for prime in first_selection)
    assert first_selection[0] != first_selection[1]


def test_sum_primes_adds_numbers() -> None:
    """The helper should sum the pair element-wise."""

    assert primes.sum_primes((3, 11)) == 14


def test_pick_two_primes_raises_when_pool_insufficient(monkeypatch: pytest.MonkeyPatch) -> None:
    """Sampling should fail when the available prime pool is too small."""

    monkeypatch.setattr(primes, "PRIMES_UNDER_30", ())

    with pytest.raises(ValueError):
        primes.pick_two_primes()
