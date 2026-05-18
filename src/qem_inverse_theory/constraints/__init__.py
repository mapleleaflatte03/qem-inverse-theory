"""Physical admissibility constraints for quantum observables."""

from .spectral import spectral_bounds, validate_expectation, project_to_spectral_bounds
from .probability_simplex import project_to_simplex, validate_probability_vector
from .physical_bounds import default_pauli_bounds, observable_bounds
