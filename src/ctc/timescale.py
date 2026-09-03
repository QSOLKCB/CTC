"""Positive-floor telescopic-time recurrence for the frozen CTC v0.1.0 contract."""

from __future__ import annotations

from fractions import Fraction
import math


def _finite(name: str, value: float) -> float:
    value = float(value)
    if not math.isfinite(value):
        raise ValueError(f"{name} must be finite")
    return value


def _positive_ratio(name: str, numerator: float, denominator: float) -> float:
    """Return an exact-input positive ratio or reject binary64 under/overflow."""
    exact = Fraction.from_float(numerator) / Fraction.from_float(denominator)
    try:
        result = float(exact)
    except OverflowError as exc:
        raise ValueError(f"{name} is outside the finite binary64 range") from exc
    if not math.isfinite(result) or result <= 0.0:
        raise ValueError(f"{name} is not representable as a finite positive binary64 value")
    return result


def _positive_fraction_float(name: str, value: Fraction) -> float:
    try:
        result = float(value)
    except OverflowError as exc:
        raise ValueError(f"{name} is outside the finite binary64 range") from exc
    if not math.isfinite(result) or result <= 0.0:
        raise ValueError(f"{name} is not representable as a finite positive binary64 value")
    return result


def _scaled_decay_distance(distance: float, rate: float) -> float:
    """Return distance*exp(-rate) without materializing an underflowed factor."""
    log_remaining = math.log(distance) - rate
    if not math.isfinite(log_remaining):
        raise ArithmeticError(
            "strict above-floor contraction is outside the representable binary64 range"
        )
    remaining = math.exp(log_remaining)
    if not math.isfinite(remaining) or remaining <= 0.0:
        raise ArithmeticError(
            "strict above-floor contraction is not representable in binary64; increase numerical resolution"
        )
    return remaining


def next_interval(*, current: float, floor: float, eta: float, xi: float, exposure: float) -> float:
    """Advance one fixed-width model epoch.

    ``eta`` and ``xi`` are effective per-epoch coefficients for the declared
    model epoch. This function does not rescale them when the epoch width changes.

    The recurrence is evaluated in the numerically stable form nearest the
    current state or the floor. Near zero contraction, ``expm1`` avoids upward
    rounding. For strong contraction, the floor distance and exponential are
    combined in log space so an individually underflowed ``exp(-rate)`` cannot
    erase a representable product. If a mathematically strict contraction cannot
    be represented as a distinct binary64 value, the reference rejects the step
    rather than silently replacing strict compression with a stalled or
    floor-pinned trajectory.
    """
    current = _finite("current", current)
    floor = _finite("floor", floor)
    eta = _finite("eta", eta)
    xi = _finite("xi", xi)
    exposure = _finite("exposure", exposure)
    if floor <= 0.0:
        raise ValueError("floor must be > 0")
    if current < floor:
        raise ValueError("current must be >= floor")
    if eta <= 0.0:
        raise ValueError("eta must be > 0")
    if xi < 0.0:
        raise ValueError("xi must be >= 0")
    if not 0.0 <= exposure <= 1.0:
        raise ValueError("exposure must lie in [0, 1]")
    if current == floor:
        return floor

    distance = current - floor
    rate = eta + xi * exposure
    if not math.isfinite(rate):
        raise ArithmeticError("positive contraction rate is outside the finite binary64 range")

    if rate < math.log(2.0):
        nxt = current + distance * math.expm1(-rate)
    else:
        remaining = _scaled_decay_distance(distance, rate)
        nxt = floor + remaining

    if nxt <= floor:
        raise ArithmeticError(
            "strict above-floor contraction is not representable in binary64; increase numerical resolution"
        )
    if nxt >= current:
        raise ArithmeticError(
            "strict positive contraction is not representable in binary64; increase numerical resolution"
        )
    return nxt


def transformed_outcome(*, current: float, nxt: float, floor: float) -> float:
    """Return the canonical floor-distance log contraction outcome.

    Exact-floor epochs are intentionally rejected because the transformed
    estimand is undefined there. Near zero contraction the result is evaluated as
    ``log1p((current-nxt)/(nxt-floor))`` to avoid cancellation between two nearly
    equal logarithms. For very large contractions, the equivalent difference of
    logs avoids overflow in the relative decrement.
    """
    current = _finite("current", current)
    nxt = _finite("nxt", nxt)
    floor = _finite("floor", floor)
    if floor <= 0.0:
        raise ValueError("floor must be > 0")
    if current <= floor:
        raise ValueError("current must be strictly above floor")
    if not floor < nxt <= current:
        raise ValueError("nxt must satisfy floor < nxt <= current")
    if nxt == current:
        return 0.0

    f_current = Fraction.from_float(current)
    f_nxt = Fraction.from_float(nxt)
    f_floor = Fraction.from_float(floor)
    next_distance = f_nxt - f_floor
    current_distance = f_current - f_floor
    decrement = f_current - f_nxt

    relative = decrement / next_distance
    try:
        relative_float = float(relative)
    except OverflowError:
        relative_float = math.inf

    if math.isfinite(relative_float) and relative_float > 0.0:
        result = math.log1p(relative_float)
    else:
        current_distance_float = _positive_fraction_float("current floor distance", current_distance)
        next_distance_float = _positive_fraction_float("next floor distance", next_distance)
        result = math.log(current_distance_float) - math.log(next_distance_float)

    if result <= 0.0:
        raise ArithmeticError(
            "positive transformed contraction is not representable in binary64; increase numerical resolution"
        )
    return result


def compression_ratio(*, current: float, nxt: float) -> float:
    current = _finite("current", current)
    nxt = _finite("nxt", nxt)
    if current <= 0.0 or nxt <= 0.0:
        raise ValueError("intervals must be > 0")
    return _positive_ratio("compression ratio", nxt, current)


def timescale_ratio(*, human: float, ai: float) -> float:
    human = _finite("human", human)
    ai = _finite("ai", ai)
    if human <= 0.0 or ai <= 0.0:
        raise ValueError("intervals must be > 0")
    return _positive_ratio("timescale ratio", human, ai)
