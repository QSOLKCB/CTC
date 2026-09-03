"""Algebraic and equilibrium diagnostics for the CTC v0.1.0 reference model."""

from __future__ import annotations

from dataclasses import dataclass
import math

from .saturation import saturation


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

    @property
    def trace(self) -> float:
        return -(self.p + self.q)

    @property
    def determinant(self) -> float:
        return self.p * self.q - self.b * self.c

    @property
    def discriminant(self) -> float:
        return (self.p - self.q) ** 2 + 4.0 * self.b * self.c

    @property
    def stable(self) -> bool:
        return self.b * self.c < self.p * self.q

    @property
    def eigenvalues(self) -> tuple[float, float]:
        """Return the two real eigenvalues without cancelling the smaller root.

        The canonical v0.1 positive-coupling Jacobian has negative trace. We
        compute the root whose sign matches the trace by direct addition, then
        recover the other eigenvalue from the determinant/product identity.
        """
        disc = self.discriminant
        if disc < -1e-14:
            raise ValueError("v0.1 positive-coupling discriminant became negative")
        root = math.sqrt(max(0.0, disc))
        trace = self.trace
        if root == 0.0:
            value = trace / 2.0
            return (value, value)

        far = (trace + math.copysign(root, trace)) / 2.0
        if far == 0.0:
            return ((trace + root) / 2.0, (trace - root) / 2.0)
        near = self.determinant / far

        if trace <= 0.0:
            return (near, far)
        return (far, near)


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
