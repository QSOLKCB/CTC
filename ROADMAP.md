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
- [x] explicit continuous-to-discrete sampling contract;
- [x] interior-equilibrium existence statement and proof plan;
- [x] verification backlog and load-ratio subsystem;
- [x] empirical claim decomposition A-H with evidence labels;
- [x] transformed capability and timescale coupling estimands;
- [x] mediation controls for the reverse capability edge;
- [x] normalized threshold-spacing rule for telescoping claims;
- [x] equivalence-bound falsification contract for capability and timescale coupling;
- [x] machine-readable v0.1 specification;
- [x] agent hard rules;
- [x] Lean theorem plan;
- [x] deep-research synthesis and correction log.

Exit criterion:

> The equations and epistemic rules are internally consistent enough to formalise without knowingly encoding the errors identified in the deep-research draft or the PR 1 reviewer findings.

## PR 2 - Lean 4 Mathematical Core

**Goal:** machine-check the pure mathematical invariants without making empirical claims.

Planned theorem IDs:

- `CTC-MATH-001` saturation positivity;
- `CTC-MATH-002` saturation strict upper bound;
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
- `CTC-MATH-013` local stability inequality reduction;
- `CTC-MATH-014` saturation strict monotonicity;
- `CTC-MATH-015` telescopic iterate monotone non-increasing;
- `CTC-MATH-016` interior equilibrium existence.

Engineering requirements:

- pin Lean and Mathlib;
- deterministic CI;
- mechanically check theorem-ID agreement across normative files;
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
- saturation bounds and strict monotonicity;
- upper barriers;
- interior-equilibrium existence on admissible parameter fixtures;
- floor preservation;
- monotone timescale compression;
- convergence toward the floor;
- common model-epoch sampling `A[n]=A(t_n)`, `H[n]=H(t_n)`;
- verification backlog threshold;
- Jacobian formulas;
- absence of complex eigenvalues under positive v0.1 coupling.

Add deterministic example scenarios:

1. decoupled growth;
2. AI-assisted humanity only;
3. human-driven AI only;
4. bidirectional bounded coevolution;
5. baseline telescoping without coupled timescale causation;
6. coupled telescopic coevolution with nonzero cross-timescale effects;
7. verification-limited coevolution.

No scenario may be labelled a forecast.

## PR 4 - Empirical Data Contract and Baselines

**Goal:** define reproducible schemas before ingesting public data.

Planned schemas:

- AI capability threshold crossing;
- AI model/resource metadata;
- human learning/competence transition;
- research-cycle timing;
- asynchronous event index and calendar alignment;
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
- estimate the coefficient on transformed exposure `S_A(A)` in the per-capita `H` growth equation;
- estimate uncertainty in nuisance/reference parameters;
- test sensitivity to alternative definitions of `H`;
- do not generalise beyond the chosen domain.

Exit criterion:

> A reproducible, evidence-labelled estimate or confidence interval exists for a narrowly defined `gamma_AH` matched to the canonical ODE estimand.

## PR 6 - Human -> AI Coupling Protocol

**Goal:** design the missing mediated experiment for `gamma_HA`.

Protocol target:

```text
AI assistance
-> measured retained change in researcher capability
-> assistant exposure removed/equalised during successor development
-> successor AI built under matched resources
-> blinded successor-AI evaluation.
```

If assistant exposure cannot be removed or equalised, the protocol must identify the indirect effect through retained `H` with an explicit mediation design. A total effect of AI access on the successor must not be labelled `gamma_HA`.

The protocol should pre-register:

- treatment levels;
- retained human-capability outcomes;
- assistant-exposure handling in Stage B;
- successor-AI outcomes;
- transformed exposure `S_H(H)`;
- compute/data/time/tool budgets;
- exclusion criteria;
- statistical or mediation model;
- minimum detectable effect;
- negative and null results.

Exit criterion:

> Another research group could run the protocol without guessing what CTC meant by the reverse human-mediated coupling edge.

## PR 7 - Telescopic-Time Estimation

**Goal:** estimate `T_A`, `T_H`, `kappa_A`, `kappa_H`, `tau`, `xi_AH`, and `xi_HA` using fixed threshold definitions without threshold-spacing or floor artefacts.

Key rules:

> product release cadence is not capability-transition cadence.

> unequal capability increments must be normalized before a telescoping claim.

> `xi_AH` and `xi_HA` are coefficients on transformed floor-distance contraction outcomes, not raw interval changes or raw `kappa` values.

Tasks:

- define linked capability scales and pre-register threshold sequences;
- use equal capability increments where defensible;
- otherwise compute transition time per unit capability increment before compression ratios;
- retain separate AI and human event indices and declare calendar alignment;
- estimate first-crossing dates;
- quantify uncertainty from benchmark changes and interpolation;
- estimate or pre-specify `T_A,min`, `T_H,min`, `eta_A`, `eta_H`, `A_0`, and `H_0` with uncertainty propagation;
- for epochs strictly above the floors, construct
  `Y_H[n] = -log((T_H[n+1]-T_H,min)/(T_H[n]-T_H,min))` and
  `Y_A[n] = -log((T_A[n+1]-T_A,min)/(T_A[n]-T_A,min))`;
- estimate `xi_AH` as the coefficient on `S_A(A[n])` in `Y_H[n]` conditional on `eta_H`;
- estimate `xi_HA` as the coefficient on `S_H(H[n])` in `Y_A[n]` conditional on `eta_A`;
- exclude exact-floor epochs from ordinary `xi` regression because the transformed ratio is undefined there;
- pre-register smallest scientifically meaningful positive timescale couplings `delta_xi_AH` and `delta_xi_HA`;
- use equivalence/upper-bound analyses, not failed point-null significance tests, when claiming a timescale coupling is negligible;
- compare constant, geometric, logistic-floor, Gompertz, and regime-switching models;
- test whether a positive floor model is preferred.

Exit criterion:

> Telescoping claims are normalized, floor-aware, attributable model comparisons with uncertainty, and any `xi` estimate is bound to the canonical transformed estimand rather than inferred from visual or raw-interval compression.

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
