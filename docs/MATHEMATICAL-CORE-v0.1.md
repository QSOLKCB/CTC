# CTC Mathematical Core v0.1

Status: **draft mathematical contract, pre-formalisation**

This document defines the smallest CTC model that is intended to survive adversarial mathematical review. It deliberately separates capability dynamics, timescale dynamics, and verification dynamics.

## 1. Epistemic boundary

The equations below define a mathematical model. They do not establish that real human or AI systems satisfy the model's assumptions.

A proof of a theorem about these equations proves only:

> if the stated mathematical assumptions hold, then the stated consequence follows.

Whether the assumptions hold in the world is an empirical question governed by `EMPIRICAL-CONTRACT.md`.

## 2. State variables

For continuous time `t >= 0`:

- `A(t) > 0`: dimensionless AI capability index.
- `H(t) > 0`: dimensionless human epistemic-capability index.

For discrete capability-transition index `n in N`:

- `T_A[n] > 0`: effective time between meaningful AI capability transitions.
- `T_H[n] > 0`: effective time between meaningful human epistemic transitions.
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

- `gamma_HA`: Human -> AI.
- `gamma_AH`: AI -> Human.

## 3. Bounded coupling functions

Define

```text
S_A(A) = A / (A_0 + A)
S_H(H) = H / (H_0 + H)
```

for `A, H > 0` and `A_0, H_0 > 0`.

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

### 4.2 Bounded cross-effect

Since `S_H(H) < 1`,

```text
dA/dt < A [ alpha_A (1 - A/K_A) + gamma_HA ].
```

Therefore, for `gamma_HA >= 0`, any state satisfying

```text
A > K_A (1 + gamma_HA/alpha_A)
```

has `dA/dt < 0`.

Similarly, any state satisfying

```text
H > K_H (1 + gamma_AH/alpha_H)
```

has `dH/dt < 0`.

These thresholds provide simple a priori upper barriers for the minimal positive-coupling model. They prevent the bounded coupling term itself from forcing unlimited capability growth.

### 4.3 Interior equilibrium equations

At an interior equilibrium `(A*, H*)`, both bracketed growth terms vanish:

```text
alpha_A (1 - A*/K_A) + gamma_HA S_H(H*) = 0
alpha_H (1 - H*/K_H) + gamma_AH S_A(A*) = 0.
```

Equivalently,

```text
A* = K_A [1 + (gamma_HA/alpha_A) S_H(H*)]
H* = K_H [1 + (gamma_AH/alpha_H) S_A(A*)].
```

For positive coupling, any interior equilibrium lies at or above the uncoupled carrying scales and strictly above them when the opposite capability is positive and the corresponding coupling is strictly positive.

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

If `b c > p q`, the determinant is negative and the equilibrium is a saddle.

If `b c = p q`, the equilibrium is non-hyperbolic and linearisation alone is insufficient.

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

Capability growth and generation time are distinct. CTC therefore models generation intervals separately.

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

If `T_A[n] >= T_A,min`, then

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

The corresponding result holds for the human timescale.

This subsystem cannot generate a zero-time Zeno limit when `T_min > 0`.

### 6.4 Direction of coupling is correct by construction

For fixed `T_A[n] > T_A,min` and `xi_HA > 0`, increasing `H[n]` increases `S_H(H[n])`, decreases the exponential factor, and therefore decreases `T_A[n+1]`.

Thus greater human capability accelerates AI timescale compression in the intended direction.

The symmetric statement holds for AI capability acting on the human timescale.

### 6.5 Compression ratios

Define the observed compression ratios

```text
kappa_A[n] = T_A[n+1] / T_A[n]
kappa_H[n] = T_H[n+1] / T_H[n].
```

For a state above its floor,

```text
0 < kappa_A[n] < 1
0 < kappa_H[n] < 1.
```

Unlike a pure geometric model, these ratios approach `1` as `T_A[n]` or `T_H[n]` approaches its floor because the absolute remaining compressible interval vanishes.

## 7. The geometric-compression limiting case

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

CTC distinguishes at least the following empirical regimes.

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

AI improves measured human capability, but the improved humans do not measurably improve subsequent AI.

### Human-driven AI without AI-induced human acceleration

```text
gamma_HA > 0
gamma_AH ~= 0.
```

Human capability drives AI development, but AI does not measurably increase the human accumulation rate.

### Coupled coevolution

```text
gamma_AH > 0
gamma_HA > 0.
```

Both cross-effects are measurably positive.

### Coupled telescopic coevolution

In addition to positive bidirectional coupling, effective transition intervals compress relative to a fixed operational definition:

```text
kappa_A[n] < 1
kappa_H[n] < 1
```

for a sustained measurement window.

### Verification-limited coevolution

```text
Xi[n] > 1
```

for a sustained interval, so unresolved verification debt accumulates even if capability dynamics remain bounded.

## 11. Strong CTC hypothesis

A strong empirical version of CTC requires all of the following over a defined longitudinal window:

1. `gamma_AH > 0` under causal or quasi-causal estimation.
2. `gamma_HA > 0` under causal or quasi-causal estimation.
3. The effects persist beyond a one-time productivity level shift.
4. `T_A` and `T_H` are defined using fixed reproducible thresholds.
5. At least one human epistemic timescale exhibits sustained compression attributable in part to AI assistance.
6. At least one subsequent AI capability measure exhibits improvement attributable in part to AI-enhanced human work.

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

The initial machine-checked batch should prove only stable mathematical facts:

1. Bounds and monotonicity of `S_A` and `S_H`.
2. Geometric compression has finite accumulated time when `0 < kappa < 1`.
3. A positive generation-time floor prevents finite accumulated time.
4. The redesigned telescopic recurrence preserves `T >= T_min`.
5. The redesigned telescopic recurrence strictly decreases `T` above the floor.
6. The redesigned telescopic recurrence converges to `T_min` under `eta > 0`.
7. `Xi <= 1` is equivalent to verification demand not exceeding service capacity under positive denominators.
8. The continuous interior Jacobian has negative trace.
9. The local stability criterion reduces to `bc < pq`.
10. Nonnegative mutual coupling gives a nonnegative Jacobian discriminant, excluding complex local eigenvalues in the minimal model.

No theorem should encode an empirical parameter value as an axiom.
