"""Positive-floor telescopic-time recurrence for the frozen CTC v0.1.0 contract."""

from __future__ import annotations

import math


def _finite(name: str, value: float) -> float:
    value = float(value)
    if not math.isfinite(value):
        raise ValueError(f"{name} must be finite")
    return value


def next_interval(*, current: float, floor: float, eta: float, xi: float, exposure: float) -> float:
    """Advance one fixed-width model epoch.

    ``eta`` and ``xi`` are effective per-epoch coefficients for the declared
    model epoch. This function does not rescale them when the epoch width changes.
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
    return floor + (current - floor) * math.exp(-(eta + xi * exposure))


def transformed_outcome(*, current: float, nxt: float, floor: float) -> float:
    """Return the canonical floor-distance log contraction outcome.

    Exact-floor epochs are intentionally rejected because the transformed
    estimand is undefined there.
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
    return -math.log((nxt - floor) / (current - floor))


def compression_ratio(*, current: float, nxt: float) -> float:
    current = _finite("current", current)
    nxt = _finite("nxt", nxt)
    if current <= 0.0 or nxt <= 0.0:
        raise ValueError("intervals must be > 0")
    return nxt / current


def timescale_ratio(*, human: float, ai: float) -> float:
    human = _finite("human", human)
    ai = _finite("ai", ai)
    if human <= 0.0 or ai <= 0.0:
        raise ValueError("intervals must be > 0")
    return human / ai
