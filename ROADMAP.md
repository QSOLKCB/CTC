# CTC Roadmap

The repository is intentionally staged so that definitions, proofs, simulation, and empirical fitting cannot quietly contaminate one another.

## PR 1 - Mathematical Core v0.1

**Goal:** freeze a reviewable mathematical and epistemic contract before code or parameter fitting.

Deliverables:

- [x] expanded project README;
- [x] corrected minimal capability equations;
- [x] bounded cross-coupling functions;
- [x] corrected local Jacobian and stability condition;
- [x] explicit real-eigenvalue invariant for the two-state positive-coupling core;
- [x] positive-floor telescopic-time subsystem;
- [x] verification backlog and load-ratio subsystem;
- [x] empirical claim decomposition A-H;
- [x] falsification contract;
- [x] machine-readable v0.1 specification;
- [x] agent hard rules;
- [x] Lean theorem plan;
- [x] deep-research synthesis and correction log.

Exit criterion:

> The equations and epistemic rules are internally consistent enough to formalise without knowingly encoding the errors identified in the deep-research draft.

## PR 2 - Lean 4 Mathematical Core

**Goal:** machine-check the pure mathematical invariants without making empirical claims.

Planned theorem IDs:

- `CTC-MATH-001` saturation positivity;
- `CTC-MATH-002` saturation upper bound;
- `CTC-MATH-003` geometric compression finite sum;
- `CTC-MATH-004` positive floor prevents summability;
- `CTC-MATH-005` telescopic floor preservation;
- `CTC-MATH-006` strict compression above the floor;
- `CTC-MATH-007` convergence to the positive floor;
- `CTC-MATH-008` verification load equivalence;
- `CTC-MATH-009` backlog non-increase below critical load;
- `CTC-MATH-010` Jacobian trace negativity;
- `CTC-MATH-011` Jacobian determinant formula;
- `CTC-MATH-012` Jacobian discriminant non-negativity;
- `CTC-MATH-013` local stability inequality reduction.

Engineering requirements:

- pin Lean and Mathlib;
- deterministic CI;
- reject `sorry`, `admit`, and project `axiom` declarations;
- verify reviewed theorem sources, not merely cached declaration names;
- document any theorem deferred because Mathlib support is disproportionate to v0.1 scope.

Exit criterion:

> Every theorem claimed as `FORMAL` in the v0.1 core is either machine-checked or explicitly downgraded to a prose mathematical claim with a tracked formalisation gap.

## PR 3 - Deterministic Numerical Reference

**Goal:** implement the canonical equations without adding empirical parameter claims.

Suggested components:

```text
src/ctc/
  model.py
  saturation.py
  timescale.py
  verification.py
  diagnostics.py
```

Tests should mirror the formal invariants:

- positivity;
- saturation bounds;
- upper barriers;
- floor preservation;
- monotone timescale compression;
- convergence toward the floor;
- verification backlog threshold;
- Jacobian formulas;
- absence of complex eigenvalues under positive v0.1 coupling.

Add deterministic example scenarios:

1. decoupled growth;
2. AI-assisted humanity only;
3. human-driven AI only;
4. bidirectional bounded coevolution;
5. telescopic coevolution;
6. verification-limited coevolution.

No scenario may be labelled a forecast.

## PR 4 - Empirical Data Contract and Baselines

**Goal:** define reproducible schemas before ingesting public data.

Planned schemas:

- AI capability threshold crossing;
- AI model/resource metadata;
- human learning/competence transition;
- research-cycle timing;
- verification demand/service;
- intervention/treatment metadata;
- uncertainty and provenance;
- evidence label.

Candidate baseline sources:

- Epoch AI;
- Stanford AI Index;
- MLPerf;
- OpenAlex;
- Semantic Scholar;
- PatentsView;
- GitHub Archive;
- OECD PISA / PIAAC;
- ClinicalTrials.gov;
- replication datasets from published AI-productivity experiments.

Exit criterion:

> Every fitted parameter has a provenance path from raw observation to transformed estimate.

## PR 5 - Estimate AI -> Human Coupling

**Goal:** build a domain-specific estimate of `gamma_AH` from existing controlled or quasi-controlled studies.

Tasks:

- choose one domain first, preferably software engineering or bounded research tasks;
- separate throughput gains from retained capability gains;
- estimate uncertainty;
- test sensitivity to alternative definitions of `H`;
- do not generalise beyond the chosen domain.

Exit criterion:

> A reproducible, evidence-labelled estimate or confidence interval exists for a narrowly defined `gamma_AH`.

## PR 6 - Human -> AI Coupling Protocol

**Goal:** design the missing experiment for `gamma_HA`.

Protocol target:

```text
AI assistance
-> measured change in researcher capability
-> successor AI built under matched resources
-> blinded successor-AI evaluation.
```

The protocol should pre-register:

- treatment levels;
- human-capability outcomes;
- successor-AI outcomes;
- compute/data/time budgets;
- exclusion criteria;
- statistical model;
- minimum detectable effect;
- negative and null results.

Exit criterion:

> Another research group could run the protocol without guessing what CTC meant by the reverse coupling edge.

## PR 7 - Telescopic-Time Estimation

**Goal:** estimate `T_A`, `T_H`, `kappa_A`, `kappa_H`, and `tau` using fixed threshold definitions.

Key rule:

> product release cadence is not capability-transition cadence.

Tasks:

- define linked capability thresholds;
- estimate first-crossing dates;
- quantify uncertainty from benchmark changes;
- compare constant, geometric, logistic-floor, Gompertz, and regime-switching models;
- test whether a positive floor model is preferred;
- measure whether human epistemic timescales compress with AI exposure.

Exit criterion:

> Telescoping claims are model comparisons with uncertainty, not visual extrapolations from a hand-picked timeline.

## PR 8 - Verification Load and Backlog

**Goal:** instantiate `Xi` in common units.

Possible domain:

- generated software patches vs expert review hours;
- generated scientific claims vs expert verification hours;
- autonomous experiments vs validation throughput.

Required:

```text
Xi = demand rate / service rate
```

must use compatible units.

Exit criterion:

> `Xi > 1` or `Xi < 1` can be computed from measured quantities rather than arbitrary capability indices.

## PR 9 - Extended CTC Models

Only after the v0.1 core is formalised and numerically tested.

Candidate extensions:

- delay differential equations;
- vector-valued `H` separating productivity, retention, verification, and metacognition;
- vector-valued `A` separating reasoning, coding, science, autonomy, and efficiency;
- negative coupling / skill atrophy;
- stochastic shocks;
- adoption networks;
- institutional friction;
- resource constraints;
- punctuated-equilibrium transitions;
- synthetic-data feedback and model-collapse channels.

Oscillatory dynamics belong here, where delays or extra states can genuinely support them.

## PR 10 - Paper and Archival Release

Deliverables:

- canonical paper source;
- reproducibility bundle;
- frozen data snapshot or immutable references;
- machine-checked theorem inventory;
- numerical reference outputs and hashes;
- evidence matrix;
- limitations and falsification section;
- versioned release notes;
- archival DOI metadata.

Release rule:

> The paper must distinguish what is proved, measured, estimated, hypothesised, and speculative.

## Long-term question

The project ultimately asks whether the repeated causal chain

```text
AI_n -> Human_(n+1) -> AI_(n+1) -> Human_(n+2)
```

exists strongly enough, persistently enough, and quickly enough to produce coupled telescopic coevolution rather than merely faster machines or temporary human productivity gains.
