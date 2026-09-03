import CTC.Basic

namespace CTC

/-- CTC-MATH-005: an admissible interval remains at or above its positive floor. -/
theorem telescopic_floor_preserved {Tmin eta xi s T : ℝ}
    (hT : Tmin ≤ T) :
    Tmin ≤ nextT Tmin eta xi s T := by
  unfold nextT
  have hdiff : 0 ≤ T - Tmin := sub_nonneg.mpr hT
  have hexp : 0 ≤ Real.exp (-(eta + xi * s)) := (Real.exp_pos _).le
  nlinarith [mul_nonneg hdiff hexp]

/-- CTC-MATH-006: positive baseline compression strictly decreases an interval above its floor. -/
theorem telescopic_strict_compression {Tmin eta xi s T : ℝ}
    (hT : Tmin < T) (heta : 0 < eta) (hxi : 0 ≤ xi) (hs : 0 ≤ s) :
    nextT Tmin eta xi s T < T := by
  unfold nextT
  have hsum : 0 < eta + xi * s := by
    nlinarith [mul_nonneg hxi hs]
  have hexp0 : 0 < Real.exp (-(eta + xi * s)) := Real.exp_pos _
  have hexp1 : Real.exp (-(eta + xi * s)) < 1 := by
    rw [Real.exp_lt_one_iff]
    linarith
  have hdiff : 0 < T - Tmin := sub_pos.mpr hT
  have hmul : (T - Tmin) * Real.exp (-(eta + xi * s)) < T - Tmin :=
    mul_lt_of_lt_one_right hdiff.le hexp1
  linarith

/-- Supporting one-step contraction bound used by the convergence theorem. -/
theorem telescopic_distance_step_le {Tmin eta xi s T : ℝ}
    (hT : Tmin ≤ T) (hxi : 0 ≤ xi) (hs : 0 ≤ s) :
    nextT Tmin eta xi s T - Tmin ≤
      (T - Tmin) * Real.exp (-eta) := by
  unfold nextT
  have hdiff : 0 ≤ T - Tmin := sub_nonneg.mpr hT
  have hxs : 0 ≤ xi * s := mul_nonneg hxi hs
  have hexp : Real.exp (-(eta + xi * s)) ≤ Real.exp (-eta) := by
    apply Real.exp_le_exp.mpr
    linarith
  nlinarith [mul_le_mul_of_nonneg_left hexp hdiff]

/-- Supporting bound: the distance above the floor decays at least geometrically. -/
theorem telescopic_distance_bound
    (T s : ℕ → ℝ) {Tmin eta xi : ℝ}
    (hT0 : Tmin ≤ T 0) (heta : 0 < eta) (hxi : 0 ≤ xi)
    (hs0 : ∀ n, 0 ≤ s n)
    (hrec : ∀ n, T (n + 1) = nextT Tmin eta xi (s n) (T n)) :
    ∀ n, 0 ≤ T n - Tmin ∧
      T n - Tmin ≤ (T 0 - Tmin) * (Real.exp (-eta)) ^ n := by
  intro n
  induction n with
  | zero =>
      constructor
      · exact sub_nonneg.mpr hT0
      · simp
  | succ n ih =>
      have hTn : Tmin ≤ T n := sub_nonneg.mp ih.1
      have hfloor : Tmin ≤ T (n + 1) := by
        rw [hrec n]
        exact telescopic_floor_preserved hTn
      constructor
      · exact sub_nonneg.mpr hfloor
      · have hstep := telescopic_distance_step_le hTn hxi (hs0 n)
        rw [hrec n] at hstep
        have hr0 : 0 ≤ Real.exp (-eta) := (Real.exp_pos _).le
        have hmul := mul_le_mul_of_nonneg_right ih.2 hr0
        rw [pow_succ]
        calc
          T (n + 1) - Tmin
              ≤ (T n - Tmin) * Real.exp (-eta) := hstep
          _ ≤ ((T 0 - Tmin) * (Real.exp (-eta)) ^ n) * Real.exp (-eta) := hmul
          _ = (T 0 - Tmin) * ((Real.exp (-eta)) ^ n * Real.exp (-eta)) := by ring

/-- CTC-MATH-015: any admissible recurrence trajectory is non-increasing. -/
theorem telescopic_iterate_antitone
    (T s : ℕ → ℝ) {Tmin eta xi : ℝ}
    (hT0 : Tmin ≤ T 0) (heta : 0 < eta) (hxi : 0 ≤ xi)
    (hs0 : ∀ n, 0 ≤ s n)
    (hrec : ∀ n, T (n + 1) = nextT Tmin eta xi (s n) (T n)) :
    Antitone T := by
  have hbound := telescopic_distance_bound T s hT0 heta hxi hs0 hrec
  apply antitone_nat_of_succ_le
  intro n
  have hTn : Tmin ≤ T n := sub_nonneg.mp (hbound n).1
  rcases eq_or_lt_of_le hTn with hEq | hLt
  · rw [hrec n, ← hEq]
    simp [nextT]
  · rw [hrec n]
    exact (telescopic_strict_compression hLt heta hxi (hs0 n)).le

/-- CTC-MATH-007: the recurrence converges to the positive floor. -/
theorem telescopic_converges_to_floor
    (T s : ℕ → ℝ) {Tmin eta xi : ℝ}
    (hT0 : Tmin ≤ T 0) (heta : 0 < eta) (hxi : 0 ≤ xi)
    (hs0 : ∀ n, 0 ≤ s n)
    (hrec : ∀ n, T (n + 1) = nextT Tmin eta xi (s n) (T n)) :
    Tendsto T atTop (𝓝 Tmin) := by
  have hbound := telescopic_distance_bound T s hT0 heta hxi hs0 hrec
  have hr0 : 0 ≤ Real.exp (-eta) := (Real.exp_pos _).le
  have hr1 : Real.exp (-eta) < 1 := by
    rw [Real.exp_lt_one_iff]
    linarith
  have hrT : Tendsto (fun n : ℕ => (Real.exp (-eta)) ^ n) atTop (𝓝 0) :=
    tendsto_pow_atTop_nhds_zero_of_lt_one hr0 hr1
  have huT : Tendsto
      (fun n : ℕ => (T 0 - Tmin) * (Real.exp (-eta)) ^ n) atTop (𝓝 0) := by
    simpa using tendsto_const_nhds.mul hrT
  have hdist : Tendsto (fun n => T n - Tmin) atTop (𝓝 0) :=
    squeeze_zero'
      (Filter.Eventually.of_forall fun n => (hbound n).1)
      (Filter.Eventually.of_forall fun n => (hbound n).2)
      huT
  simpa using hdist.add_const Tmin

end CTC
