import CTC.Basic

namespace CTC

/-- CTC-MATH-008: queue-load ratio at or below one is equivalent to demand not exceeding service. -/
theorem verification_load_iff {lambda mu A H : ℝ}
    (hmu : 0 < mu) (hH : 0 < H) :
    lambda * A ≤ mu * H ↔ verificationLoad lambda mu A H ≤ 1 := by
  unfold verificationLoad
  have hden : 0 < mu * H := mul_pos hmu hH
  rw [div_le_iff₀ hden]
  simp

/-- Supporting non-negativity property of the backlog clamp. -/
theorem backlogNext_nonneg (lambda mu A H B : ℝ) :
    0 ≤ backlogNext lambda mu A H B := by
  unfold backlogNext
  exact le_max_left _ _

/-- CTC-MATH-009: subcritical verification load cannot increase a nonnegative backlog. -/
theorem verification_backlog_nonincreasing {lambda mu A H B : ℝ}
    (hmu : 0 < mu) (hH : 0 < H) (hB : 0 ≤ B)
    (hload : verificationLoad lambda mu A H ≤ 1) :
    backlogNext lambda mu A H B ≤ B := by
  have hdemand : lambda * A ≤ mu * H :=
    (verification_load_iff hmu hH).mpr hload
  unfold backlogNext
  rw [max_le_iff]
  constructor
  · exact hB
  · linarith

/-- Supporting strict-overload property. -/
theorem verification_backlog_strict_increase {lambda mu A H B : ℝ}
    (hmu : 0 < mu) (hH : 0 < H)
    (hload : 1 < verificationLoad lambda mu A H) :
    B < backlogNext lambda mu A H B := by
  unfold verificationLoad at hload
  have hden : 0 < mu * H := mul_pos hmu hH
  have hdemand : mu * H < lambda * A := by
    rw [one_lt_div hden] at hload
    simpa [mul_comm] using hload
  unfold backlogNext
  have hraw : B < B + lambda * A - mu * H := by linarith
  exact lt_of_lt_of_le hraw (le_max_right _ _)

end CTC
