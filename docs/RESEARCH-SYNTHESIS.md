# CTC Research Synthesis

This document records the high-level findings from two deep-research passes used to design CTC v0.1. It is a research map, not a substitute for the primary literature.

## 1. Central result of the research passes

The literature supports several pieces of the CTC picture separately, but does not currently establish the complete coupled loop.

| Claim | Evidence label (v0.1) | Synthesis |
|---|---|---|
| AI capability growth | `OBSERVED` | Substantial support on fixed benchmark, compute-efficiency, and algorithmic-efficiency series |
| AI -> bounded human productivity | `CAUSAL` | Substantial task-level support from controlled studies |
| AI -> durable human learning | `HYPOTHESIS` | Mixed and under-measured; retention is the key gap |
| AI -> faster scientific discovery | `ESTIMATED` | Domain-specific support, not a general law |
| AI -> later AI development | `HYPOTHESIS` | Emerging workflow evidence, incompletely quantified |
| AI-enhanced Human -> later AI | `HYPOTHESIS` | Critical empirical gap; retained human mediation has not been directly isolated |
| complete self-accelerating H <-> A | `SPECULATIVE` | Untested system-level claim |

These labels follow `EMPIRICAL-CONTRACT.md` and `AGENTS.md`; they are not universal verdicts across all domains.

The research passes therefore support building CTC as a falsifiable framework, not announcing CTC as an observed law.

## 2. Closest intellectual ancestors

### Endogenous growth

Romer-style knowledge accumulation places human research effort and existing knowledge in the same growth equation. This is a direct structural ancestor of the `H -> A` side of CTC, but standard formulations do not add an explicit reverse `A -> H` capability equation or generation-time compression.

Key source:

- Paul M. Romer, "Endogenous Technological Change," *Journal of Political Economy* 98(5), 1990. DOI: `10.1086/261725`.

### Semi-endogenous growth and declining research productivity

Jones-type models add diminishing returns to existing knowledge. Bloom et al. provide important empirical counter-pressure by showing that research effort has risen substantially in several domains while measured idea productivity has declined.

Key sources:

- Charles I. Jones, "R&D-Based Models of Economic Growth," *Journal of Political Economy* 103(4), 1995. DOI: `10.1086/262002`.
- Bloom, Jones, Van Reenen, Webb, "Are Ideas Getting Harder to Find?" *American Economic Review* 110(4), 2020. DOI: `10.1257/AER.20180338`.

### Cumulative cultural evolution and collective intelligence

Cumulative cultural evolution supplies the ratchet-like inheritance concept. Collective-brain models supply a way to think about innovation as a property of connected populations rather than isolated individuals.

Key sources:

- Mesoudi and Thornton, "What is cumulative cultural evolution?" *Proceedings of the Royal Society B* 285, 2018. DOI: `10.1098/rspb.2018.0712`.
- Muthukrishna and Henrich, "Innovation in the collective brain," *Philosophical Transactions of the Royal Society B* 371, 2016. DOI: `10.1098/rstb.2015.0192`.
- Creanza, Kolodny, Feldman, "Cultural evolutionary theory," *PNAS* 114(30), 2017. DOI: `10.1073/pnas.1620732114`.

### Gene-culture coevolution and niche construction

These literatures provide structural examples in which one evolving system changes the environment that selects or shapes the other. CTC uses this only as mathematical and conceptual ancestry. AI capability is not treated as a gene frequency.

Key source:

- Laland, Odling-Smee, Myles, "How culture shaped the human genome," *Nature Reviews Genetics* 11, 2010. DOI: `10.1038/nrg2734`.

### Coevolutionary dynamics

Adaptive dynamics and cooperative dynamical systems provide tools for coupled state evolution, Jacobian analysis, stability, and regime transitions.

Key source:

- Dieckmann and Law, "The dynamical theory of coevolution," *Journal of Mathematical Biology* 34, 1996. DOI: `10.1007/BF02409751`.

### Autocatalysis and hypercycles

Hypercycle and autocatalytic models show how mutually catalytic components can amplify one another. They are useful analogues for feedback topology, but unconstrained autocatalytic growth is not an acceptable default CTC model because it lacks empirically necessary saturation mechanisms.

Key source:

- Eigen and Schuster, "The Hypercycle," *Naturwissenschaften* 64, 1977. DOI: `10.1007/BF00450633`.

### Human-computer symbiosis and AI extenders

Licklider-style human-computer symbiosis and later work on AI cognitive extension are important conceptual ancestors of the `AI -> Human` channel.

Key source:

- Hernandez-Orallo and Vold, "AI Extenders," AIES 2019. DOI: `10.1145/3306618.3314238`.

## 3. Empirical anchors

### AI-assisted professional work

Published controlled studies report meaningful productivity gains in bounded writing, software-development, and customer-service tasks. These support an `AI -> Human` productivity channel, but they do not by themselves establish durable learning-rate acceleration.

Key sources:

- Noy and Zhang, "Experimental evidence on the productivity effects of generative artificial intelligence," *Science* 381, 2023. DOI: `10.1126/science.adh2586`.
- Peng et al., "The Impact of AI on Developer Productivity: Evidence from GitHub Copilot," 2023. arXiv: `2302.06590`.
- Brynjolfsson, Li, Raymond, "Generative AI at Work," NBER Working Paper 31161, 2023. DOI: `10.3386/w31161`.

### Algorithmic and compute progress

AI capability progress has multiple drivers, including larger training budgets and improving algorithmic efficiency. CTC should not collapse these into one unexplained time trend.

Key sources:

- Sevilla et al., "Compute Trends Across Three Eras of Machine Learning," IJCNN 2022. DOI: `10.1109/IJCNN55064.2022.9891914`.
- Kaplan et al., "Scaling Laws for Neural Language Models," 2020. arXiv: `2001.08361`.
- Hoffmann et al., "Training Compute-Optimal Large Language Models," 2022. arXiv: `2203.15556`.
- Hernandez and Brown, "Measuring the Algorithmic Efficiency of Neural Networks," 2020. arXiv: `2005.04305`.
- Ho et al., "Algorithmic Progress in Language Models," NeurIPS 2024.

### AI-assisted science

Self-driving laboratories show that closed-loop automation can compress experimental cycles in narrow scientific settings. AlphaFold-related work shows that AI can redirect research activity toward previously less tractable targets. These are important `AI -> Human/Science` channels, but they do not yet establish general acceleration of all scientific verification stages.

Key sources:

- MacLeod et al., "Self-driving laboratory for accelerated discovery of thin-film materials," *Science Advances* 6, 2020. DOI: `10.1126/sciadv.aaz8867`.
- Ryan R. Hill and Carolyn Stein, "How Artificial Intelligence Shapes Science: Evidence from AlphaFold," NBER Working Paper **35143**, 2026. DOI: `10.3386/w35143`.

The Hill-Stein working-paper number, year, and DOI were rechecked against the NBER record during PR 1 review.

### Countervailing evidence

CTC must incorporate evidence that human epistemic systems can slow, saturate, or degrade even while tools improve.

Relevant findings include declining measured research productivity, declining disruption metrics in papers and patents, and reported metacognitive costs from some forms of generative-AI use.

Key sources:

- Park, Leahey, Funk, "Papers and patents are becoming less disruptive over time," *Nature* 613, 2023. DOI: `10.1038/s41586-022-05543-x`.
- Bloom et al. 2020, DOI: `10.1257/AER.20180338`.
- Fan et al., "Beware of metacognitive laziness," *British Journal of Educational Technology* 55, 2024. DOI: `10.1111/bjet.13544`.

These are not automatic falsifications of CTC. They are constraints any credible CTC fit must overcome rather than ignore.

## 4. Why CTC is not a singularity model

Classic intelligence-explosion and singularity literature asks whether machine intelligence can recursively improve until qualitative or superhuman transitions occur.

CTC asks a different and earlier question:

```text
Does AI improve humans in ways that causally improve later AI,
and does that later AI then further improve humans?
```

This loop can exist below any definition of AGI and can fail even if individual AI systems become extremely capable.

Singularity literature is therefore treated as a possible limiting scenario, not as evidence for CTC.

Relevant background:

- Hutter, "Can Intelligence Explode?" 2012. arXiv: `1202.6177`.
- Sandberg, "An Overview of Models of Technological Singularity," 2013. DOI: `10.1002/9781118555927.ch36`.

## 5. The important novelty claim

The research passes found established precedents for:

- one-directional knowledge accumulation;
- cultural accumulation;
- mutually coupled dynamical systems;
- AI productivity effects;
- AI scaling and efficiency trends;
- verification bottlenecks;
- bounded technological learning curves.

The potentially novel contribution is the combined object:

```text
bidirectional human-AI capability coupling
+
explicit human and AI transition-time state variables
+
endogenous cross-attributed timescale compression
+
verification capacity as a separate load process.
```

This novelty claim remains `HYPOTHESIS` until a formal prior-art search is completed for the exact combination.

## 6. Corrections made after the mathematical deep-research pass

The second pass was useful, but several proposed mathematical statements were rejected before becoming repository invariants.

### 6.1 Rejected: logarithmic coupling described as saturating

A term such as

```text
log(1 + H/H_0)
```

grows without bound. It grows slowly, but does not saturate.

v0.1 replaces it with

```text
H/(H_0+H),
```

which is monotone and bounded above by one.

### 6.2 Rejected: an incorrect discrete Jury reduction

The deep-research draft reduced a discrete-map stability condition incorrectly. v0.1 avoids carrying that error forward by selecting a cleaner continuous-time capability core and deriving its `2 x 2` Jacobian directly.

The canonical continuous local condition is

```text
b*c < p*q,
```

with negative trace automatic for positive intrinsic damping terms.

### 6.3 Rejected: Neimark-Sacker / Hopf behaviour in the minimal positive-coupling core

For the corrected continuous Jacobian

```text
[ -p  b ]
[  c -q ]
```

with `b,c >= 0`, the discriminant is

```text
(p-q)^2 + 4bc >= 0.
```

The local eigenvalues are real. A Hopf transition therefore cannot arise from this two-state positive-coupling core.

Oscillation would require an extension such as delay, more state variables, or signed interactions.

### 6.4 Rejected: timescale equation with reversed coupling direction

The deep-research draft multiplied a compression ratio by a factor that increased with the opposite capability. Because a smaller ratio means stronger compression, the proposed term had the intended causal direction backwards.

v0.1 instead evolves the distance above a positive physical floor:

```text
T_next - T_min
= (T - T_min) exp(-(eta + xi*S)).
```

Increasing the coupled capability now decreases the next transition interval while preserving the admissible floor domain.

### 6.5 Rejected: Evolutionary Reynolds Number

No momentum-diffusion mechanism analogous to kinematic viscosity has been established for CTC. A Reynolds-number label would therefore be decorative.

v0.1 uses a verification load ratio:

```text
Xi = verification demand / verification service capacity,
```

which has a direct queueing interpretation and can be measured in common units.

### 6.6 Deferred: strong global stability claims

Cooperativity and a candidate Lyapunov function do not automatically prove global convergence under the proposed nonlinear terms. v0.1 keeps the local stability result and boundedness barriers, and defers any global theorem until it is proved carefully.

### 6.7 Review correction: baseline compression is not coupled compression

Because `eta_A,eta_H>0` compress the model intervals even when `xi_HA=xi_AH=0`, observing `kappa<1` does not identify a coupled timescale effect. Strong CTC therefore requires an identified nonzero cross-timescale contribution beyond the baseline.

### 6.8 Review correction: threshold spacing and clock alignment

Unequal capability-threshold increments can manufacture shrinking crossing intervals under a constant underlying growth rate. Empirical telescoping must use equal increments or normalize time by threshold increment. AI and human threshold events are also asynchronous; fitting the mathematical recurrence requires an explicit calendar-time alignment rule.

### 6.9 Review correction: gamma estimands and human mediation

The ODE coefficients multiply `S_A(A)` and `S_H(H)` in per-capita growth equations. Raw capability contrasts therefore identify scaled effects, not `gamma` directly. In the reverse `H -> A` experiment, direct AI-assistant effects during successor development must be removed, equalised, or separated by a mediation design before the retained human-mediated effect can be labelled `gamma_HA`.

## 7. Most important empirical unknowns

### `gamma_HA`

Does an AI-induced, retained increase in human research capability cause a measurable increase in the capability growth of subsequent AI systems after direct assistant exposure is controlled?

This is the missing reverse capability edge in the loop.

### `xi_AH` and `xi_HA`

Does opposite-system capability causally compress the other system's transition interval beyond its baseline `eta` trend?

Without this attribution, the framework may observe telescoping and bidirectional capability coupling separately without establishing **coupled telescopic** coevolution.

### `T_H`, `kappa_H`, and normalized threshold times

Does AI assistance produce a durable reduction in the time required for humans or human teams to cross fixed epistemic-capability increments after threshold spacing is controlled?

This distinguishes a one-time productivity boost from human telescopic evolution.

## 8. Core research principle

The scientifically interesting outcome is not merely

```text
A increases.
```

It is evidence for a repeated causal chain:

```text
A_n -> H_(n+1) -> A_(n+1) -> H_(n+2)
```

with measurable capability coupling in both directions, cross-attributed timescale compression, explicit clock alignment, and verification capacity that can be independently monitored.
