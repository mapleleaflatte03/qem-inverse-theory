"""Tests for shot noise utilities."""

import numpy as np
import pytest
from qem_inverse_theory.benchmarks.shot_noise import (
    pauli_variance_from_expectation,
    add_gaussian_shot_noise,
    allocate_shots_uniform,
)


def test_pauli_variance_at_zero():
    """Var(O) = 1 - 0² = 1 for <O> = 0."""
    assert pauli_variance_from_expectation(0.0) == 1.0


def test_pauli_variance_at_one():
    """Var(O) = 1 - 1² = 0 for <O> = 1."""
    assert pauli_variance_from_expectation(1.0) == 0.0


def test_shot_noise_reduces_with_shots():
    """More shots → less noise variance."""
    rng = np.random.default_rng(42)
    values = np.array([0.5, 0.5, 0.5, 0.5, 0.5])
    noisy_low = add_gaussian_shot_noise(values, shots=10, rng=np.random.default_rng(0))
    noisy_high = add_gaussian_shot_noise(values, shots=10000, rng=np.random.default_rng(0))
    # High shots should be closer to true values
    assert np.std(noisy_high - values) < np.std(noisy_low - values)


def test_allocate_shots_uniform_sums():
    total = 1000
    n = 7
    alloc = allocate_shots_uniform(total, n)
    assert alloc.sum() == total
    assert len(alloc) == n
    assert np.all(alloc > 0)
