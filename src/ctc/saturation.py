"""Canonical bounded coupling functions for CTC v0.1.0."""

from __future__ import annotations

import math


def _require_finite(name: str, value: float) -> float:
    value = float(value)
    if not math.isfinite(value):
        raise ValueError(f"{name} must be finite")
    return value


def saturation(reference: float, value: float) -> float:
    """Return value / (reference + value) on the positive CTC domain."""
    reference = _require_finite("reference", reference)
    value = _require_finite("value", value)
    if reference <= 0.0:
        raise ValueError("reference must be > 0")
    if value <= 0.0:
        raise ValueError("value must be > 0")
    return value / (reference + value)
