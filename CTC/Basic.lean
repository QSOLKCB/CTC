import Mathlib

namespace CTC

/-- Canonical bounded coupling function from the frozen v0.1.0 contract. -/
def saturation (x0 x : ℝ) : ℝ := x / (x0 + x)

/-- One fixed-width model-epoch update of a telescopic transition interval. -/
def nextT (Tmin eta xi s T : ℝ) : ℝ :=
  Tmin + (T - Tmin) * Real.exp (-(eta + xi * s))

/-- Dimensionless verification load ratio. -/
def verificationLoad (lambda mu A H : ℝ) : ℝ :=
  lambda * A / (mu * H)

/-- One verification-backlog update. -/
def backlogNext (lambda mu A H B : ℝ) : ℝ :=
  max 0 (B + lambda * A - mu * H)

/-- The v0.1.0 two-state Jacobian at an interior equilibrium. -/
def jacobian (p q b c : ℝ) : Matrix (Fin 2) (Fin 2) ℝ :=
  !![-p, b; c, -q]

/-- AI nullcline map. -/
def phi (K alpha gamma H0 H : ℝ) : ℝ :=
  K * (1 + (gamma / alpha) * saturation H0 H)

/-- Human nullcline map. -/
def psi (K alpha gamma A0 A : ℝ) : ℝ :=
  K * (1 + (gamma / alpha) * saturation A0 A)

end CTC
