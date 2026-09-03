import CTC.Saturation

namespace CTC

private theorem phi_pos {K alpha gamma H0 H : ℝ}
    (hK : 0 < K) (halpha : 0 < alpha) (hgamma : 0 ≤ gamma)
    (hH0 : 0 < H0) (hH : 0 < H) :
    0 < phi K alpha gamma H0 H := by
  unfold phi
  have hs : 0 ≤ saturation H0 H := (saturation_pos hH0 hH).le
  have hr : 0 ≤ gamma / alpha := div_nonneg hgamma halpha.le
  have hi : 0 < 1 + (gamma / alpha) * saturation H0 H := by
    nlinarith [mul_nonneg hr hs]
  exact mul_pos hK hi

private theorem psi_pos {K alpha gamma A0 A : ℝ}
    (hK : 0 < K) (halpha : 0 < alpha) (hgamma : 0 ≤ gamma)
    (hA0 : 0 < A0) (hA : 0 < A) :
    0 < psi K alpha gamma A0 A := by
  unfold psi
  have hs : 0 ≤ saturation A0 A := (saturation_pos hA0 hA).le
  have hr : 0 ≤ gamma / alpha := div_nonneg hgamma halpha.le
  have hi : 0 < 1 + (gamma / alpha) * saturation A0 A := by
    nlinarith [mul_nonneg hr hs]
  exact mul_pos hK hi

private theorem phi_lower {K alpha gamma H0 H : ℝ}
    (hK : 0 < K) (halpha : 0 < alpha) (hgamma : 0 ≤ gamma)
    (hH0 : 0 < H0) (hH : 0 < H) :
    K ≤ phi K alpha gamma H0 H := by
  unfold phi
  have hs : 0 ≤ saturation H0 H := (saturation_pos hH0 hH).le
  have hr : 0 ≤ gamma / alpha := div_nonneg hgamma halpha.le
  have hi : 1 ≤ 1 + (gamma / alpha) * saturation H0 H := by
    nlinarith [mul_nonneg hr hs]
  simpa using mul_le_mul_of_nonneg_left hi hK.le

private theorem phi_le_bar {K alpha gamma H0 H : ℝ}
    (hK : 0 < K) (halpha : 0 < alpha) (hgamma : 0 ≤ gamma)
    (hH0 : 0 < H0) (hH : 0 < H) :
    phi K alpha gamma H0 H ≤ K * (1 + gamma / alpha) := by
  unfold phi
  have hs := saturation_le_one hH0 hH
  have hr : 0 ≤ gamma / alpha := div_nonneg hgamma halpha.le
  have hm : (gamma / alpha) * saturation H0 H ≤ gamma / alpha := by
    simpa using mul_le_mul_of_nonneg_left hs hr
  exact mul_le_mul_of_nonneg_left (by linarith) hK.le

private theorem phi_lt_bar {K alpha gamma H0 H : ℝ}
    (hK : 0 < K) (halpha : 0 < alpha) (hgamma : 0 < gamma)
    (hH0 : 0 < H0) (hH : 0 < H) :
    phi K alpha gamma H0 H < K * (1 + gamma / alpha) := by
  unfold phi
  have hs := saturation_lt_one hH0 hH
  have hr : 0 < gamma / alpha := div_pos hgamma halpha
  have hm : (gamma / alpha) * saturation H0 H < gamma / alpha := by
    simpa using mul_lt_mul_of_pos_left hs hr
  exact mul_lt_mul_of_pos_left (by linarith) hK

private theorem psi_lower {K alpha gamma A0 A : ℝ}
    (hK : 0 < K) (halpha : 0 < alpha) (hgamma : 0 ≤ gamma)
    (hA0 : 0 < A0) (hA : 0 < A) :
    K ≤ psi K alpha gamma A0 A := by
  unfold psi
  have hs : 0 ≤ saturation A0 A := (saturation_pos hA0 hA).le
  have hr : 0 ≤ gamma / alpha := div_nonneg hgamma halpha.le
  have hi : 1 ≤ 1 + (gamma / alpha) * saturation A0 A := by
    nlinarith [mul_nonneg hr hs]
  simpa using mul_le_mul_of_nonneg_left hi hK.le

private theorem psi_le_bar {K alpha gamma A0 A : ℝ}
    (hK : 0 < K) (halpha : 0 < alpha) (hgamma : 0 ≤ gamma)
    (hA0 : 0 < A0) (hA : 0 < A) :
    psi K alpha gamma A0 A ≤ K * (1 + gamma / alpha) := by
  unfold psi
  have hs := saturation_le_one hA0 hA
  have hr : 0 ≤ gamma / alpha := div_nonneg hgamma halpha.le
  have hm : (gamma / alpha) * saturation A0 A ≤ gamma / alpha := by
    simpa using mul_le_mul_of_nonneg_left hs hr
  exact mul_le_mul_of_nonneg_left (by linarith) hK.le

private theorem phi_continuousAt_of_pos {K alpha gamma H0 H : ℝ}
    (hH0 : 0 < H0) (hH : 0 < H) :
    ContinuousAt (phi K alpha gamma H0) H := by
  unfold phi
  exact continuousAt_const.mul
    (continuousAt_const.add
      (continuousAt_const.mul (saturation_continuousAt_of_pos hH0 hH)))

private theorem psi_continuousAt_of_pos {K alpha gamma A0 A : ℝ}
    (hA0 : 0 < A0) (hA : 0 < A) :
    ContinuousAt (psi K alpha gamma A0) A := by
  unfold psi
  exact continuousAt_const.mul
    (continuousAt_const.add
      (continuousAt_const.mul (saturation_continuousAt_of_pos hA0 hA)))

/-- CTC-MATH-016: the bounded positive-coupling nullclines have an interior equilibrium.

This theorem proves existence and the coordinate bounds frozen in v0.1.0. It does not claim
uniqueness, global stability, or any empirical parameter value. -/
theorem interior_equilibrium_exists
    {A0 H0 KA KH alphaA alphaH gammaHA gammaAH : ℝ}
    (hA0 : 0 < A0) (hH0 : 0 < H0)
    (hKA : 0 < KA) (hKH : 0 < KH)
    (halphaA : 0 < alphaA) (halphaH : 0 < alphaH)
    (hgammaHA : 0 ≤ gammaHA) (hgammaAH : 0 ≤ gammaAH) :
    ∃ Astar Hstar : ℝ,
      0 < Astar ∧ 0 < Hstar ∧
      Astar = phi KA alphaA gammaHA H0 Hstar ∧
      Hstar = psi KH alphaH gammaAH A0 Astar ∧
      KA ≤ Astar ∧ Astar ≤ KA * (1 + gammaHA / alphaA) ∧
      KH ≤ Hstar ∧ Hstar ≤ KH * (1 + gammaAH / alphaH) := by
  rcases eq_or_lt_of_le hgammaHA with hzero | hpos
  · have hg0 : gammaHA = 0 := hzero.symm
    let Astar : ℝ := KA
    let Hstar : ℝ := psi KH alphaH gammaAH A0 Astar
    have hAstar : 0 < Astar := by simpa [Astar] using hKA
    have hHstar : 0 < Hstar := by
      dsimp [Hstar]
      exact psi_pos hKH halphaH hgammaAH hA0 hAstar
    have hAeq : Astar = phi KA alphaA gammaHA H0 Hstar := by
      simp [Astar, phi, hg0]
    have hHeq : Hstar = psi KH alphaH gammaAH A0 Astar := rfl
    have hHlo : KH ≤ Hstar := by
      dsimp [Hstar]
      exact psi_lower hKH halphaH hgammaAH hA0 hAstar
    have hHhi : Hstar ≤ KH * (1 + gammaAH / alphaH) := by
      dsimp [Hstar]
      exact psi_le_bar hKH halphaH hgammaAH hA0 hAstar
    refine ⟨Astar, Hstar, hAstar, hHstar, hAeq, hHeq, ?_, ?_, hHlo, hHhi⟩
    · simp [Astar]
    · simp [Astar, hg0]
  · let Abar : ℝ := KA * (1 + gammaHA / alphaA)
    let F : ℝ → ℝ := fun A => phi KA alphaA gammaHA H0 (psi KH alphaH gammaAH A0 A)
    let G : ℝ → ℝ := fun A => F A - A
    have hr : 0 < gammaHA / alphaA := div_pos hpos halphaA
    have hKAbar_lt : KA < Abar := by
      dsimp [Abar]
      have hi : 1 < 1 + gammaHA / alphaA := by linarith
      simpa using mul_lt_mul_of_pos_left hi hKA
    have hKAbar : KA ≤ Abar := hKAbar_lt.le
    have hFcont : ContinuousOn F (Set.Icc KA Abar) := by
      intro A hAI
      have hApos : 0 < A := lt_of_lt_of_le hKA hAI.1
      have hpsiPos : 0 < psi KH alphaH gammaAH A0 A :=
        psi_pos hKH halphaH hgammaAH hA0 hApos
      have houter := phi_continuousAt_of_pos
        (K := KA) (alpha := alphaA) (gamma := gammaHA)
        (H0 := H0) (H := psi KH alphaH gammaAH A0 A) hH0 hpsiPos
      have hinner := psi_continuousAt_of_pos
        (K := KH) (alpha := alphaH) (gamma := gammaAH)
        (A0 := A0) (A := A) hA0 hApos
      simpa [F, Function.comp_def] using (houter.comp hinner).continuousWithinAt
    have hGcont : ContinuousOn G (Set.Icc KA Abar) := by
      intro A hAI
      have hFc := hFcont A hAI
      change ContinuousWithinAt (F - id) (Set.Icc KA Abar) A
      exact hFc.sub continuousWithinAt_id
    have hpsiKApos : 0 < psi KH alphaH gammaAH A0 KA :=
      psi_pos hKH halphaH hgammaAH hA0 hKA
    have hFKA : KA ≤ F KA := by
      simpa [F] using
        (phi_lower hKA halphaA hgammaHA hH0 hpsiKApos)
    have hGKA : 0 ≤ G KA := by
      dsimp [G]
      linarith
    have hAbarPos : 0 < Abar := lt_trans hKA hKAbar_lt
    have hpsiAbarPos : 0 < psi KH alphaH gammaAH A0 Abar :=
      psi_pos hKH halphaH hgammaAH hA0 hAbarPos
    have hFAbar : F Abar < Abar := by
      simpa [F, Abar] using
        (phi_lt_bar hKA halphaA hpos hH0 hpsiAbarPos)
    have hGAbar : G Abar < 0 := by
      dsimp [G]
      linarith
    have hzeroMem : (0 : ℝ) ∈ Set.Icc (G Abar) (G KA) :=
      ⟨hGAbar.le, hGKA⟩
    have himage : (0 : ℝ) ∈ G '' Set.Icc KA Abar :=
      intermediate_value_Icc' hKAbar hGcont hzeroMem
    rcases himage with ⟨Astar, hAI, hGAstar⟩
    let Hstar : ℝ := psi KH alphaH gammaAH A0 Astar
    have hAstar : 0 < Astar := lt_of_lt_of_le hKA hAI.1
    have hHstar : 0 < Hstar := by
      dsimp [Hstar]
      exact psi_pos hKH halphaH hgammaAH hA0 hAstar
    have hFAstar : F Astar = Astar := by
      dsimp [G] at hGAstar
      linarith
    have hAeq : Astar = phi KA alphaA gammaHA H0 Hstar := by
      simpa [F, Hstar] using hFAstar.symm
    have hHeq : Hstar = psi KH alphaH gammaAH A0 Astar := rfl
    have hHlo : KH ≤ Hstar := by
      dsimp [Hstar]
      exact psi_lower hKH halphaH hgammaAH hA0 hAstar
    have hHhi : Hstar ≤ KH * (1 + gammaAH / alphaH) := by
      dsimp [Hstar]
      exact psi_le_bar hKH halphaH hgammaAH hA0 hAstar
    refine ⟨Astar, Hstar, hAstar, hHstar, hAeq, hHeq, hAI.1, ?_, hHlo, hHhi⟩
    simpa [Abar] using hAI.2

end CTC
