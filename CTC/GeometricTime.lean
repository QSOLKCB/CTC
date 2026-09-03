import CTC.Basic

namespace CTC

/-- CTC-MATH-003: geometric compression has the standard finite accumulated time. -/
theorem geometric_compression_hasSum {T0 kappa : ℝ}
    (hT0 : 0 < T0) (hkappa : 0 < kappa) (hkappa1 : kappa < 1) :
    HasSum (fun n : ℕ => T0 * kappa ^ n) (T0 / (1 - kappa)) := by
  have hnorm : ‖kappa‖ < 1 := by
    rw [Real.norm_eq_abs, abs_of_pos hkappa]
    exact hkappa1
  simpa [div_eq_mul_inv] using
    (hasSum_geometric_of_norm_lt_one hnorm).mul_left T0

/-- CTC-MATH-004: a positive floor prevents finite-time accumulation. -/
theorem positive_floor_not_summable (T0 kappa Tmin : ℝ) (hTmin : 0 < Tmin) :
    ¬ Summable (fun n : ℕ => max (T0 * kappa ^ n) Tmin) := by
  intro hsum
  have hconst : Summable (fun _ : ℕ => Tmin) :=
    Summable.of_nonneg_of_le
      (fun _ => le_of_lt hTmin)
      (fun n => le_max_right (T0 * kappa ^ n) Tmin)
      hsum
  have hzero : Tendsto (fun _ : ℕ => Tmin) atTop (𝓝 0) := hconst.tendsto_atTop_zero
  have hself : Tendsto (fun _ : ℕ => Tmin) atTop (𝓝 Tmin) := tendsto_const_nhds
  have : Tmin = 0 := tendsto_nhds_unique hself hzero
  exact (ne_of_gt hTmin) this

end CTC
