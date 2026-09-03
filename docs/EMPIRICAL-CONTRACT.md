# CTC Empirical Contract

Status: **draft operational contract**

This document defines what must be measured before CTC may make empirical claims. The mathematical model is not permitted to smuggle empirical assumptions in as theorem premises that are later reported as facts.

## 1. Claim decomposition

CTC tracks eight claims independently.

| ID | Claim | Evidence label (v0.1) | Notes from the research synthesis |
|---|---|---|---|
| A | AI capability is increasing on fixed measurements | `OBSERVED` | Many benchmark and efficiency series; ceiling effects must be documented per Section 2.1 |
| B | Meaningful AI development intervals are compressing | `ESTIMATED` | Definition-sensitive and dependent on threshold/scale choice |
| C | AI materially contributes to development of later AI | `HYPOTHESIS` | Emerging workflow evidence, not cleanly quantified as a causal contribution |
| D | AI increases human productivity on bounded tasks | `CAUSAL` | Randomised and quasi-randomised task-level studies exist in bounded domains |
| E | AI increases durable human learning or reasoning capacity | `HYPOTHESIS` | Mixed results; retained capability is under-measured |
| F | AI increases the rate of scientific or technological discovery | `ESTIMATED` | Domain-specific evidence; not established generally |
| G | AI-enhanced humans subsequently produce measurably better AI | `HYPOTHESIS` | Critical empirical gap; the mediated reverse edge is not yet directly measured |
| H | The complete H <-> A feedback loop is self-accelerating | `SPECULATIVE` | Untested system-level claim |

Labels use the vocabulary of Section 11 and `AGENTS.md`. They describe the strongest evidence class currently available for the stated claim in at least one operational domain, not a universal verdict.

**Rule:** evidence for one claim cannot be substituted for evidence for another.

## 2. Operationalising AI capability A

A single scalar `A` is an abstraction. Empirical work should retain a vector of measurements and define any scalar reduction explicitly.

Candidate components:

- fixed benchmark performance;
- compute needed to reach a fixed performance threshold;
- algorithmic efficiency;
- code-generation and software-repair capability;
- reasoning performance on non-saturated evaluations;
- autonomous experimental throughput;
- fraction of an AI-development workflow completed without human intervention;
- cost and latency required to reach a fixed quality threshold.

### 2.1 Required rules

1. Do not define a new generation merely by a vendor model name.
2. Do not use a benchmark after saturation without documenting ceiling effects.
3. Prefer fixed capability thresholds over moving benchmark leaderboards.
4. Record model release date, evaluation date, evaluation version, cost, compute, and uncertainty.
5. Keep capability and resource consumption separate.

## 3. Operationalising human epistemic capability H

`H` must not mean biological intelligence. In CTC it denotes measurable human or human-group epistemic capability within a specified task domain.

Candidate components:

- time to fixed competence;
- retained learning after AI assistance is removed;
- quality-adjusted research output per researcher-hour;
- experimental cycle duration;
- independent verification throughput;
- cross-domain transfer performance;
- error-detection rate;
- hypothesis quality under blinded review;
- replication success;
- team problem-solving performance;
- ability to improve AI systems under controlled conditions.

### 3.1 Productivity is not learning

A faster task completion time is a **level or throughput effect** unless durable capability accumulation is separately measured.

CTC must distinguish:

```text
AI makes a person faster while the tool is present
```

from

```text
AI changes the rate at which the person acquires retained capability.
```

Only the second directly supports telescopic compression of a human epistemic timescale.

## 4. Measuring the coupling coefficients

The canonical ODE coefficients multiply transformed exposures in **per-capita growth rates**. Empirical estimands must match that structure rather than treating a raw capability contrast as a coupling coefficient.

Define

```text
g_A = (1/A) dA/dt
g_H = (1/H) dH/dt
```

so the canonical equations imply

```text
g_A - alpha_A (1 - A/K_A) = gamma_HA * S_H(H)
g_H - alpha_H (1 - H/K_H) = gamma_AH * S_A(A).
```

### 4.1 AI -> Human coupling gamma_AH

Target estimand:

```text
gamma_AH = causal coefficient on S_A(A)
in the per-capita human-capability growth equation,
conditional on the declared baseline term.
```

For a finite causal contrast between AI capability states `A_0` and `A_1`, the model predicts

```text
Delta g_H = gamma_AH * [S_A(A_1) - S_A(A_0)]
```

after accounting for the baseline human-growth term. A marginal design identifies `gamma_AH * S_A'(A)` unless the transformation is explicitly inverted. Therefore neither a raw `A` contrast nor a raw change in `H` may simply be reported as `gamma_AH`.

Preferred designs:

- randomised controlled trial;
- stepped-wedge deployment;
- difference-in-differences around tool adoption;
- instrumental-variable design where valid;
- matched longitudinal cohorts with pre-registration and fixed outcomes.

The treatment variable should describe AI capability or assistance intensity, not merely binary access. `A_0`, `K_H`, and other nuisance parameters used to recover `gamma_AH` must be pre-specified or estimated with uncertainty.

### 4.2 Human -> AI coupling gamma_HA

Target estimand:

```text
gamma_HA = causal coefficient on S_H(H)
in the per-capita successor-AI capability growth equation,
conditional on the declared baseline term.
```

For a finite causal contrast between retained human-capability states `H_0` and `H_1`, the model predicts

```text
Delta g_A = gamma_HA * [S_H(H_1) - S_H(H_0)]
```

after accounting for the baseline AI-growth term. A marginal design identifies `gamma_HA * S_H'(H)` unless the transformation is explicitly inverted.

This is the critical missing measurement.

A valid reverse-edge experiment must isolate **human mediation**. It is not enough for one treatment group to have an AI assistant while building the successor system, because direct assistant coding, debugging, search, or throughput can improve the successor without any retained change in human capability.

Preferred two-stage identification:

1. Randomise or quasi-randomise AI assistance and demonstrate a retained change in a pre-registered `H` outcome after assistance is removed or reduced.
2. During successor-AI development, remove or equalise assistant exposure across the resulting researcher cohorts, while matching compute, data, time, tooling, and evaluation budgets.
3. Evaluate successor systems with blinded fixed outcomes.

If assistant exposure cannot be removed or equalised, use an explicit mediation design that identifies the indirect effect through retained `H`; do not label the total effect of AI access on the successor as `gamma_HA`.

Example outcome dimensions:

- training efficiency;
- architecture quality;
- bug density;
- robustness;
- benchmark capability;
- inference cost;
- reproducibility;
- verified theorem or code contribution;
- successful experiment count.

The experiment must distinguish "more output" from "better successor AI" and direct machine assistance from the mediated human-capability effect.

## 5. Measuring generation intervals

A generation interval is not a product-release interval unless the release crosses a pre-defined capability threshold.

Define a sequence of ordered capability thresholds `theta_0 < theta_1 < ...` on a fixed or explicitly linked scale.

For AI:

```text
T_A[i] = time between first validated crossings of theta_A[i] and theta_A[i+1].
```

For humans:

```text
T_H[j] = time between first validated crossings of theta_H[j] and theta_H[j+1]
```

for a specified cohort, domain, and assessment. Separate event indices `i` and `j` are intentional: AI and human threshold crossings are generally asynchronous.

### 5.1 Threshold-spacing rule

A bare comparison of successive crossing intervals is valid only when threshold increments are equal on the pre-specified capability scale:

```text
Delta theta[n] = theta[n+1] - theta[n] = constant.
```

If increments are unequal, define the normalized crossing time

```text
U_A[i] = T_A[i] / (theta_A[i+1] - theta_A[i])
U_H[j] = T_H[j] / (theta_H[j+1] - theta_H[j])
```

and test compression using normalized ratios

```text
kappa_A_norm[i] = U_A[i+1] / U_A[i]
kappa_H_norm[j] = U_H[j+1] / U_H[j].
```

Unequal threshold spacing can manufacture apparent compression even when the underlying capability-growth rate is constant. A telescoping claim must therefore use equal increments or the normalized construction above.

### 5.2 Model-clock alignment

The mathematical recurrence uses a common model epoch `n` with declared calendar times `t_n` and samples

```text
A[n] = A(t_n)
H[n] = H(t_n).
```

Empirical threshold-event series `T_A[i]` and `T_H[j]` must not be silently identified with that common index. Any fit of the canonical recurrence must declare an alignment rule, such as evaluation of a continuous fitted capability trajectory at common calendar epochs, together with interpolation and uncertainty treatment.

A claim of telescoping requires a pre-specified statistical rule for deciding whether the observed or normalized interval sequence is inconsistent with constant or increasing transition time.

## 6. Minimum empirical test for CTC

The smallest convincing longitudinal test contains two linked stages.

### Stage A: AI -> Human

Randomise or quasi-randomise researchers to different AI-assistance levels.

Measure:

- retained domain competence;
- research-cycle time;
- verified output quality;
- independent error-detection ability;
- productivity after the assistance is removed or reduced.

Estimate `gamma_AH` against the transformed exposure `S_A(A)` and per-capita outcome defined in Section 4.1.

### Stage B: Human -> AI

Use the retained-capability researcher cohorts to develop successor AI systems under matched compute, data, time, and evaluation budgets. Remove or equalise AI-assistant exposure during this stage unless an explicit mediation design is used.

Measure the successor systems with blinded fixed evaluations.

Estimate `gamma_HA` against the transformed exposure `S_H(H)` and per-capita outcome defined in Section 4.2.

### Longitudinal repetition

Repeat across multiple capability transitions. A single two-stage experiment can establish bidirectional coupling, but not self-acceleration. Strong CTC requires persistence across generations.

## 7. Verification load

For a chosen domain and time window, measure:

```text
verification demand D[n]
verification service C[n]
```

in the same units, such as expert-review hours required and expert-review hours available.

Then

```text
Xi[n] = D[n] / C[n].
```

The proxy form

```text
Xi[n] = lambda_A A[n] / (mu_H H[n])
```

is valid only after `lambda_A` and `mu_H` have been estimated against common units.

Do not report `Xi > 1` from arbitrary composite indices.

## 8. Falsification criteria

### 8.1 Strong falsification of coupled telescopic coevolution

Strong CTC is rejected for an operational domain if repeated adequately powered studies find any of:

1. `gamma_AH` is indistinguishable from zero or negative under the pre-registered retained-human-capability outcome;
2. `gamma_HA` is indistinguishable from zero or negative under the pre-registered mediated successor-AI outcome;
3. AI assistance produces no sustained reduction in any defined human epistemic transition interval after controlling for one-time level effects; or
4. human capability produces no attributable reduction in a defined AI transition interval beyond the baseline `eta_A` compression term.

Conditions 1 and 2 test capability coupling. Conditions 3 and 4 test timescale coupling. A positive baseline `eta` or an unrelated secular trend cannot rescue a null cross-timescale effect.

### 8.2 Falsification of self-acceleration

The self-accelerating version is rejected if:

- coupling effects decay toward zero over successive generations;
- normalized `kappa_H >= 1` persistently under fixed measurement;
- AI productivity gains are one-time level shifts with no rate effect;
- non-compressible verification or experimental bottlenecks dominate system time;
- resource constraints force `T_A` to a stable floor without corresponding human-timescale compression;
- observed compression is explained by threshold spacing rather than a change in capability-growth rate.

### 8.3 Partial falsification

Individual claims A-G may be rejected without rejecting every other component of the framework.

## 9. Countervailing measurements

CTC must actively measure possible negative effects rather than treating them as anecdotes:

- metacognitive offloading;
- skill atrophy;
- reduced retention;
- automation bias;
- homogenisation of scientific hypotheses;
- synthetic-data degradation;
- verification overload;
- adoption inequality;
- increased resource concentration;
- reduced disruptive novelty.

A richer model may eventually allow signed or vector-valued coupling. v0.1 keeps the positive-coupling core simple but the empirical programme must look for negative channels.

## 10. Candidate public data sources

The research pass identified several useful sources for baseline construction:

- Epoch AI notable/frontier model data;
- Stanford AI Index;
- MLPerf;
- OpenAlex;
- Semantic Scholar Open Research Corpus;
- USPTO / PatentsView;
- GitHub Archive;
- OECD PISA / PIAAC;
- ClinicalTrials.gov;
- published replication data from AI-productivity experiments;
- published self-driving-laboratory throughput studies.

These sources do not by themselves estimate `gamma_HA`. That parameter requires a targeted causal mediation design.

## 11. Evidence labels

Every empirical claim in CTC should carry one of:

- `OBSERVED`: directly measured in the cited dataset.
- `ESTIMATED`: inferred by a declared statistical model.
- `CAUSAL`: supported by an identified causal design.
- `FORMAL`: proved from mathematical assumptions only.
- `HYPOTHESIS`: proposed and testable but not established.
- `SPECULATIVE`: outside current empirical support.

No document or code path may silently upgrade a label.

## 12. The central experiment

The decisive CTC question is not whether AI helps humans perform tasks.

It is:

> Do humans whose epistemic capability has been measurably increased by AI subsequently create measurably better AI under a design that isolates the retained human-mediated effect, which then causes a further increase in human epistemic capability?

That is the loop the repository exists to test.
