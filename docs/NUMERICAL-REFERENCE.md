# Deterministic Numerical Reference

Status: **PR 3 reference implementation**

This layer numerically implements the equations frozen in CTC `v0.1.0` and
machine-checked in `v0.2.0`. It does not introduce empirical parameter
estimates, forecasts, or new mathematical claims.

## Scope

The Python package in `src/ctc/` contains:

- the bounded saturation function;
- the continuous capability ODE;
- deterministic fixed-step RK4 integration on the declared common epoch grid;
- positive-floor telescopic-time updates;
- verification load and backlog updates;
- equilibrium and Jacobian diagnostics;
- seven synthetic reference scenarios.

The implementation uses the Python standard library only at runtime.

## Clock contract

A simulation declares

```text
t_n = t_0 + n * Delta_t
A[n] = A(t_n)
H[n] = H(t_n)
```

and integrates the continuous capability system from `t_n` to `t_(n+1)` with a
fixed number of RK4 substeps.

The discrete `eta`, `xi`, `lambda_A`, and `mu_H` values are **per declared model
epoch**. Changing `Delta_t` does not silently rescale them. A scientifically
meaningful change of epoch width therefore requires re-parameterisation outside
this reference implementation.

At epoch `n`, the `T_A`, `T_H`, and `B` updates use `A[n]` and `H[n]`. The
capability state is then integrated to `A[n+1]` and `H[n+1]`.

## Numerical policy

The reference implementation deliberately refuses to hide invalid numerical
states:

- positive-domain capability values are never clipped back above zero;
- interval floors are produced by the canonical recurrence, not by a post-hoc clamp;
- verification backlog uses `max(0, ...)` because that operation is part of the canonical equation;
- exact-floor epochs are rejected by the transformed `xi` outcome because the log ratio is undefined there.

If RK4 leaves the positive capability domain, the implementation raises an
error and tells the caller to reduce `Delta_t` or increase the number of
substeps.

## Formal-invariant mirrors

Tests exercise numerical counterparts of the frozen formal contracts:

- saturation positivity, upper bound, and strict monotonicity;
- positive floors and strict compression above the floor;
- convergence toward the floor;
- verification-load threshold behavior;
- Jacobian trace, determinant, discriminant, and real eigenvalues;
- interior-equilibrium witness and coordinate barriers.

These tests are regression checks on the implementation. They do not replace
the Lean proofs.

## Synthetic scenarios

`reference/scenarios-v0.1.json` contains exactly seven deterministic fixtures:

1. decoupled growth;
2. AI-assisted humanity only;
3. human-driven AI only;
4. bidirectional bounded coevolution;
5. baseline telescoping without cross-timescale attribution;
6. coupled telescopic coevolution;
7. verification-limited coevolution.

Every scenario is explicitly marked:

```text
SYNTHETIC_REFERENCE_FIXTURE
forecast = false
```

The numbers are chosen to exercise code paths. They are not measurements,
estimates, calibrations, or predictions.

## Reproducibility

The checked-in artifact is rendered with floats canonicalized to 12 significant
digits before JSON serialization. CI runs the reference suite on Python 3.11,
3.12, and 3.13 and checks that the renderer reproduces the committed artifact
and SHA-256 manifest.

Run locally:

```bash
python -m pip install -e .
python -m unittest discover -s tests -v
python scripts/check_reference_scenarios.py
```

To inspect the generated scenarios:

```bash
python scripts/generate_reference_scenarios.py
```
