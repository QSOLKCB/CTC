"""Canonical bounded coupling functions for CTC v0.1.0."""

from __future__ import annotations

from fractions import Fraction
import math


def _require_finite(name: str, value: float) -> float:
    value = float(value)
    if not math.isfinite(value):
        raise ValueError(f"{name} must be finite")
    return value


def _exact_saturation(reference: float, value: float) -> Fraction:
    return Fraction.from_float(value) / (
        Fraction.from_float(reference) + Fraction.from_float(value)
    )


def _rounded_saturation(exact: Fraction) -> float:
    result = float(exact)
    if not 0.0 < result < 1.0:
        raise ValueError("saturation is not representable strictly inside (0, 1) for these inputs")
    return result


def saturation_approx(reference: float, value: float) -> float:
    """Return the nearest binary64 saturation value without an ordering guarantee.

    This helper is used only for descriptive numerical output where the exact
    model dynamics are evaluated through composite expressions before rounding.
    The public ``saturation`` function below is the fail-closed invariant-facing
    API and rejects inputs whose strict ordering cannot be represented.
    """
    reference = _require_finite("reference", reference)
    value = _require_finite("value", value)
    if reference <= 0.0:
        raise ValueError("reference must be > 0")
    if value <= 0.0:
        raise ValueError("value must be > 0")
    return _rounded_saturation(_exact_saturation(reference, value))


def saturation(reference: float, value: float) -> float:
    """Return value/(reference+value) while preserving strict float ordering.

    The canonical ratio is evaluated exactly from the accepted binary64 inputs.
    A binary64 return value is accepted only when the immediately larger finite
    input maps to a strictly larger rounded saturation. If that adjacent exact
    increase would collapse onto the same float, this function rejects the input
    rather than silently violating the frozen strict-monotonicity invariant.

    This successor check is sufficient for the accepted numerical domain: once
    the immediate successor has a larger result, every still-larger input has an
    exact saturation at least as large as that successor and therefore cannot
    compare equal to the accepted result. Open-boundary values remain rejected.
    """
    reference = _require_finite("reference", reference)
    value = _require_finite("value", value)
    if reference <= 0.0:
        raise ValueError("reference must be > 0")
    if value <= 0.0:
        raise ValueError("value must be > 0")

    exact = _exact_saturation(reference, value)
    result = _rounded_saturation(exact)

    successor = math.nextafter(value, math.inf)
    if math.isfinite(successor):
        successor_result = _rounded_saturation(_exact_saturation(reference, successor))
        if successor_result <= result:
            raise ValueError(
                "strict saturation increase is not representable for the next binary64 input"
            )

    return result
