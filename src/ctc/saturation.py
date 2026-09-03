"""Canonical bounded coupling functions for CTC v0.1.0."""

from __future__ import annotations

from fractions import Fraction
import math


def _require_finite(name: str, value: float) -> float:
    value = float(value)
    if not math.isfinite(value):
        raise ValueError(f"{name} must be finite")
    return value


def saturation(reference: float, value: float) -> float:
    """Return value / (reference + value) on the positive CTC domain.

    The ratio is first evaluated exactly from the accepted binary64 inputs. If
    nearest rounding would collapse a value strictly above or below the symmetry
    point onto exactly ``0.5``, the result is moved by one ULP to the correct
    side. This preserves the frozen local strict-monotonicity relation around
    ``value == reference`` instead of making an adjacent larger input compare
    equal. Open-boundary results that would round to exactly 0 or 1 remain
    rejected.
    """
    reference = _require_finite("reference", reference)
    value = _require_finite("value", value)
    if reference <= 0.0:
        raise ValueError("reference must be > 0")
    if value <= 0.0:
        raise ValueError("value must be > 0")

    f_reference = Fraction.from_float(reference)
    f_value = Fraction.from_float(value)
    exact = f_value / (f_reference + f_value)
    result = float(exact)

    if not 0.0 < result < 1.0:
        raise ValueError("saturation is not representable strictly inside (0, 1) for these inputs")

    half = Fraction(1, 2)
    if exact > half and result <= 0.5:
        result = math.nextafter(0.5, math.inf)
    elif exact < half and result >= 0.5:
        result = math.nextafter(0.5, 0.0)

    if not 0.0 < result < 1.0:
        raise ValueError("saturation is not representable strictly inside (0, 1) for these inputs")
    return result
