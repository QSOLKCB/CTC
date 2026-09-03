"""Verification-load and backlog recurrence for CTC v0.1.0."""

from __future__ import annotations

from fractions import Fraction
import math


def _positive(name: str, value: float) -> float:
    value = float(value)
    if not math.isfinite(value) or value <= 0.0:
        raise ValueError(f"{name} must be finite and > 0")
    return value


def _fraction(value: float) -> Fraction:
    return Fraction.from_float(value)


def _finite_positive_float(name: str, value: Fraction) -> float:
    try:
        result = float(value)
    except OverflowError as exc:
        raise ValueError(f"{name} is outside the finite binary64 range") from exc
    if not math.isfinite(result) or result <= 0.0:
        raise ValueError(f"{name} is not representable as a finite positive binary64 value")
    return result


def load_ratio(*, lambda_a: float, mu_h: float, A: float, H: float) -> float:
    """Return Xi=(lambda_a*A)/(mu_h*H) without losing the critical-load ordering.

    Products are formed exactly from the accepted binary64 inputs. If the exact
    ratio lies strictly above or below one but rounds to ``1.0``, return the
    nearest representable float on the correct side of one so ``Xi <= 1`` agrees
    with the exact backlog demand/service ordering.
    """
    lambda_a = _positive("lambda_a", lambda_a)
    mu_h = _positive("mu_h", mu_h)
    A = _positive("A", A)
    H = _positive("H", H)

    exact = (_fraction(lambda_a) * _fraction(A)) / (_fraction(mu_h) * _fraction(H))
    result = _finite_positive_float("verification load ratio", exact)
    if result == 1.0:
        if exact > 1:
            return math.nextafter(1.0, math.inf)
        if exact < 1:
            return math.nextafter(1.0, 0.0)
    return result


def backlog_next(*, B: float, lambda_a: float, mu_h: float, A: float, H: float) -> float:
    """Advance the canonical backlog recurrence with exact binary64 arithmetic inputs.

    Products and their difference are formed exactly so large, mutually
    cancelling demand/service terms cannot become ``inf - inf``. If the exact
    recurrence changes a positive backlog but conversion would round back to the
    previous binary64 value, the nearest representable float in the exact
    direction is returned. If no finite positive float exists in that direction,
    the update is rejected rather than silently erasing the movement.
    """
    B = float(B)
    if not math.isfinite(B) or B < 0.0:
        raise ValueError("B must be finite and >= 0")
    lambda_a = _positive("lambda_a", lambda_a)
    mu_h = _positive("mu_h", mu_h)
    A = _positive("A", A)
    H = _positive("H", H)

    baseline = _fraction(B)
    exact = baseline + _fraction(lambda_a) * _fraction(A) - _fraction(mu_h) * _fraction(H)
    if exact <= 0:
        return 0.0

    result = _finite_positive_float("verification backlog", exact)
    if exact > baseline and result <= B:
        directed = math.nextafter(B, math.inf)
        if not math.isfinite(directed) or directed <= B:
            raise ValueError("positive verification-backlog increase is not representable in binary64")
        return directed
    if exact < baseline and result >= B:
        directed = math.nextafter(B, 0.0)
        if directed <= 0.0:
            raise ValueError("positive verification-backlog decrease is not representable in binary64")
        return directed
    return result
