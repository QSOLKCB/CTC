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
- `2 x 2` Jacobian algebra.

Lean must not be used to make these empirical statements true by declaration:

- `gamma_AH > 0` in the real world;
- `gamma_HA > 0` in the real world;
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
0 < S(x; x0)
S(x; x0) < 1
S(x; x0) <= 1
S is strictly monotone on positive reals
```

Optional later targets:

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
HasSum (fun n => T0 * kappa^n) (T0 / (1-kappa)).
```

Also prove positivity and strict decrease of `T[n]`.

Epistemic note: this theorem is elementary mathematics and carries no claim that real AI generation intervals follow a geometric law.

## 5. Stage 3: positive floor blocks finite-time accumulation

For

```text
Tfloor[n] = max (T0 * kappa^n) Tmin
```

with `Tmin > 0`, prove non-summability.

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

1. `Tmin <= nextT ... T`.
2. If `Tmin < T`, then `nextT ... T < T`.
3. `nextT ... T - Tmin <= (T - Tmin) * exp(-eta)`.
4. Iterated recurrence remains above the floor.
5. Iterated recurrence is monotone non-increasing.
6. The distance to the floor is bounded by `D0 * exp(-n*eta)`.
7. Therefore `T[n] -> Tmin`.

The state-dependent saturation value `s[n]` can initially be abstracted as any sequence in `[0,1]`. This keeps the proof reusable and avoids coupling the limit theorem to the capability ODE.

## 7. Stage 5: verification load

For positive `lambda`, `mu`, `A`, and `H`, prove:

```text
lambda*A <= mu*H
<->
lambda*A/(mu*H) <= 1.
```

Define

```text
Xi = lambda*A/(mu*H).
```

Then prove the backlog step properties for

```text
Bnext = max 0 (B + lambda*A - mu*H).
```

Targets:

- if `Xi <= 1`, then `Bnext <= B` for `B >= 0`;
- if `Xi > 1`, then `Bnext > B` for `B >= 0`;
- `Bnext >= 0` always.

## 8. Stage 6: corrected Jacobian algebra

At an interior equilibrium use symbolic nonnegative values `p`, `q`, `b`, `c` and matrix

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
trace J < 0.
```

Under `0 <= b`, `0 <= c`:

```text
Delta = (p-q)^2 + 4*b*c >= 0.
```

Therefore the characteristic polynomial has real roots. The minimal positive-coupling Jacobian cannot have a non-real conjugate eigenpair.

## 9. Stage 7: local stability reduction

For a real `2 x 2` continuous-time Jacobian, local linear stability requires negative trace and positive determinant.

For the CTC Jacobian, negative trace is automatic under `p,q>0`, so prove the algebraic reduction:

```text
det J > 0 <-> b*c < p*q.
```

This is the canonical v0.1 stability inequality.

Formalising the full Hartman-Grobman or nonlinear local asymptotic stability theorem is not required in the first batch. The first batch should prove the CTC-specific algebra and cite the standard dynamical-systems theorem in prose until Mathlib support and proof scope are reviewed.

## 10. Stage 8: exclusion of Hopf in the minimal core

A classical Hopf bifurcation requires a complex-conjugate eigenpair crossing the imaginary axis.

The first Lean batch only needs the algebraic prerequisite:

```text
Delta >= 0
```

for nonnegative positive-coupling parameters.

The repository may then state carefully:

> the minimal two-state positive-coupling Jacobian has real eigenvalues at an interior equilibrium, so the local spectral prerequisite for Hopf is absent.

Do not overstate this as a theorem about richer CTC models with delay, signed coupling, or extra state variables.

## 11. Suggested theorem IDs

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
```

## 12. Trust rules

The formalisation PR should include a mechanical audit that rejects:

- `axiom` declarations in project theorem sources;
- `sorry`;
- `admit`;
- unreviewed local theorem substitutes with trusted-sounding names;
- empirical constants encoded as theorem facts without explicit assumptions.

The audit should verify the reviewed source files, not merely declaration names in prebuilt `.olean` artifacts.

## 13. PR sequencing

### PR 1

Freeze documentation, definitions, invariants, empirical contract, and theorem targets.

### PR 2

Add Lean project and prove `CTC-MATH-001` through `CTC-MATH-013` where Mathlib support is straightforward.

### PR 3

Add a deterministic numerical reference implementation and property tests that mirror the formal contracts.

### PR 4

Add empirical data schemas and ingestion for public baseline datasets.

The order is intentional: definitions first, proofs second, simulation third, empirical fitting fourth.
