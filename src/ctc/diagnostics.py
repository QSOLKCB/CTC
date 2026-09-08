"""Algebraic and equilibrium diagnostics for the CTC v0.1.0 reference model."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, localcontext
from fractions import Fraction
import math
import sys


def _fraction(value: float) -> Fraction:
    return Fraction.from_float(float(value))


def _fraction_to_float(name: str, value: Fraction) -> float:
    try:
        result = float(value)
    except OverflowError as exc:
        raise ValueError(f"{name} is outside the finite binary64 range") from exc
    if not math.isfinite(result):
        raise ValueError(f"{name} is outside the finite binary64 range")
    if result == 0.0 and value != 0:
        raise ValueError(f"{name} is nonzero but below binary64 resolution")
    return result


def _positive_increment_float(name: str, *, base: float, exact: Fraction) -> float:
    """Convert an exact value known to be >= base without erasing a strict increment."""
    result = _fraction_to_float(name, exact)
    f_base = _fraction(base)
    if exact > f_base and result <= base:
        result = math.nextafter(base, math.inf)
        if not math.isfinite(result):
            raise ValueError(f"{name} has a positive increment outside finite binary64 resolution")
    return result


def _ceil_fraction_float(name: str, value: Fraction) -> float:
    """Return the least available finite float at or above an exact positive value."""
    result = _fraction_to_float(name, value)
    if _fraction(result) < value:
        result = math.nextafter(result, math.inf)
        if not math.isfinite(result):
            raise ValueError(f"{name} is outside the finite binary64 range")
    return result


def _barrier_exact(*, K: float, alpha: float, gamma: float) -> Fraction:
    """Return K*(1+gamma/alpha) exactly from binary64 inputs."""
    return _fraction(K) + _fraction(K) * _fraction(gamma) / _fraction(alpha)


def _barrier(*, K: float, alpha: float, gamma: float, name: str) -> float:
    """Evaluate K*(1+gamma/alpha) without losing a positive coupling increment."""
    return _positive_increment_float(
        name,
        base=K,
        exact=_barrier_exact(K=K, alpha=alpha, gamma=gamma),
    )


def _nullcline_exact(
    *, K: float, alpha: float, gamma: float, reference: float, value: Fraction
) -> Fraction:
    """Return the canonical nullcline value exactly from binary64 parameters."""
    if gamma == 0.0:
        return _fraction(K)
    return _fraction(K) + (
        _fraction(K)
        * _fraction(gamma)
        * value
        / (_fraction(alpha) * (_fraction(reference) + value))
    )


def _nullcline_from_state(
    *, K: float, alpha: float, gamma: float, reference: float, value: float, name: str
) -> float:
    """Evaluate K*(1+(gamma/alpha)*value/(reference+value)) as one exact product.

    All public nullcline inputs are validated against the frozen positive-state,
    positive-scale, nonnegative-coupling domain before any zero-coupling shortcut
    or arithmetic is evaluated. The saturation factor is not materialized as a
    binary64 value first. A strictly positive coupling contribution is also not
    allowed to round back to exactly ``K``; when the exact increment is smaller
    than one ULP, the returned diagnostic is moved to the next finite float above
    ``K`` so the sign of the canonical contribution is preserved.

    This direction-preserving public diagnostic is not itself an equilibrium
    certificate. ``find_interior_equilibrium`` uses the exact rational nullcline
    map separately and only returns a pair that is an exact representable fixed
    point of the canonical equations.
    """
    try:
        K = float(K)
        alpha = float(alpha)
        gamma = float(gamma)
        reference = float(reference)
        value = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{name} inputs must be real-valued") from exc

    for field, candidate in {
        "K": K,
        "alpha": alpha,
        "reference": reference,
        "value": value,
    }.items():
        if not math.isfinite(candidate) or candidate <= 0.0:
            raise ValueError(f"{name} {field} must be finite and > 0")
    if not math.isfinite(gamma) or gamma < 0.0:
        raise ValueError(f"{name} gamma must be finite and >= 0")

    exact = _nullcline_exact(
        K=K,
        alpha=alpha,
        gamma=gamma,
        reference=reference,
        value=_fraction(value),
    )
    if gamma == 0.0:
        return K
    return _positive_increment_float(name, base=K, exact=exact)


@dataclass(frozen=True)
class Equilibrium:
    A: float
    H: float


@dataclass(frozen=True)
class JacobianTerms:
    p: float
    q: float
    b: float
    c: float

    def __post_init__(self) -> None:
        for name in ("p", "q", "b", "c"):
            value = float(getattr(self, name))
            if not math.isfinite(value):
                raise ValueError(f"{name} must be finite")
            object.__setattr__(self, name, value)
        if self.p <= 0.0 or self.q <= 0.0:
            raise ValueError("p and q must be > 0")
        if self.b < 0.0 or self.c < 0.0:
            raise ValueError("b and c must be >= 0")

    @property
    def trace(self) -> float:
        exact = -(_fraction(self.p) + _fraction(self.q))
        return _fraction_to_float("Jacobian trace", exact)

    @property
    def determinant(self) -> float:
        exact = _fraction(self.p) * _fraction(self.q) - _fraction(self.b) * _fraction(self.c)
        return _fraction_to_float("Jacobian determinant", exact)

    @property
    def discriminant(self) -> float:
        exact = (_fraction(self.p) - _fraction(self.q)) ** 2 + 4 * _fraction(self.b) * _fraction(self.c)
        return _fraction_to_float("Jacobian discriminant", exact)

    @property
    def stable(self) -> bool:
        return _fraction(self.b) * _fraction(self.c) < _fraction(self.p) * _fraction(self.q)

    def _eigenvalues_at_precision(self, precision: int) -> tuple[Decimal, Decimal]:
        """Evaluate both complete canonical roots under one Decimal context."""
        with localcontext() as ctx:
            ctx.prec = precision
            p = Decimal.from_float(self.p)
            q = Decimal.from_float(self.q)
            b = Decimal.from_float(self.b)
            c = Decimal.from_float(self.c)
            root = ((p - q) * (p - q) + Decimal(4) * b * c).sqrt()
            near = (-(p + q) + root) / Decimal(2)
            far = (-(p + q) - root) / Decimal(2)
        return near, far

    @property
    def eigenvalues(self) -> tuple[float, float]:
        """Return accurately rounded real eigenvalues from complete roots."""
        if self.b == 0.0 or self.c == 0.0:
            if self.p <= self.q:
                return (-self.p, -self.q)
            return (-self.q, -self.p)

        rounded: list[tuple[float, float]] = []
        for precision in (80, 160):
            near_decimal, far_decimal = self._eigenvalues_at_precision(precision)
            values: list[float] = []
            for name, exact_decimal in (
                ("Jacobian near eigenvalue", near_decimal),
                ("Jacobian far eigenvalue", far_decimal),
            ):
                if not exact_decimal.is_finite():
                    raise ValueError(f"{name} is outside the finite binary64 range")
                try:
                    value = float(exact_decimal)
                except OverflowError as exc:
                    raise ValueError(f"{name} is outside the finite binary64 range") from exc
                if not math.isfinite(value):
                    raise ValueError(f"{name} is outside the finite binary64 range")
                if value == 0.0 and exact_decimal != 0:
                    raise ValueError(f"{name} is nonzero but below binary64 resolution")
                values.append(value)
            rounded.append((values[0], values[1]))

        if rounded[0] != rounded[1]:
            raise ValueError("Jacobian eigenvalue rounding is not numerically resolved")
        return rounded[1]


def upper_barriers(*, K_A: float, K_H: float, alpha_A: float, alpha_H: float,
                   gamma_HA: float, gamma_AH: float) -> tuple[float, float]:
    for name, value in {"K_A": K_A, "K_H": K_H, "alpha_A": alpha_A, "alpha_H": alpha_H}.items():
        if not math.isfinite(value) or value <= 0.0:
            raise ValueError(f"{name} must be finite and > 0")
    for name, value in {"gamma_HA": gamma_HA, "gamma_AH": gamma_AH}.items():
        if not math.isfinite(value) or value < 0.0:
            raise ValueError(f"{name} must be finite and >= 0")
    return (
        _barrier(K=K_A, alpha=alpha_A, gamma=gamma_HA, name="AI upper barrier"),
        _barrier(K=K_H, alpha=alpha_H, gamma=gamma_AH, name="human upper barrier"),
    )


def phi(*, H: float, K_A: float, alpha_A: float, gamma_HA: float, H_0: float) -> float:
    return _nullcline_from_state(
        K=K_A,
        alpha=alpha_A,
        gamma=gamma_HA,
        reference=H_0,
        value=H,
        name="AI nullcline",
    )


def psi(*, A: float, K_H: float, alpha_H: float, gamma_AH: float, A_0: float) -> float:
    return _nullcline_from_state(
        K=K_H,
        alpha=alpha_H,
        gamma=gamma_AH,
        reference=A_0,
        value=A,
        name="human nullcline",
    )


def find_interior_equilibrium(
    *, A_0: float, H_0: float, K_A: float, K_H: float,
    alpha_A: float, alpha_H: float, gamma_HA: float, gamma_AH: float,
    iterations: int = 4096,
) -> Equilibrium:
    """Deterministically find an exact representable interior equilibrium.

    Bisection is driven by the exact rational composition of the two canonical
    nullclines formed from the accepted binary64 parameters. Public ``phi`` and
    ``psi`` values may be direction-preserving rounded diagnostics, so equality
    of those float values is deliberately not used as a fixed-point certificate.

    A candidate is returned only when its AI coordinate is an exact scalar fixed
    point and its exact human nullcline coordinate is itself exactly representable
    in binary64. If the unique equilibrium lies between adjacent floats, or one
    coordinate is not exactly representable, the solver fails closed rather than
    returning a rounded non-equilibrium that could poison Jacobian diagnostics.
    """
    for name, value in {
        "A_0": A_0, "H_0": H_0, "K_A": K_A, "K_H": K_H,
        "alpha_A": alpha_A, "alpha_H": alpha_H,
    }.items():
        if not math.isfinite(value) or value <= 0.0:
            raise ValueError(f"{name} must be finite and > 0")
    for name, value in {"gamma_HA": gamma_HA, "gamma_AH": gamma_AH}.items():
        if not math.isfinite(value) or value < 0.0:
            raise ValueError(f"{name} must be finite and >= 0")
    if not isinstance(iterations, int) or isinstance(iterations, bool):
        raise TypeError("iterations must be an integer")
    if iterations < 1:
        raise ValueError("iterations must be >= 1")

    def H_exact(A: float) -> Fraction:
        return _nullcline_exact(
            K=K_H,
            alpha=alpha_H,
            gamma=gamma_AH,
            reference=A_0,
            value=_fraction(A),
        )

    def F_exact(A: float) -> Fraction:
        return _nullcline_exact(
            K=K_A,
            alpha=alpha_A,
            gamma=gamma_HA,
            reference=H_0,
            value=H_exact(A),
        )

    def residual(A: float) -> Fraction:
        return F_exact(A) - _fraction(A)

    def witness(A: float) -> Equilibrium | None:
        f_A = _fraction(A)
        if F_exact(A) != f_A:
            return None
        exact_H = H_exact(A)
        try:
            H = _fraction_to_float("equilibrium H coordinate", exact_H)
        except ValueError:
            return None
        if _fraction(H) != exact_H:
            return None
        return Equilibrium(A=A, H=H)

    if gamma_HA == 0.0:
        candidate = witness(K_A)
        if candidate is not None:
            return candidate
        raise RuntimeError(
            "canonical equilibrium exists but no exact representable binary64 witness exists"
        )

    lo = K_A
    exact_barrier = _barrier_exact(K=K_A, alpha=alpha_A, gamma=gamma_HA)
    max_float = sys.float_info.max
    if exact_barrier > _fraction(max_float):
        hi = max_float
    else:
        hi = _ceil_fraction_float("AI equilibrium bracket", exact_barrier)

    g_lo = residual(lo)
    g_hi = residual(hi)
    if g_lo < 0 or g_hi > 0:
        raise RuntimeError("equilibrium bracket invariant violated")

    if g_lo == 0:
        candidate = witness(lo)
        if candidate is not None:
            return candidate
        raise RuntimeError(
            "canonical equilibrium exists at the scalar endpoint but no exact representable binary64 witness exists"
        )
    if g_hi == 0:
        candidate = witness(hi)
        if candidate is not None:
            return candidate
        raise RuntimeError(
            "canonical equilibrium exists at the scalar endpoint but no exact representable binary64 witness exists"
        )

    for _ in range(iterations):
        mid = lo + (hi - lo) * 0.5
        if mid == lo or mid == hi:
            for endpoint in (lo, hi):
                candidate = witness(endpoint)
                if candidate is not None:
                    return candidate
            raise RuntimeError(
                "equilibrium exists between adjacent binary64 values but no exact representable fixed-point witness exists"
            )

        g_mid = residual(mid)
        if g_mid == 0:
            candidate = witness(mid)
            if candidate is not None:
                return candidate
            raise RuntimeError(
                "canonical scalar fixed point has no exact representable binary64 equilibrium pair"
            )
        if g_mid > 0:
            lo = mid
        else:
            hi = mid

    raise RuntimeError(
        "equilibrium witness did not resolve to an exact fixed point or adjacent binary64 bracket"
    )


def jacobian_terms(
    *, equilibrium: Equilibrium, A_0: float, H_0: float, K_A: float, K_H: float,
    alpha_A: float, alpha_H: float, gamma_HA: float, gamma_AH: float,
) -> JacobianTerms:
    """Return canonical interior-Jacobian terms without overflowing finite ratios."""
    A = float(equilibrium.A)
    H = float(equilibrium.H)
    for name, value in {
        "A": A, "H": H, "A_0": A_0, "H_0": H_0,
        "K_A": K_A, "K_H": K_H, "alpha_A": alpha_A, "alpha_H": alpha_H,
        "gamma_HA": gamma_HA, "gamma_AH": gamma_AH,
    }.items():
        if not math.isfinite(value):
            raise ValueError(f"{name} must be finite")
    if min(A, H, A_0, H_0, K_A, K_H, alpha_A, alpha_H) <= 0.0:
        raise ValueError("equilibrium, reference, carrying, and intrinsic-growth scales must be > 0")
    if gamma_HA < 0.0 or gamma_AH < 0.0:
        raise ValueError("coupling coefficients must be >= 0")

    fA = _fraction(A)
    fH = _fraction(H)
    fA0 = _fraction(A_0)
    fH0 = _fraction(H_0)
    p = _fraction_to_float("Jacobian p", _fraction(alpha_A) * fA / _fraction(K_A))
    q = _fraction_to_float("Jacobian q", _fraction(alpha_H) * fH / _fraction(K_H))
    b = _fraction_to_float(
        "Jacobian b",
        _fraction(gamma_HA) * fA * fH0 / ((fH0 + fH) ** 2),
    ) if gamma_HA != 0.0 else 0.0
    c = _fraction_to_float(
        "Jacobian c",
        _fraction(gamma_AH) * fH * fA0 / ((fA0 + fA) ** 2),
    ) if gamma_AH != 0.0 else 0.0
    return JacobianTerms(p=p, q=q, b=b, c=c)
