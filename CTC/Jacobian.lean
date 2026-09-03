import CTC.Basic

namespace CTC

/-- Supporting exact trace identity for the canonical 2x2 Jacobian. -/
theorem jacobian_trace_formula (p q b c : ℝ) :
    (jacobian p q b c).trace = -(p + q) := by
  simp [jacobian, Matrix.trace_fin_two]
  ring

/-- CTC-MATH-010: the canonical Jacobian trace is negative for positive p and q. -/
theorem jacobian_trace_negative {p q b c : ℝ} (hp : 0 < p) (hq : 0 < q) :
    (jacobian p q b c).trace < 0 := by
  rw [jacobian_trace_formula]
  linarith

/-- CTC-MATH-011: determinant formula for the canonical Jacobian. -/
theorem jacobian_det_formula (p q b c : ℝ) :
    (jacobian p q b c).det = p * q - b * c := by
  simp [jacobian, Matrix.det_fin_two]
  ring

/-- CTC-MATH-012: nonnegative mutual coupling forces a nonnegative characteristic discriminant. -/
theorem jacobian_discriminant_nonnegative {p q b c : ℝ}
    (hb : 0 ≤ b) (hc : 0 ≤ c) :
    0 ≤ (p - q) ^ 2 + 4 * b * c := by
  have hsq : 0 ≤ (p - q) ^ 2 := sq_nonneg (p - q)
  have hbc : 0 ≤ b * c := mul_nonneg hb hc
  nlinarith

end CTC
