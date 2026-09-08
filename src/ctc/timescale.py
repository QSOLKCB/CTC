"""Positive-floor telescopic-time recurrence for the frozen CTC v0.1.0 contract."""

from __future__ import annotations

from decimal import Decimal, localcontext
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


def _decimal_from_fraction(value: Fraction) -> Decimal:
    """Convert an exact rational to Decimal under the caller's active context."""
    return Decimal(value.numerator) / Decimal(value.denominator)


def _effective_rate_exact(*, eta: float, cross: Fraction) -> Fraction:
    """Return the exact eta + cross rate formed from accepted binary64 inputs."""
    exact = Fraction.from_float(eta) + cross
    if exact <= 0:
        raise ArithmeticError("positive contraction rate is outside the finite binary64 range")
    return exact


def _effective_rate_from_cross(*, eta: float, cross: Fraction) -> float:
    """Return the rounded rate used only to enforce the accepted-domain ordering contract."""
    exact = _effective_rate_exact(eta=eta, cross=cross)
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


def _interval_from_rate(*, current: float, floor: float, rate: Fraction) -> float:
    """Round the complete canonical floor-centered recurrence from exact inputs.

    ``current`` and ``floor`` are accepted binary64 values and ``rate`` is the
    exact rational effective rate formed from accepted binary64 coefficients.
    The complete expression

        floor + (current - floor) * exp(-rate)

    is evaluated at two Decimal precisions. Both evaluations must round to the
    same binary64 result; otherwise the step fails closed. This avoids premature
    rounding of either the floor distance or the effective rate and subsumes the
    older factor/decrement reconstruction arbitration without a branch boundary.
    """
    if rate <= 0:
        raise ArithmeticError("positive contraction rate is outside the finite binary64 range")

    rounded: list[float] = []
    for precision in (80, 160):
        with localcontext() as ctx:
            ctx.prec = precision
            d_current = Decimal.from_float(current)
            d_floor = Decimal.from_float(floor)
            d_rate = _decimal_from_fraction(rate)
            value = d_floor + (d_current - d_floor) * (-d_rate).exp()
        if not value.is_finite():
            raise ArithmeticError("canonical contraction is outside the finite binary64 range")
        try:
            result = float(value)
        except OverflowError as exc:
            raise ArithmeticError("canonical contraction is outside the finite binary64 range") from exc
        if not math.isfinite(result):
            raise ArithmeticError("canonical contraction is outside the finite binary64 range")
        rounded.append(result)

    if rounded[0] != rounded[1]:
        raise ArithmeticError(
            "canonical contraction rounding is not numerically resolved; increase numerical resolution"
        )
    nxt = rounded[1]
    if nxt <= floor:
        raise ArithmeticError(
            "strict above-floor contraction is not representable in binary64; increase numerical resolution"
        )
    if nxt >= current:
        raise ArithmeticError(
            "strict positive contraction is not representable in binary64; increase numerical resolution"
        )
    return nxt


def _immediate_successor_cross(
    *, eta: float, xi: float, exposure: float, cross: Fraction
) -> Fraction | None:
    """Return the immediate larger exposure cross term or fail on lost ordering.

    The accepted public numerical domain must preserve strict ordering for every
    adjacent binary64 exposure, not merely at the next exposure that reaches a
    different rounded effective-rate level. If the immediate larger exposure has
    a strictly larger exact cross term but the rounded rate does not increase,
    the current input is unresolved and fails closed.
    """
    if xi == 0.0 or exposure >= 1.0:
        return None

    successor = math.nextafter(exposure, math.inf)
    if not math.isfinite(successor) or successor > 1.0:
        return None

    f_xi = Fraction.from_float(xi)
    successor_cross = f_xi * Fraction.from_float(successor)
    if successor_cross <= cross:
        return None

    rate = _effective_rate_from_cross(eta=eta, cross=cross)
    successor_rate = _effective_rate_from_cross(eta=eta, cross=successor_cross)
    if successor_rate <= rate:
        raise ArithmeticError(
            "strict adjacent cross-exposure ordering is below binary64 rate resolution"
        )
    return successor_cross


def _next_interval_from_cross(
    *, current: float, floor: float, eta: float, cross: Fraction,
    successor_cross: Fraction | None = None,
) -> float:
    """Advance with an exact cross-compression contribution."""
    if current == floor:
        return floor

    rate = _effective_rate_from_cross(eta=eta, cross=cross)
    exact_rate = _effective_rate_exact(eta=eta, cross=cross)
    nxt = _interval_from_rate(current=current, floor=floor, rate=exact_rate)
    if cross > 0:
        baseline = _interval_from_rate(
            current=current,
            floor=floor,
            rate=Fraction.from_float(eta),
        )
        if nxt >= baseline:
            raise ArithmeticError(
                "positive cross-exposure compression is below binary64 interval resolution"
            )

    if successor_cross is not None:
        successor_rate = _effective_rate_from_cross(eta=eta, cross=successor_cross)
        if successor_rate <= rate:
            raise ArithmeticError("larger cross exposure does not produce a distinct effective rate")
        successor_nxt = _interval_from_rate(
            current=current,
            floor=floor,
            rate=_effective_rate_exact(eta=eta, cross=successor_cross),
        )
        if successor_nxt >= nxt:
            raise ArithmeticError(
                "strict cross-exposure ordering is below binary64 interval resolution"
            )
    return nxt


def _coupled_cross(*, xi: float, reference: float, value: float) -> Fraction:
    if xi == 0.0:
        return Fraction(0, 1)
    f_xi = Fraction.from_float(xi)
    f_reference = Fraction.from_float(reference)
    f_value = Fraction.from_float(value)
    return f_xi * f_value / (f_reference + f_value)


def _validate_coupled_inputs(
    *, current: float, floor: float, eta: float, xi: float, reference: float, value: float
) -> tuple[float, float, float, float, float, float]:
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
    return current, floor, eta, xi, reference, value


def next_interval(*, current: float, floor: float, eta: float, xi: float, exposure: float) -> float:
    """Advance one fixed-width model epoch with fail-closed strict ordering."""
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
        successor_cross = _immediate_successor_cross(
            eta=eta, xi=xi, exposure=exposure, cross=cross
        )
    return _next_interval_from_cross(
        current=current, floor=floor, eta=eta, cross=cross, successor_cross=successor_cross
    )


def next_interval_coupled(
    *, current: float, floor: float, eta: float, xi: float, reference: float, value: float
) -> float:
    """Advance using exact composite coupling and validate the immediate successor.

    Any strictly larger exact composite exposure must remain ordered. If the
    immediate larger binary64 capability has a larger exact cross term but its
    effective rate rounds to the same binary64 value, the current input fails
    closed. If the rate is distinct, the successor interval must be strictly
    smaller. Thus adjacent accepted capabilities cannot erase coupling order at
    either the rate or interval conversion boundary.
    """
    current, floor, eta, xi, reference, value = _validate_coupled_inputs(
        current=current, floor=floor, eta=eta, xi=xi, reference=reference, value=value
    )
    cross = _coupled_cross(xi=xi, reference=reference, value=value)
    successor_cross = None
    if current != floor and xi > 0.0:
        successor = math.nextafter(value, math.inf)
        if math.isfinite(successor):
            candidate_cross = _coupled_cross(xi=xi, reference=reference, value=successor)
            if candidate_cross > cross:
                rate = _effective_rate_from_cross(eta=eta, cross=cross)
                candidate_rate = _effective_rate_from_cross(eta=eta, cross=candidate_cross)
                if candidate_rate <= rate:
                    raise ArithmeticError(
                        "strict coupled cross-exposure ordering is below binary64 rate resolution"
                    )
                successor_cross = candidate_cross
    return _next_interval_from_cross(
        current=current, floor=floor, eta=eta, cross=cross, successor_cross=successor_cross
    )


def next_interval_coupled_pair(
    *, current: float, floor: float, eta: float, xi: float, reference: float,
    value: float, comparison_value: float,
) -> float:
    """Advance from value and verify ordering against an actual model state."""
    current, floor, eta, xi, reference, value = _validate_coupled_inputs(
        current=current, floor=floor, eta=eta, xi=xi, reference=reference, value=value
    )
    comparison_value = _finite("comparison_value", comparison_value)
    if comparison_value <= 0.0:
        raise ValueError("comparison_value must be > 0")

    cross = _coupled_cross(xi=xi, reference=reference, value=value)
    nxt = _next_interval_from_cross(current=current, floor=floor, eta=eta, cross=cross)
    if current == floor or xi == 0.0 or comparison_value == value:
        return nxt

    comparison_cross = _coupled_cross(xi=xi, reference=reference, value=comparison_value)
    comparison_nxt = _next_interval_from_cross(
        current=current, floor=floor, eta=eta, cross=comparison_cross
    )
    if comparison_value > value and comparison_nxt >= nxt:
        raise ArithmeticError("actual larger capability exposure is below binary64 interval resolution")
    if comparison_value < value and comparison_nxt <= nxt:
        raise ArithmeticError("actual smaller capability exposure is below binary64 interval resolution")
    return nxt


def transformed_outcome(*, current: float, nxt: float, floor: float) -> float:
    """Return the accurately rounded canonical floor-distance log contraction."""
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
    ratio = current_distance / next_distance

    rounded: list[float] = []
    for precision in (80, 160):
        with localcontext() as ctx:
            ctx.prec = precision
            value = _decimal_from_fraction(ratio).ln()
        if not value.is_finite():
            raise ArithmeticError("transformed contraction is outside the finite binary64 range")
        try:
            result = float(value)
        except OverflowError as exc:
            raise ArithmeticError("transformed contraction is outside the finite binary64 range") from exc
        if not math.isfinite(result):
            raise ArithmeticError("transformed contraction is outside the finite binary64 range")
        rounded.append(result)

    if rounded[0] != rounded[1]:
        raise ArithmeticError(
            "transformed contraction rounding is not numerically resolved; increase numerical resolution"
        )
    result = rounded[1]
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
