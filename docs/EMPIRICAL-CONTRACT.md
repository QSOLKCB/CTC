# CTC Empirical Contract

Status: **draft operational contract**

This document defines what must be measured before CTC may make empirical claims. The mathematical model is not permitted to smuggle empirical assumptions in as theorem premises that are later reported as facts.

## 1. Claim decomposition

CTC tracks eight claims independently.

| ID | Claim | Current status from the research synthesis |
|---|---|---|
| A | AI capability is increasing on fixed measurements | Supported on many benchmark and efficiency measures |
| B | Meaningful AI development intervals are compressing | Plausible, definition-sensitive |
| C | AI materially contributes to development of later AI | Emerging, not dominant or cleanly quantified |
| D | AI increases human productivity on bounded tasks | Strong task-level evidence |
| E | AI increases durable human learning or reasoning capacity | Mixed and under-measured |
| F | AI increases the rate of scientific or technological discovery | Domain-specific evidence, not established generally |
| G | AI-enhanced humans subsequently produce measurably better AI | Critical empirical gap |
| H | The complete H <-> A feedback loop is self-accelerating | Untested system-level hypothesis |

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

### 4.1 AI -> Human coupling gamma_AH

Target estimand:

```text
gamma_AH = causal effect of AI capability on the growth rate of a defined H measure.
```

Preferred designs:

- randomised controlled trial;
- stepped-wedge deployment;
- difference-in-differences around tool adoption;
- instrumental-variable design where valid;
- matched longitudinal cohorts with pre-registration and fixed outcomes.

The treatment variable should describe AI capability or assistance intensity, not merely binary access.

### 4.2 Human -> AI coupling gamma_HA

Target estimand:

```text
gamma_HA = causal effect of AI-enhanced human capability on subsequent AI capability growth.
```

This is the critical missing measurement.

A direct experiment could compare teams that are otherwise matched but differ in access to an AI research assistant, then evaluate the resulting successor systems on a blinded, fixed benchmark and resource budget.

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

The experiment must distinguish "more output" from "better successor AI".

## 5. Measuring generation intervals

A generation interval is not a product-release interval unless the release crosses a pre-defined capability threshold.

Define a sequence of ordered capability thresholds `theta_0 < theta_1 < ...` on a fixed or explicitly linked scale.

For AI:

```text
T_A[n] = time between first validated crossings of theta_A[n] and theta_A[n+1].
```

For humans:

```text
T_H[n] = time between first validated crossings of theta_H[n] and theta_H[n+1]
```

for a specified cohort, domain, and assessment.

Then

```text
kappa_A[n] = T_A[n+1] / T_A[n]
kappa_H[n] = T_H[n+1] / T_H[n].
```

A claim of telescoping requires a pre-specified statistical rule for deciding whether the observed sequence is inconsistent with constant or increasing intervals.

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

Estimate `gamma_AH`.

### Stage B: Human -> AI

Use the resulting researcher cohorts to develop successor AI systems under matched compute, data, time, and evaluation budgets.

Measure the successor systems with blinded fixed evaluations.

Estimate `gamma_HA`.

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

Strong CTC is rejected for an operational domain if repeated adequately powered studies find either:

1. `gamma_HA` is indistinguishable from zero or negative under the pre-registered successor-AI outcome; or
2. AI assistance produces no sustained reduction in any defined human epistemic transition interval after controlling for one-time level effects.

### 8.2 Falsification of self-acceleration

The self-accelerating version is rejected if:

- coupling effects decay toward zero over successive generations;
- `kappa_H >= 1` persistently under fixed measurement;
- AI productivity gains are one-time level shifts with no rate effect;
- non-compressible verification or experimental bottlenecks dominate system time;
- resource constraints force `T_A` to a stable floor without corresponding human-timescale compression.

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

These sources do not by themselves estimate `gamma_HA`. That parameter requires a targeted causal design.

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

> Do humans whose epistemic capability has been measurably increased by AI subsequently create measurably better AI, which then causes a further increase in human epistemic capability?

That is the loop the repository exists to test.
