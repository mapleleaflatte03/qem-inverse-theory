"""Tests for spectral and physical constraints."""

import numpy as np
import pytest
from qem_inverse_theory.constraints import (
    spectral_bounds,
    validate_expectation,
    project_to_spectral_bounds,
    project_to_simplex,
    validate_probability_vector,
)


def test_spectral_bounds_pauli():
    eigs = np.array([-1.0, 1.0])
    assert spectral_bounds(eigs) == (-1.0, 1.0)


def test_spectral_bounds_general():
    eigs = np.array([0.0, 0.5, 1.0])
    assert spectral_bounds(eigs) == (0.0, 1.0)


def test_validate_expectation_inside():
    assert validate_expectation(0.5, (-1.0, 1.0))


def test_validate_expectation_outside():
    assert not validate_expectation(1.5, (-1.0, 1.0))


def test_project_stays_inside():
    for val in [-2.0, -1.0, 0.0, 0.5, 1.0, 1.5, 3.0]:
        projected = project_to_spectral_bounds(val, (-1.0, 1.0))
        assert -1.0 <= projected <= 1.0


def test_project_identity_inside():
    assert project_to_spectral_bounds(0.5, (-1.0, 1.0)) == 0.5


def test_simplex_projection_sums_to_one():
    v = np.array([0.3, -0.1, 0.5, 0.8])
    projected = project_to_simplex(v)
    assert abs(projected.sum() - 1.0) < 1e-10


def test_simplex_projection_nonnegative():
    v = np.array([-0.5, 0.2, 0.3, 1.5])
    projected = project_to_simplex(v)
    assert np.all(projected >= -1e-10)


def test_validate_probability_vector_valid():
    v = np.array([0.25, 0.25, 0.25, 0.25])
    assert validate_probability_vector(v)


def test_validate_probability_vector_invalid():
    v = np.array([0.5, 0.5, 0.5])  # sums to 1.5
    assert not validate_probability_vector(v)
