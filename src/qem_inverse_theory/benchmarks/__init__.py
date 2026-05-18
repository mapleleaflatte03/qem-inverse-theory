"""Synthetic benchmarks for ZNE inverse problem research."""

from .synthetic_response import (
    exponential_decay_response,
    polynomial_bias_response,
    mixed_response,
    adversarial_response_with_same_observed_nodes,
)
from .shot_noise import add_gaussian_shot_noise, pauli_variance_from_expectation, allocate_shots_uniform
from .metrics import absolute_error, mse, bias_variance_decomposition, physical_validity_rate, interval_coverage
