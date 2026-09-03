"""Algebraic and equilibrium diagnostics for the CTC v0.1.0 reference model."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
import math

from .saturation import saturation


def _fraction(value: float) -> Fraction:
    return Fraction.from_float(value)


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
        """Return the two real eigenvalues with scaled, cancellation-resistant arithmetic.

        The half-discriminant root is computed with ``hypot`` instead of first
        forming ``(p-q)^2``. The more negative root is formed directly; the
        other root is recovered from the exact determinant/product identity.
        This lets finite roots remain available even when the discriminant itself
        is too large to represent as a binary64 number.
        """
        half_sum = self.p * 0.5 + self.q * 0.5
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
        K_A * (1.0 + gamma_HA / alpha_A),
        K_H * (1.0 + gamma_AH / alpha_H),
    )


def phi(*, H: float, K_A: float, alpha_A: float, gamma_HA: float, H_0: float) -> float:
    return K_A * (1.0 + (gamma_HA / alpha_A) * saturation(H_0, H))


def psi(*, A: float, K_H: float, alpha_H: float, gamma_AH: float, A_0: float) -> float:
    return K_H * (1.0 + (gamma_AH / alpha_H) * saturation(A_0, A))


def find_interior_equilibrium(
    *, A_0: float, H_0: float, K_A: float, K_H: float,
    alpha_A: float, alpha_H: float, gamma_HA: float, gamma_AH: float,
    iterations: int = 96,
) -> Equilibrium:
    """Deterministically find one interior equilibrium by the proof's scalar bracket.

    This is a numerical witness for testing and diagnostics, not a substitute for
    the Lean existence theorem.
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
    hi = K_A * (1.0 + gamma_HA / alpha_A)
    g_lo = F(lo) - lo
    g_hi = F(hi) - hi
    if g_lo < -1e-12 or g_hi > 1e-12:
        raise RuntimeError("equilibrium bracket invariant violated")

    for _ in range(iterations):
        mid = (lo + hi) / 2.0
        g_mid = F(mid) - mid
        if g_mid >= 0.0:
            lo = mid
        else:
            hi = mid

    A_star = (lo + hi) / 2.0
    return Equilibrium(A=A_star, H=H_of(A_star))


def jacobian_terms(
    *, equilibrium: Equilibrium, A_0: float, H_0: float, K_A: float, K_H: float,
    alpha_A: float, alpha_H: float, gamma_HA: float, gamma_AH: float,
) -> JacobianTerms:
    A = equilibrium.A
    H = equilibrium.H
    p = alpha_A * A / K_A
    q = alpha_H * H / K_H
    b = gamma_HA * A * H_0 / (H_0 + H) ** 2
    c = gamma_AH * H * A_0 / (A_0 + A) ** 2
    return JacobianTerms(p=p, q=q, b=b, c=c)
