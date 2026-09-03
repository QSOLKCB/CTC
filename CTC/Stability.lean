import CTC.Jacobian

namespace CTC

/-- CTC-MATH-013: positive determinant is exactly the frozen local-stability inequality. -/
theorem local_stability_inequality (p q b c : ℝ) :
    0 < (jacobian p q b c).det ↔ b * c < p * q := by
  rw [jacobian_det_formula]
  constructor <;> intro h <;> linarith

end CTC
