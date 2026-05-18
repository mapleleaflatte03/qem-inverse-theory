"""Common physical bounds for quantum observables."""


def default_pauli_bounds() -> tuple[float, float]:
    """Bounds for single Pauli expectation values."""
    return (-1.0, 1.0)


def observable_bounds(eigenvalues=None) -> tuple[float, float]:
    """Return bounds from eigenvalues, defaulting to Pauli bounds."""
    if eigenvalues is None:
        return default_pauli_bounds()
    from .spectral import spectral_bounds
    return spectral_bounds(eigenvalues)
