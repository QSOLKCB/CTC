"""Canonical bounded coupling functions for CTC v0.1.0."""

from __future__ import annotations

import math


def _require_finite(name: str, value: float) -> float:
    value = float(value)
    if not math.isfinite(value):
        raise ValueError(f"{name} must be finite")
    return value


def saturation(reference: float, value: float) -> float:
    """Return value / (reference + value) on the positive CTC domain.

    The algebra is evaluated in a ratio form that cannot overflow the
    denominator when both positive inputs are individually finite. If the true
    mathematical result is so close to an open boundary that binary64 rounds it
    to exactly 0 or 1, the input range is rejected rather than silently
    violating the frozen ``0 < S < 1`` contract.
    """
    reference = _require_finite("reference", reference)
    value = _require_finite("value", value)
    if reference <= 0.0:
        raise ValueError("reference must be > 0")
    if value <= 0.0:
        raise ValueError("value must be > 0")

    if value >= reference:
        result = 1.0 / (1.0 + reference / value)
    else:
        ratio = value / reference
        result = ratio / (1.0 + ratio)

    if not 0.0 < result < 1.0:
        raise ValueError("saturation is not representable strictly inside (0, 1) for these inputs")
    return result
