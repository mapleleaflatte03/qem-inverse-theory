"""Core data types for ZNE inverse problem analysis."""

from dataclasses import dataclass, field
from typing import Any, Protocol, runtime_checkable

import numpy as np
from numpy.typing import NDArray


@dataclass
class ZNEData:
    """Observed ZNE data: scale factors, noisy estimates, and metadata."""

    scales: NDArray[np.float64]
    estimates: NDArray[np.float64]
    variances: NDArray[np.float64] | None = None
    shots: NDArray[np.int64] | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        self.scales = np.asarray(self.scales, dtype=np.float64)
        self.estimates = np.asarray(self.estimates, dtype=np.float64)
        if self.variances is not None:
            self.variances = np.asarray(self.variances, dtype=np.float64)
        if self.shots is not None:
            self.shots = np.asarray(self.shots, dtype=np.int64)

    @property
    def n(self) -> int:
        return len(self.scales)


@dataclass
class FitResult:
    """Result of a ZNE estimation procedure."""

    estimate: float
    variance: float | None = None
    method: str = ""
    diagnostics: dict[str, Any] = field(default_factory=dict)
    assumptions: list[str] = field(default_factory=list)


@runtime_checkable
class Estimator(Protocol):
    """Protocol for ZNE estimators."""

    def fit(self, data: ZNEData) -> FitResult: ...
