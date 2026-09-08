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


def _effective_rate_from_cross(*, eta: float, cross: Fraction) -> float:
    """Form eta + cross exactly and reject a lost positive cross effect."""
    exact = Fraction.from_float(eta) + cross
    try:
        rate = float(exact)
    except OverflowError as exc:
        raise ArithmeticError("positive contraction rate is outside the finite binary64 range") from exc
    if not math.isfinite(rate) or rate <= 0.0:
        raise ArithmeticError("positive contraction rate is outside the finite binary64 range")
    if cross > 0 and rate <= eta:
        raise ArithmeticError(
            "positive cross-exposure compression is below binary64 rate resolution"
        )
    return rate


def _interval_from_rate(*, current: float, floor: float, rate: float) -> float:
    """Evaluate the floor-centered recurrence for one representable positive rate."""
    distance = current - floor
    remaining = _scaled_decay_distance(distance, rate)
    nxt = floor + remaining

    # At extremely small positive rates, log(distance)-rate may round back to
    # log(distance), making the floor-centered reconstruction appear stationary.
    # Use the equivalent decrement form only as a representability fallback.
    if nxt >= current:
        nxt = current + distance * math.expm1(-rate)

    if nxt <= floor:
        raise ArithmeticError(
            "strict above-floor contraction is not representable in binary64; increase numerical resolution"
        )
    if nxt >= current:
        raise ArithmeticError(
            "strict positive contraction is not representable in binary64; increase numerical resolution"
        )
    return nxt


def _successor_cross_for_distinct_rate(
    *, eta: float, xi: float, exposure: float, cross: Fraction
) -> Fraction | None:
    """Find the next attainable exposure whose rounded effective rate is larger.

    Adjacent exposure floats often share one rounded effective rate. Rather than
    rejecting solely for that intermediate collision, locate the first binary64
    exposure at the next rounded-rate boundary. The final interval must then be
    strictly smaller or the current exposure is unresolved and fails closed.
    """
    if xi == 0.0 or exposure >= 1.0:
        return None

    rate = _effective_rate_from_cross(eta=eta, cross=cross)
    next_rate = math.nextafter(rate, math.inf)
    if not math.isfinite(next_rate):
        return None

    f_eta = Fraction.from_float(eta)
    f_xi = Fraction.from_float(xi)
    midpoint = (Fraction.from_float(rate) + Fraction.from_float(next_rate)) / 2
    target_exposure = (midpoint - f_eta) / f_xi

    try:
        candidate = float(target_exposure)
    except OverflowError:
        return None
    if candidate <= exposure:
        candidate = math.nextafter(exposure, math.inf)

    for _ in range(4):
        if not math.isfinite(candidate) or candidate > 1.0:
            return None
        candidate_cross = f_xi * Fraction.from_float(candidate)
        candidate_rate = _effective_rate_from_cross(eta=eta, cross=candidate_cross)
        if candidate_rate > rate:
            return candidate_cross
        candidate = math.nextafter(candidate, math.inf)

    raise ArithmeticError(
        "next distinct cross-exposure rate is not numerically resolvable"
    )


def _successor_coupled_cross_for_distinct_rate(
    *, eta: float, xi: float, reference: float, value: float, cross: Fraction
) -> Fraction | None:
    """Find the next capability value that reaches a larger rounded coupled rate.

    The coupled cross term ``xi*value/(reference+value)`` is strictly increasing
    in positive ``value`` when ``xi > 0``. Invert that exact relation at the next
    rounded-rate boundary so ordering can be checked without walking an
    unbounded number of adjacent binary64 values.
    """
    if xi == 0.0:
        return None

    rate = _effective_rate_from_cross(eta=eta, cross=cross)
    next_rate = math.nextafter(rate, math.inf)
    if not math.isfinite(next_rate):
        return None

    f_eta = Fraction.from_float(eta)
    f_xi = Fraction.from_float(xi)
    f_reference = Fraction.from_float(reference)
    midpoint = (Fraction.from_float(rate) + Fraction.from_float(next_rate)) / 2
    target_cross = midpoint - f_eta
    if target_cross <= cross:
        target_cross = math.nextafter(rate, math.inf)
        target_cross = Fraction.from_float(target_cross) - f_eta
    if target_cross >= f_xi:
        return None

    target_value = target_cross * f_reference / (f_xi - target_cross)
    try:
        candidate = float(target_value)
    except OverflowError:
        return None
    if candidate <= value:
        candidate = math.nextafter(value, math.inf)

    for _ in range(4):
        if not math.isfinite(candidate):
            return None
        f_candidate = Fraction.from_float(candidate)
        candidate_cross = f_xi * f_candidate / (f_reference + f_candidate)
        candidate_rate = _effective_rate_from_cross(eta=eta, cross=candidate_cross)
        if candidate_rate > rate:
            return candidate_cross
        candidate = math.nextafter(candidate, math.inf)

    raise ArithmeticError(
        "next distinct coupled cross-exposure rate is not numerically resolvable"
    )


def _next_interval_from_cross(
    *, current: float, floor: float, eta: float, cross: Fraction,
    successor_cross: Fraction | None = None,
) -> float:
    """Advance with an exact cross-compression contribution.

    The cross contribution must survive rate formation and the final interval
    must reflect stronger compression than the eta-only baseline. When an actual
    larger binary64 exposure can produce the next distinct rounded effective
    rate, its resulting interval must also be strictly smaller. This rejects
    pairwise cross-exposure collisions without inventing trajectory motion.
    """
    if current == floor:
        return floor

    rate = _effective_rate_from_cross(eta=eta, cross=cross)
    nxt = _interval_from_rate(current=current, floor=floor, rate=rate)
    if cross > 0:
        baseline = _interval_from_rate(current=current, floor=floor, rate=eta)
        if nxt >= baseline:
            raise ArithmeticError(
                "positive cross-exposure compression is below binary64 interval resolution"
            )

    if successor_cross is not None:
        successor_rate = _effective_rate_from_cross(eta=eta, cross=successor_cross)
        if successor_rate <= rate:
            raise ArithmeticError(
                "larger cross exposure does not produce a distinct effective rate"
            )
        successor_nxt = _interval_from_rate(
            current=current,
            floor=floor,
            rate=successor_rate,
        )
        if successor_nxt >= nxt:
            raise ArithmeticError(
                "strict cross-exposure ordering is below binary64 interval resolution"
            )
    return nxt


def next_interval(*, current: float, floor: float, eta: float, xi: float, exposure: float) -> float:
    """Advance one fixed-width model epoch.

    ``eta`` and ``xi`` are effective per-epoch coefficients for the declared
    model epoch. This function does not rescale them when the epoch width changes.

    The recurrence uses one floor-centered decay construction across the full
    positive-rate domain so crossing an arbitrary numerical branch threshold
    cannot reverse the ordering of stronger versus weaker compression. The floor
    distance and exponential are combined in log space, preserving representable
    products even when ``exp(-rate)`` itself would underflow. The cross term is
    formed exactly from the accepted binary64 inputs and must remain observable
    in the effective rate, against the eta-only baseline, and against the next
    attainable distinct effective rate; unresolved strict ordering fails closed.
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

    cross = Fraction.from_float(xi) * Fraction.from_float(exposure)
    successor_cross = None
    if current != floor:
        successor_cross = _successor_cross_for_distinct_rate(
            eta=eta,
            xi=xi,
            exposure=exposure,
            cross=cross,
        )
    return _next_interval_from_cross(
        current=current,
        floor=floor,
        eta=eta,
        cross=cross,
        successor_cross=successor_cross,
    )


def next_interval_coupled(
    *, current: float, floor: float, eta: float, xi: float, reference: float, value: float
) -> float:
    """Advance using the exact composite cross term xi*value/(reference+value).

    This path is for model dynamics whose exposure is the canonical saturation.
    It deliberately never materializes that saturation as a standalone binary64
    value before multiplication by ``xi``. Strict ordering is also checked at the
    next attainable capability value that reaches a distinct rounded rate.
    """
    current = _finite("current", current)
    floor = _finite("floor", floor)
    eta = _finite("eta", eta)
    xi = _finite("xi", xi)
    reference = _finite("reference", reference)
    value = _finite("value", value)
    if floor <= 0.0:
        raise ValueError("floor must be > 0")
    if current < floor:
        raise ValueError("current must be >= floor")
    if eta <= 0.0:
        raise ValueError("eta must be > 0")
    if xi < 0.0:
        raise ValueError("xi must be >= 0")
    if reference <= 0.0 or value <= 0.0:
        raise ValueError("reference and value must be > 0")

    if xi == 0.0:
        cross = Fraction(0, 1)
    else:
        f_xi = Fraction.from_float(xi)
        f_reference = Fraction.from_float(reference)
        f_value = Fraction.from_float(value)
        cross = f_xi * f_value / (f_reference + f_value)

    successor_cross = None
    if current != floor and xi > 0.0:
        successor_cross = _successor_coupled_cross_for_distinct_rate(
            eta=eta,
            xi=xi,
            reference=reference,
            value=value,
            cross=cross,
        )
    return _next_interval_from_cross(
        current=current,
        floor=floor,
        eta=eta,
        cross=cross,
        successor_cross=successor_cross,
    )


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