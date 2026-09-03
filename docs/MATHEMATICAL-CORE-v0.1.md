# CTC Mathematical Core v0.1

Status: **draft mathematical contract, pre-formalisation**

This document defines the smallest CTC model intended to survive adversarial mathematical review. Capability dynamics, timescale dynamics, verification dynamics, and empirical attribution are kept distinct.

## 1. Epistemic boundary

The equations below define a mathematical model. They do not establish that real human or AI systems satisfy the model's assumptions.

A proof of a theorem about these equations proves only:

> if the stated mathematical assumptions hold, then the stated consequence follows.

Whether the assumptions hold in the world is an empirical question governed by `EMPIRICAL-CONTRACT.md`.

## 2. State variables

For continuous time `t >= 0`:

- `A(t) > 0`: dimensionless AI capability index.
- `H(t) > 0`: dimensionless human epistemic-capability index.

For a common discrete model epoch `n in N`:

- `T_A[n] >= T_A,min`: effective AI capability-transition interval.
- `T_H[n] >= T_H,min`: effective human epistemic-transition interval.
- `B[n] >= 0`: unresolved verification backlog.

Reference and constraint parameters:

- `A_0, H_0 > 0`: positive reference capability scales.
- `K_A, K_H > 0`: baseline resource-constrained carrying scales.
- `alpha_A, alpha_H > 0`: intrinsic capability-growth rates.
- `gamma_HA, gamma_AH >= 0`: cross-coupling strengths in the mutual-amplification regime.
- `T_A,min, T_H,min > 0`: hard lower bounds on generation intervals.
- `eta_A, eta_H > 0`: baseline timescale-compression rates.
- `xi_HA, xi_AH >= 0`: cross-coupling effects on timescale compression.
- `lambda_A, mu_H > 0`: verification-demand and verification-service coefficients.

The labels `HA` and `AH` encode direction:

- `gamma_HA`, `xi_HA`: Human -> AI.
- `gamma_AH`, `xi_AH`: AI -> Human.

The floor constraints are part of the admissible v0.1 state domain. An initial interval below its floor is outside the canonical contract. The recurrence itself would approach the floor from either side, but the floor-preservation invariant is asserted only for admissible states.

### 2.1 Continuous-to-discrete sampling rule

The capability ODE and the discrete subsystems use different mathematical clocks, so the bridge must be explicit.

Let

```text
t_0 < t_1 < t_2 < ...
```

be a declared common sequence of calendar-time model epochs. Define

```text
A[n] = A(t_n)
H[n] = H(t_n).
```

The recurrences for `T_A[n]`, `T_H[n]`, and `B[n]` use these sampled values and share the same model index `n`.

Empirical AI and human threshold crossings need not be synchronous. They may use separate event indices `i` and `j`. A numerical or empirical fit must declare how asynchronous observations are interpolated or aligned to the common `t_n` grid. The nth AI threshold event must never be silently identified with the nth human threshold event.

## 3. Bounded coupling functions

Define

```text
S_A(A) = A / (A_0 + A)
S_H(H) = H / (H_0 + H)
```

for positive arguments and reference scales.

These satisfy

```text
0 < S_A(A) < 1
0 < S_H(H) < 1
```

and

```text
dS_A/dA = A_0 / (A_0 + A)^2 > 0
dS_H/dH = H_0 / (H_0 + H)^2 > 0.
```

Unlike `log(1+x)`, these functions genuinely saturate:

```text
lim_(A->infinity) S_A(A) = 1
lim_(H->infinity) S_H(H) = 1.
```

## 4. Canonical capability subsystem

The minimal continuous model is

```text
dA/dt = A [ alpha_A (1 - A/K_A) + gamma_HA S_H(H) ]       (CTC-C1)

dH/dt = H [ alpha_H (1 - H/K_H) + gamma_AH S_A(A) ]       (CTC-C2)
```

This is a cooperative, mutually coupled logistic system with bounded cross-effects.

### 4.1 Positivity

Because each derivative contains its state variable as a multiplicative factor, the coordinate axes are invariant. With positive initial conditions, solutions cannot cross an axis under ordinary uniqueness assumptions for this smooth vector field.

Formal target:

```text
A(0) > 0 and H(0) > 0
=>
A(t) > 0 and H(t) > 0 for all times on the solution interval.
```

### 4.2 Bounded cross-effect and upper barriers

Since `S_H(H) < 1`,

```text
dA/dt < A [ alpha_A (1 - A/K_A) + gamma_HA ].
```

Therefore, for `gamma_HA >= 0`, any state satisfying

```text
A > K_A (1 + gamma_HA/alpha_A)
```

has `dA/dt < 0`.

Similarly,

```text
H > K_H (1 + gamma_AH/alpha_H)
```

implies `dH/dt < 0`.

Define

```text
A_bar = K_A (1 + gamma_HA/alpha_A)
H_bar = K_H (1 + gamma_AH/alpha_H).
```

These thresholds are simple a priori upper barriers for the minimal positive-coupling model. They prevent the bounded coupling terms themselves from forcing unlimited capability growth.

### 4.3 Interior equilibrium equations

At an interior equilibrium `(A*, H*)`, both bracketed growth terms vanish:

```text
alpha_A (1 - A*/K_A) + gamma_HA S_H(H*) = 0
alpha_H (1 - H*/K_H) + gamma_AH S_A(A*) = 0.
```

Equivalently, define nullcline maps

```text
phi(H) = K_A [1 + (gamma_HA/alpha_A) S_H(H)]
psi(A) = K_H [1 + (gamma_AH/alpha_H) S_A(A)]
```

and require

```text
A* = phi(H*)
H* = psi(A*).
```

Any such equilibrium obeys

```text
K_A <= A* <= A_bar
K_H <= H* <= H_bar.
```

When the corresponding coupling coefficient is strictly positive, the upper inequality is strict because `S < 1`; when it is zero, that coordinate equals its uncoupled carrying scale.

### 4.4 Existence of an interior equilibrium

**Claim.** For positive `A_0, H_0, K_A, K_H, alpha_A, alpha_H` and nonnegative `gamma_HA, gamma_AH`, at least one equilibrium exists in the positive quadrant.

If `gamma_HA = 0`, set

```text
A* = K_A
H* = psi(K_A).
```

Then `phi(H*) = K_A = A*`, `H* = psi(A*)`, and both coordinates are positive.

If `gamma_HA > 0`, let

```text
F(A) = phi(psi(A))
I = [K_A, A_bar].
```

`F` is continuous on `I`. For every `A in I`, boundedness of `S_H` gives

```text
K_A <= F(A) < A_bar.
```

Therefore

```text
F(K_A) - K_A >= 0
F(A_bar) - A_bar < 0.
```

By the intermediate value theorem there exists `A* in I` with `F(A*) = A*`. Set `H* = psi(A*)`. Then `A* = phi(H*)` and `H* = psi(A*)`, so both bracketed terms in `(CTC-C1)` and `(CTC-C2)` vanish. Positivity follows from `K_A,K_H>0`.

Uniqueness is **not** asserted in v0.1.

Evidence label: `FORMAL` conditional on the model assumptions. Planned theorem: `CTC-MATH-016 interior_equilibrium_exists`.

### 4.5 Nullcline-slope relation

At an interior equilibrium, with the Jacobian quantities defined in Section 5,

```text
phi'(H*) psi'(A*) = b c / (p q).
```

Thus `bc < pq` is equivalent to the composite nullcline slope being less than one at the equilibrium. This is a geometric interpretation of the local determinant condition, not a uniqueness theorem.

## 5. Correct local stability calculation

At an interior equilibrium define

```text
p = alpha_A A*/K_A > 0
q = alpha_H H*/K_H > 0
b = gamma_HA A* H_0 / (H_0 + H*)^2 >= 0
c = gamma_AH H* A_0 / (A_0 + A*)^2 >= 0.
```

The Jacobian is

```text
J* = [ -p   b ]
     [  c  -q ].
```

Its trace and determinant are

```text
tr(J*)  = -(p + q) < 0

det(J*) = p q - b c.
```

For a two-dimensional continuous autonomous system, an interior hyperbolic equilibrium is locally asymptotically stable when

```text
tr(J*) < 0  and  det(J*) > 0.
```

The trace condition is automatic here. Therefore the minimal CTC local-stability criterion is

```text
b c < p q.                                      (CTC-S1)
```

If `b c > p q`, the determinant is negative and the equilibrium is a saddle. If `b c = p q`, the equilibrium is non-hyperbolic and linearisation alone is insufficient.

### 5.1 Real-eigenvalue invariant

The characteristic discriminant is

```text
Delta = (p - q)^2 + 4 b c.
```

For nonnegative cross-coupling, `Delta >= 0`, and it is strictly positive unless both `p=q` and `bc=0`.

Therefore the minimal two-variable positive-coupling model has real Jacobian eigenvalues at an interior equilibrium.

Consequences:

- A local Hopf bifurcation is excluded in this minimal continuous model.
- Oscillatory coevolution is not produced by the two-state positive-coupling core alone.
- Any future oscillatory extension must add structure such as delays, additional state variables, signed coupling, or another dynamical mechanism.

This is a core invariant and should be machine-checked before a richer model is introduced.

## 6. Telescopic-time subsystem

Capability growth and generation time are distinct. CTC therefore models generation intervals separately on the common model epoch from Section 2.1.

Define

```text
T_A[n+1] = T_A,min
           + (T_A[n] - T_A,min)
             exp(-(eta_A + xi_HA S_H(H[n])))               (CTC-T1)

T_H[n+1] = T_H,min
           + (T_H[n] - T_H,min)
             exp(-(eta_H + xi_AH S_A(A[n])))               (CTC-T2)
```

with

```text
eta_A, eta_H > 0
xi_HA, xi_AH >= 0.
```

### 6.1 Floor preservation

For admissible states, if `T_A[n] >= T_A,min`, then

```text
T_A[n+1] >= T_A,min.
```

The same holds for `T_H`.

### 6.2 Strict compression above the floor

If `T_A[n] > T_A,min`, then the exponential factor lies strictly between zero and one, so

```text
T_A,min < T_A[n+1] < T_A[n].
```

Likewise for `T_H`.

### 6.3 Convergence to the physical floor

Let

```text
D_A[n] = T_A[n] - T_A,min >= 0.
```

Then

```text
D_A[n+1]
= D_A[n] exp(-(eta_A + xi_HA S_H(H[n])))
<= D_A[n] exp(-eta_A).
```

Hence

```text
0 <= D_A[n] <= D_A[0] exp(-n eta_A),
```

so

```text
T_A[n] -> T_A,min.
```

The corresponding result holds for the human timescale. This subsystem cannot generate a zero-time Zeno limit when `T_min > 0`.

### 6.4 Direction and attribution of timescale coupling

For fixed `T_A[n] > T_A,min` and `xi_HA > 0`, increasing `H[n]` increases `S_H(H[n])`, decreases the exponential factor, and therefore decreases `T_A[n+1]`.

The symmetric statement holds for AI capability acting on the human timescale when `xi_AH > 0`.

However, `eta_A,eta_H>0` produce baseline compression even when

```text
xi_HA = xi_AH = 0.
```

Therefore baseline compression is **not evidence of coupled telescopic coevolution**. Empirically, the cross-timescale effect must be nonzero or an equivalent causal design must attribute compression beyond the `eta` baseline to the opposite capability.

### 6.5 Compression ratios

Define model compression ratios

```text
kappa_A[n] = T_A[n+1] / T_A[n]
kappa_H[n] = T_H[n+1] / T_H[n].
```

For an admissible state strictly above its floor,

```text
0 < kappa_A[n] < 1
0 < kappa_H[n] < 1.
```

Unlike a pure geometric model, these ratios approach `1` as the state approaches its positive floor because the absolute remaining compressible interval vanishes.

Empirical threshold-crossing ratios are governed by `EMPIRICAL-CONTRACT.md`: unequal capability-threshold increments must be normalized before a telescoping claim is made.

## 7. Geometric-compression limiting case

For comparison only, suppose

```text
T[n] = T_0 kappa^n
```

with `T_0 > 0` and constant `0 < kappa < 1`.

Then

```text
sum_(n=0)^infinity T[n] = T_0 / (1-kappa) < infinity.
```

This is a standard geometric-series result. It is not evidence for a physical singularity.

If a positive floor is imposed,

```text
T[n] = max(T_0 kappa^n, T_min),
```

then

```text
sum_(n=0)^infinity T[n] = infinity
```

because the tail is bounded below by the positive constant `T_min`.

## 8. Timescale ratio

Define

```text
tau[n] = T_H[n] / T_A[n].                       (CTC-T3)
```

Interpretation:

- `tau >> 1`: human epistemic transitions are much slower than AI transitions.
- `tau ~= 1`: the effective transition timescales are comparable.
- `tau << 1`: the human transition interval is shorter than the AI interval.

CTC does not assume `tau` must monotonically decrease. The empirical question is whether AI-driven human timescale compression prevents sustained divergence between the two clocks.

## 9. Verification subsystem

Let `B[n] >= 0` be unresolved verification backlog and define

```text
B[n+1] = max(0, B[n] + lambda_A A[n] - mu_H H[n]).         (CTC-V1)
```

The incoming verification demand at step `n` is

```text
D[n] = lambda_A A[n],
```

and verification service capacity is

```text
C[n] = mu_H H[n].
```

Define the dimensionless load ratio

```text
Xi[n] = lambda_A A[n] / (mu_H H[n]).                       (CTC-V2)
```

for positive `H[n]`.

Then:

- `Xi[n] < 1` implies `D[n] < C[n]`, so backlog is non-increasing at that step.
- `Xi[n] = 1` implies zero net load before the non-negativity clamp.
- `Xi[n] > 1` implies `D[n] > C[n]`, so backlog strictly increases at that step.

This is a queue-load or arrival/service ratio. CTC deliberately does not call it an evolutionary Reynolds number.

## 10. Coupled-coevolution regimes

### Decoupled development

```text
gamma_AH ~= 0
gamma_HA ~= 0
```

AI and human capability changes are not measurably causing one another within the chosen operationalisation.

### AI-assisted humanity without reciprocal coevolution

```text
gamma_AH > 0
gamma_HA ~= 0.
```

### Human-driven AI without AI-induced human acceleration

```text
gamma_HA > 0
gamma_AH ~= 0.
```

### Coupled coevolution

```text
gamma_AH > 0
gamma_HA > 0.
```

Both capability cross-effects are measurably positive.

### Baseline telescoping without coupled timescale causation

```text
kappa_A[n] < 1
kappa_H[n] < 1
xi_HA ~= 0
xi_AH ~= 0.
```

This is compression, but it is not **coupled telescopic coevolution** because the opposite capability does not cause the compression.

### Coupled telescopic coevolution

In addition to positive bidirectional capability coupling, effective transition intervals compress and the compression contains identified opposite-system contributions:

```text
gamma_AH > 0
gamma_HA > 0
xi_AH > 0   (or identified causal equivalent)
xi_HA > 0   (or identified causal equivalent)
kappa_A[n] < 1
kappa_H[n] < 1
```

for a sustained, fixed operational window above the physical floors.

### Verification-limited coevolution

```text
Xi[n] > 1
```

for a sustained interval, so unresolved verification debt accumulates even if capability dynamics remain bounded.

## 11. Strong CTC hypothesis

A strong empirical version of CTC requires all of the following over a defined longitudinal window:

1. `gamma_AH > 0` under an identified causal or quasi-causal design matched to the transformed `S_A(A)` estimand.
2. `gamma_HA > 0` under an identified design that isolates retained human mediation from direct assistant effects.
3. AI-caused human-timescale compression beyond the `eta_H` baseline, represented by `xi_AH > 0` or an identified equivalent.
4. Human-caused AI-timescale compression beyond the `eta_A` baseline, represented by `xi_HA > 0` or an identified equivalent.
5. The effects persist beyond a one-time productivity level shift.
6. `T_A` and `T_H` use fixed reproducible equal-increment capability thresholds, or unequal increments are explicitly normalized.
7. At least one human epistemic timescale exhibits sustained compression attributable in part to AI assistance.
8. At least one subsequent AI capability measure exhibits improvement attributable in part to AI-enhanced **retained human capability**.

No claim of AGI, ASI, consciousness, autonomy, or a technological singularity is required.

## 12. Non-goals for v0.1

The core does not yet model:

- heterogeneous human populations;
- heterogeneous AI systems;
- network topology or adoption diffusion;
- delays;
- punctuated capability jumps;
- strategic behaviour;
- endogenous resource prices;
- negative coupling or skill atrophy as a separate state;
- model-collapse dynamics;
- stochastic shocks.

These are extensions, not excuses to overload the minimal core.

## 13. Formal theorem targets

The initial machine-checked batch should prove only stable mathematical facts.

| # | Statement | Theorem IDs |
|---|---|---|
| 1 | Positivity/upper bound and strict monotonicity of the saturation function | `CTC-MATH-001`, `CTC-MATH-002`, `CTC-MATH-014` |
| 2 | Geometric compression has finite accumulated time when `0 < kappa < 1` | `CTC-MATH-003` |
| 3 | A positive generation-time floor prevents finite accumulated time | `CTC-MATH-004` |
| 4 | The telescopic recurrence preserves `T >= T_min` | `CTC-MATH-005` |
| 5 | The telescopic recurrence strictly decreases above the floor and its iterates are non-increasing | `CTC-MATH-006`, `CTC-MATH-015` |
| 6 | The telescopic recurrence converges to `T_min` under `eta > 0` | `CTC-MATH-007` |
| 7 | `Xi <= 1` iff demand does not exceed service capacity; backlog is non-increasing below critical load | `CTC-MATH-008`, `CTC-MATH-009` |
| 8 | The interior Jacobian has negative trace and determinant `pq-bc` | `CTC-MATH-010`, `CTC-MATH-011` |
| 9 | Nonnegative mutual coupling gives nonnegative discriminant and hence real local eigenvalues | `CTC-MATH-012` |
| 10 | Local stability reduces algebraically to `bc < pq` | `CTC-MATH-013` |
| 11 | At least one positive-quadrant interior equilibrium exists under the v0.1 parameter assumptions | `CTC-MATH-016` |

This inventory must match `FORMALIZATION-PLAN.md` Section 12, `spec/ctc-core-v0.1.yaml`, and the PR 2 inventory in `ROADMAP.md`.

No theorem should encode an empirical parameter value as an axiom.
