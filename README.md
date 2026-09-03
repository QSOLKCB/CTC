# Coupled Telescopic Coevolution (CTC)

**CTC** is a falsifiable mathematical framework for studying whether human and artificial cognitive systems can enter a mutually accelerating coevolutionary regime.

The motivating recursion is:

```text
AI_n -> Human_(n+1) -> AI_(n+1) -> Human_(n+2)
```

The central claim is deliberately narrower than a technological-singularity claim. CTC asks whether increasingly capable AI measurably increases the rate at which humans learn, reason, discover, verify, engineer, and coordinate, and whether those enhanced human capabilities then measurably improve subsequent AI systems.

## Core questions

CTC separates questions that are often collapsed into one story:

1. Is AI capability increasing?
2. Are meaningful AI development intervals compressing?
3. Does AI materially contribute to later AI development?
4. Does AI increase human productivity?
5. Does AI increase durable human learning or reasoning capacity?
6. Does AI increase the rate of scientific or technological discovery?
7. Do AI-enhanced humans subsequently produce measurably better AI?
8. Does the complete human-AI feedback loop become self-accelerating?

The framework treats each claim as independently testable. Evidence for one is not evidence for all eight. In v0.1, the AI development-interval compression claim remains a `HYPOTHESIS` until the thresholded longitudinal analysis planned for PR 7 is actually run.

## Mathematical core v0.1

Let `A(t) > 0` denote an AI capability index and `H(t) > 0` a human epistemic-capability index. Define bounded cross-coupling functions

```text
S_A(A) = A / (A_0 + A)
S_H(H) = H / (H_0 + H)
```

with positive reference scales `A_0, H_0`.

The minimal continuous capability model is

```text
dA/dt = A [ alpha_A (1 - A/K_A) + gamma_HA S_H(H) ]
dH/dt = H [ alpha_H (1 - H/K_H) + gamma_AH S_A(A) ]
```

where:

- `alpha_A`, `alpha_H` are intrinsic capability-growth rates;
- `K_A`, `K_H` are baseline resource-constrained carrying scales;
- `gamma_HA` is human-to-AI coupling;
- `gamma_AH` is AI-to-human coupling.

Positive `gamma_HA` and `gamma_AH` define a mutual-amplification regime. The cross-coupling is bounded rather than logarithmically unbounded.

## Telescopic time

Capability and generation time are distinct state variables. CTC therefore models the effective interval between meaningful capability transitions explicitly:

```text
T_A[n+1] = T_A,min + (T_A[n] - T_A,min)
             * exp(-(eta_A + xi_HA * S_H(H[n])))

T_H[n+1] = T_H,min + (T_H[n] - T_H,min)
             * exp(-(eta_H + xi_AH * S_A(A[n])))
```

For positive baseline compression rates `eta_A, eta_H`, nonnegative coupling coefficients `xi_HA, xi_AH`, and admissible initial intervals `T_A[0] >= T_A,min` and `T_H[0] >= T_H,min`, generation intervals remain at or above their physical floors and converge toward those floors rather than toward zero.

The discrete v0.1 model samples continuous capability on an equally spaced common calendar grid

```text
t_n = t_0 + n * Delta_t,    Delta_t > 0,
A[n] = A(t_n),
H[n] = H(t_n).
```

The discrete coefficients are defined per declared epoch width `Delta_t`. Changing the grid spacing requires re-parameterising those coefficients; the same numerical values must not be silently reused on a refined or coarsened grid. Empirical AI and human threshold crossings may be asynchronous and must be aligned by an explicit pre-registered rule rather than identifying the nth AI event with the nth human event.

The timescale ratio

```text
tau[n] = T_H[n] / T_A[n]
```

tracks whether human epistemic adaptation is keeping temporal pace with AI development.

Baseline compression alone is not sufficient to establish **coupled** telescopic coevolution. The strong empirical claim requires nonzero cross-timescale effects, or an equivalent identified attribution showing that opposite-system capability causes compression beyond the `eta` baseline. At a physical floor, the corresponding next interval is pinned to that floor, so no strict cross-capability compression effect is claimed there.

## Verification load

CTC keeps verification separate from capability. Let `B[n] >= 0` be unresolved verification backlog:

```text
B[n+1] = max(0, B[n] + lambda_A A[n] - mu_H H[n])
```

and define

```text
Xi[n] = lambda_A A[n] / (mu_H H[n]).
```

`lambda_A` and `mu_H` are per-epoch coefficients for the declared `Delta_t`. `Xi < 1` means verification service capacity exceeds incoming verification demand under the model; `Xi > 1` means verification debt accumulates while the state is held fixed. This is a queue-load ratio, not a Reynolds-number analogue.

## What CTC does not claim

CTC does **not** assume:

- AGI or ASI exists or must exist;
- capability growth is exponential forever;
- finite-time mathematical accumulation implies a physical singularity;
- AI assistance necessarily improves human reasoning;
- productivity gains are automatically learning-rate gains;
- either coupling direction is positive without measurement;
- failure to reject a zero coupling coefficient proves that the coupling is absent.

The strongest currently open empirical quantities are the human-to-AI coupling `gamma_HA`, cross-timescale coupling, and the human timescale compression dynamics `T_H` / `kappa_H`.

## Repository structure

- [`docs/MATHEMATICAL-CORE-v0.1.md`](docs/MATHEMATICAL-CORE-v0.1.md) — canonical equations, invariants, and corrected local stability analysis.
- [`docs/EMPIRICAL-CONTRACT.md`](docs/EMPIRICAL-CONTRACT.md) — claim matrix, operational measurements, falsification criteria, and dataset targets.
- [`docs/FORMALIZATION-PLAN.md`](docs/FORMALIZATION-PLAN.md) — Lean 4 theorem targets and proof order.
- [`docs/RESEARCH-SYNTHESIS.md`](docs/RESEARCH-SYNTHESIS.md) — literature ancestry, evidence boundaries, and adversarial corrections from the two deep-research passes.
- [`spec/ctc-core-v0.1.yaml`](spec/ctc-core-v0.1.yaml) — machine-readable mathematical contract.
- [`ROADMAP.md`](ROADMAP.md) — staged implementation plan.
- [`AGENTS.md`](AGENTS.md) — machine-agent rules for preserving epistemic and mathematical invariants.

## Epistemic rule

> A theorem about the CTC equations is not evidence that the empirical world satisfies the theorem's assumptions.

Mathematical validity, parameter estimation, causal evidence, and speculative extrapolation are tracked separately throughout this repository.

## Status

**v0.1 mathematical contract: draft / pre-formalisation.**

The immediate next phase is a small Lean 4 batch proving only pure mathematical invariants before any empirical parameter values are frozen.

## License

Apache License 2.0. See [`LICENSE`](LICENSE).
