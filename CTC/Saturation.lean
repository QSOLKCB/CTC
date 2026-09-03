import CTC.Basic

namespace CTC

/-- CTC-MATH-001: the canonical saturation is positive on positive inputs. -/
theorem saturation_pos {x0 x : ℝ} (hx0 : 0 < x0) (hx : 0 < x) :
    0 < saturation x0 x := by
  unfold saturation
  positivity

/-- CTC-MATH-002: the canonical saturation is strictly below one. -/
theorem saturation_lt_one {x0 x : ℝ} (hx0 : 0 < x0) (hx : 0 < x) :
    saturation x0 x < 1 := by
  unfold saturation
  have hden : 0 < x0 + x := by linarith
  rw [div_lt_one hden]
  linarith

/-- Supporting weak upper bound. -/
theorem saturation_le_one {x0 x : ℝ} (hx0 : 0 < x0) (hx : 0 < x) :
    saturation x0 x ≤ 1 :=
  (saturation_lt_one hx0 hx).le

/-- Supporting continuity lemma on the positive domain. -/
theorem saturation_continuousAt_of_pos {x0 x : ℝ} (hx0 : 0 < x0) (hx : 0 < x) :
    ContinuousAt (saturation x0) x := by
  unfold saturation
  exact continuousAt_id.div (continuousAt_const.add continuousAt_id) (by linarith)

/-- CTC-MATH-014: saturation is strictly increasing on positive reals. -/
theorem saturation_strict_mono {x0 : ℝ} (hx0 : 0 < x0) :
    StrictMonoOn (saturation x0) (Set.Ioi (0 : ℝ)) := by
  intro a ha b hb hab
  unfold saturation
  have hda : 0 < x0 + a := by linarith [ha]
  have hdb : 0 < x0 + b := by linarith [hb]
  rw [div_lt_div_iff₀ hda hdb]
  nlinarith

end CTC
