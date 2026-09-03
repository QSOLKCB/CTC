"""Algebraic and equilibrium diagnostics for the CTC v0.1.0 reference model."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
import math


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


def _barrier(*, K: float, alpha: float, gamma: float, name: str) -> float:
    """Evaluate K*(1+gamma/alpha) without losing a positive coupling increment."""
    exact = _fraction(K) + _fraction(K) * _fraction(gamma) / _fraction(alpha)
    return _positive_increment_float(name, base=K, exact=exact)


def _nullcline_from_state(
    *, K: float, alpha: float, gamma: float, reference: float, value: float, name: str
) -> float:
    """Evaluate K*(1+(gamma/alpha)*value/(reference+value)) as one exact product.

    The saturation factor is not materialized as a binary64 value first. A
    strictly positive coupling contribution is also not allowed to round back to
    exactly ``K``; when the exact increment is smaller than one ULP, the returned
    diagnostic is moved to the next finite float above ``K`` so the sign of the
    canonical contribution is preserved.
    """
    if gamma == 0.0:
        return float(K)
    exact = _fraction(K) + (
        _fraction(K)
        * _fraction(gamma)
        * _fraction(value)
        / (_fraction(alpha) * (_fraction(reference) + _fraction(value)))
    )
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

    def _half_discriminant_root(self) -> float:
        """Return 0.5*sqrt((p-q)^2 + 4bc) without squaring large values."""
        half_difference = (self.p - self.q) * 0.5
        coupling = math.sqrt(self.b) * math.sqrt(self.c)
        root = math.hypot(half_difference, coupling)
        if not math.isfinite(root):
            raise ValueError("Jacobian spectral radius is outside the finite binary64 range")
        return root

    @property
    def eigenvalues(self) -> tuple[float, float]:
        """Return the two real eigenvalues with scaled, cancellation-resistant arithmetic."""
        if self.b == 0.0 or self.c == 0.0:
            if self.p <= self.q:
                return (-self.p, -self.q)
            return (-self.q, -self.p)

        half_sum = _fraction_to_float(
            "Jacobian half trace magnitude",
            (_fraction(self.p) + _fraction(self.q)) / 2,
        )
        half_root = self._half_discriminant_root()
        far = -half_sum - half_root
        if not math.isfinite(far):
            raise ValueError("Jacobian eigenvalue is outside the finite binary64 range")
        if far == 0.0:
            raise ValueError("canonical positive-p,q Jacobian produced an unrepresentable far eigenvalue")

        exact_det = _fraction(self.p) * _fraction(self.q) - _fraction(self.b) * _fraction(self.c)
        near = _fraction_to_float("Jacobian near eigenvalue", exact_det / _fraction(far))
        return (near, far)


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
    """Deterministically find one representably resolved interior equilibrium.

    The proof supplies a scalar bracket. Numerically, a fixed small bisection
    count is unsafe when that bracket spans many orders of magnitude, so the
    routine continues until it finds an exact fixed point or there is no
    representable binary64 midpoint left. ``iterations`` is a hard safety cap;
    an unresolved bracket is rejected rather than returned as a witness.
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

    def H_of(A: float) -> float:
        return psi(A=A, K_H=K_H, alpha_H=alpha_H, gamma_AH=gamma_AH, A_0=A_0)

    def F(A: float) -> float:
        return phi(H=H_of(A), K_A=K_A, alpha_A=alpha_A, gamma_HA=gamma_HA, H_0=H_0)

    if gamma_HA == 0.0:
        A_star = K_A
        return Equilibrium(A=A_star, H=H_of(A_star))

    lo = K_A
    hi = _barrier(K=K_A, alpha=alpha_A, gamma=gamma_HA, name="AI equilibrium bracket")
    g_lo = F(lo) - lo
    g_hi = F(hi) - hi
    if g_lo < 0.0 or g_hi > 0.0:
        raise RuntimeError("equilibrium bracket invariant violated")
    if g_lo == 0.0:
        return Equilibrium(A=lo, H=H_of(lo))
    if g_hi == 0.0:
        return Equilibrium(A=hi, H=H_of(hi))

    for _ in range(iterations):
        mid = lo + (hi - lo) * 0.5
        if mid == lo or mid == hi:
            if F(lo) == lo:
                return Equilibrium(A=lo, H=H_of(lo))
            if F(hi) == hi:
                return Equilibrium(A=hi, H=H_of(hi))
            raise RuntimeError(
                "equilibrium exists between adjacent binary64 values but no representable fixed-point witness exists"
            )

        g_mid = F(mid) - mid
        if g_mid == 0.0:
            return Equilibrium(A=mid, H=H_of(mid))
        if g_mid > 0.0:
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
