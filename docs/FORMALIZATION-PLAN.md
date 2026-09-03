# CTC Lean 4 Formalisation Plan

Status: **planned for PR 2**

The first formalisation batch should prove only mathematics that is independent of empirical claims. It should be intentionally small, inspectable, and hostile to assumption smuggling.

## 1. Formalisation boundary

Lean may prove statements about:

- real numbers;
- sequences;
- inequalities;
- limits;
- geometric series;
- rational saturation functions;
- the telescopic recurrence;
- the queue-load inequality;
- `2 x 2` Jacobian algebra;
- existence of an interior equilibrium for the declared bounded nullcline maps.

Lean must not be used to make these empirical statements true by declaration:

- `gamma_AH > 0` in the real world;
- `gamma_HA > 0` in the real world;
- `xi_AH > 0` or `xi_HA > 0` in the real world;
- any measured value of `kappa_A` or `kappa_H`;
- the existence of AGI or ASI;
- a claimed singularity date;
- the validity of any benchmark as a universal capability measure.

Empirical propositions may later be represented as explicit hypotheses, never axioms masquerading as measurements.

## 2. Proposed source layout

```text
CTC/
  Basic.lean
  Saturation.lean
  GeometricTime.lean
  TelescopicTime.lean
  Verification.lean
  Equilibrium.lean
  Jacobian.lean
  Stability.lean
  All.lean
```

Suggested build files:

```text
lakefile.lean
lean-toolchain
```

The exact Lean and Mathlib versions should be pinned in the formalisation PR and then treated as part of the reproducibility contract.

## 3. Stage 1: bounded saturation functions

Define

```text
S(x; x0) = x / (x0 + x)
```

for `x > 0`, `x0 > 0`.

Targets:

```text
0 < S(x; x0)                           -- CTC-MATH-001
S(x; x0) < 1                           -- CTC-MATH-002
S is strictly monotone on positive reals -- CTC-MATH-014
```

The weak bound `S(x;x0) <= 1` may be a lemma derived from `CTC-MATH-002`; it is not a separate normative theorem ID.

Optional later target:

```text
Tendsto (fun x => x/(x0+x)) atTop (nhds 1)
```

These theorems support both capability coupling and telescopic-time coupling.

## 4. Stage 2: geometric compression

For

```text
T[n] = T0 * kappa^n
```

prove, under `T0 > 0` and `0 < kappa < 1`:

```text
HasSum (fun n => T0 * kappa^n) (T0 / (1-kappa)).  -- CTC-MATH-003
```

Positivity and strict decrease of `T[n]` may be proved as supporting lemmas.

Epistemic note: this theorem is elementary mathematics and carries no claim that real AI generation intervals follow a geometric law.

## 5. Stage 3: positive floor blocks finite-time accumulation

For

```text
Tfloor[n] = max (T0 * kappa^n) Tmin
```

with `Tmin > 0`, prove non-summability (`CTC-MATH-004`).

A robust proof route is comparison with the constant positive sequence:

```text
Tfloor[n] >= Tmin
```

for every `n`, so if `Tfloor` were summable then the constant positive lower bound would have to be summable, contradiction.

Avoid fragile ratio-test machinery where a direct comparison proof is available.

## 6. Stage 4: telescopic recurrence

Formalise a one-dimensional generic recurrence first:

```text
nextT Tmin eta xi s T =
  Tmin + (T - Tmin) * exp (-(eta + xi*s))
```

under:

```text
0 < Tmin
Tmin <= T
0 < eta
0 <= xi
0 <= s
s <= 1.
```

Targets:

1. `Tmin <= nextT ... T`. (`CTC-MATH-005`)
2. If `Tmin < T`, then `nextT ... T < T`. (`CTC-MATH-006`)
3. `nextT ... T - Tmin <= (T - Tmin) * exp(-eta)`.
4. Iterated recurrence remains above the floor.
5. Iterated recurrence is monotone non-increasing. (`CTC-MATH-015`)
6. The distance to the floor is bounded by `D0 * exp(-n*eta)`.
7. Therefore `T[n] -> Tmin`. (`CTC-MATH-007`)

Items 3, 4, and 6 are proof lemmas supporting the numbered contract rather than additional theorem IDs.

The state-dependent saturation value `s[n]` can initially be abstracted as any sequence in `[0,1]`. This keeps the proof reusable and avoids coupling the limit theorem to the capability ODE.

## 7. Stage 5: verification load

For positive `lambda`, `mu`, `A`, and `H`, prove:

```text
lambda*A <= mu*H
<->
lambda*A/(mu*H) <= 1.                 -- CTC-MATH-008
```

Define

```text
Xi = lambda*A/(mu*H).
```

Then prove for

```text
Bnext = max 0 (B + lambda*A - mu*H)
```

that if `Xi <= 1`, then `Bnext <= B` for `B >= 0` (`CTC-MATH-009`). The `Xi > 1` strict-increase and `Bnext >= 0` properties may be supporting lemmas.

## 8. Stage 6: corrected Jacobian algebra

At an interior equilibrium use symbolic **positive** values `p`, `q` and nonnegative values `b`, `c` with matrix

```text
J = [[-p, b], [c, -q]].
```

Do not formalise the full nonlinear ODE first. Prove the algebraic invariants independently.

Targets:

```text
trace J = -(p+q)
det J = p*q - b*c
```

Under `0 < p`, `0 < q`:

```text
trace J < 0.                            -- CTC-MATH-010
```

The determinant identity is `CTC-MATH-011`.

Under `0 <= b`, `0 <= c`:

```text
Delta = (p-q)^2 + 4*b*c >= 0.           -- CTC-MATH-012
```

Therefore the characteristic polynomial has real roots. The minimal positive-coupling Jacobian cannot have a non-real conjugate eigenpair.

## 9. Stage 7: local stability reduction

For a real `2 x 2` continuous-time Jacobian, local linear stability requires negative trace and positive determinant.

For the CTC Jacobian, negative trace is automatic under `p,q>0`, so prove the algebraic reduction:

```text
det J > 0 <-> b*c < p*q.                -- CTC-MATH-013
```

This is the canonical v0.1 stability inequality.

Formalising the full Hartman-Grobman or nonlinear local asymptotic stability theorem is not required in the first batch. The first batch should prove the CTC-specific algebra and cite the standard dynamical-systems theorem in prose until Mathlib support and proof scope are reviewed.

## 10. Stage 8: exclusion of Hopf in the minimal core

A classical Hopf bifurcation requires a complex-conjugate eigenpair crossing the imaginary axis.

The first Lean batch only needs the algebraic prerequisite already captured by `CTC-MATH-012`:

```text
Delta >= 0
```

for nonnegative positive-coupling parameters.

The repository may then state carefully:

> the minimal two-state positive-coupling Jacobian has real eigenvalues at an interior equilibrium, so the local spectral prerequisite for Hopf is absent.

Do not overstate this as a theorem about richer CTC models with delay, signed coupling, or extra state variables.

## 11. Stage 9: interior-equilibrium existence

Define the bounded nullcline maps

```text
phi(H) = K_A * (1 + (gamma_HA/alpha_A) * S_H(H))
psi(A) = K_H * (1 + (gamma_AH/alpha_H) * S_A(A)).
```

Target `CTC-MATH-016 interior_equilibrium_exists` under positive reference/carrying/growth parameters and nonnegative coupling.

Suggested proof structure:

1. If `gamma_HA = 0`, set `A_star = K_A` and `H_star = psi(K_A)` and verify both nullcline equations directly.
2. If `gamma_HA > 0`, define `A_bar = K_A * (1 + gamma_HA/alpha_A)` and `F(A) = phi(psi(A))` on `[K_A, A_bar]`.
3. Prove continuity of `F` and bounds `K_A <= F(A) < A_bar`.
4. Apply the intermediate value theorem to `F(A)-A`: it is nonnegative at `K_A` and negative at `A_bar`.
5. Set `H_star = psi(A_star)` and prove positivity and both equilibrium equations.

The expected coordinate bounds are

```text
K_A <= A_star <= K_A * (1 + gamma_HA/alpha_A)
K_H <= H_star <= K_H * (1 + gamma_AH/alpha_H).
```

Strict upper inequalities follow in a coordinate when its corresponding coupling coefficient is strictly positive. Uniqueness is explicitly **not** part of `CTC-MATH-016`.

A likely Mathlib route uses continuity of rational functions plus an interval-IVT theorem such as `intermediate_value_Icc`; exact theorem names should be verified against the pinned Mathlib revision rather than assumed in advance.

## 12. Suggested theorem IDs

Stable names make later documentation and empirical records easier to bind to formal results.

```text
CTC-MATH-001  saturation_pos
CTC-MATH-002  saturation_lt_one
CTC-MATH-003  geometric_compression_hasSum
CTC-MATH-004  positive_floor_not_summable
CTC-MATH-005  telescopic_floor_preserved
CTC-MATH-006  telescopic_strict_compression
CTC-MATH-007  telescopic_converges_to_floor
CTC-MATH-008  verification_load_iff
CTC-MATH-009  verification_backlog_nonincreasing
CTC-MATH-010  jacobian_trace_negative
CTC-MATH-011  jacobian_det_formula
CTC-MATH-012  jacobian_discriminant_nonnegative
CTC-MATH-013  local_stability_inequality
CTC-MATH-014  saturation_strict_mono
CTC-MATH-015  telescopic_iterate_antitone
CTC-MATH-016  interior_equilibrium_exists
```

This inventory must match `docs/MATHEMATICAL-CORE-v0.1.md` Section 13, `spec/ctc-core-v0.1.yaml`, and the PR 2 inventory in `ROADMAP.md`.

## 13. Trust rules

The formalisation PR should include a mechanical audit that rejects:

- `axiom` declarations in project theorem sources;
- `sorry`;
- `admit`;
- unreviewed local theorem substitutes with trusted-sounding names;
- empirical constants encoded as theorem facts without explicit assumptions.

The audit should verify the reviewed source files, not merely declaration names in prebuilt `.olean` artifacts.

## 14. PR sequencing

### PR 1

Freeze documentation, definitions, invariants, empirical contract, and theorem targets.

### PR 2

Add Lean project and prove `CTC-MATH-001` through `CTC-MATH-016` where Mathlib support is straightforward.

### PR 3

Add a deterministic numerical reference implementation and property tests that mirror the formal contracts. The common model-epoch sampling rule is implemented here; empirical asynchronous event alignment remains governed by `EMPIRICAL-CONTRACT.md`.

### PR 4

Add empirical data schemas and ingestion for public baseline datasets.

The order is intentional: definitions first, proofs second, simulation third, empirical fitting fourth.
