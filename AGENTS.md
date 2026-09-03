# AGENTS.md

Machine-agent instructions for `QSOLKCB/CTC`.

## Purpose

Preserve the distinction between mathematical truth, empirical evidence, estimation, and speculation while evolving the Coupled Telescopic Coevolution framework.

## Hard rules

1. **Do not upgrade evidence classes.** A `FORMAL` theorem does not establish an `OBSERVED`, `ESTIMATED`, or `CAUSAL` fact about real human or AI systems.
2. **Do not encode empirical claims as axioms.** Real-world signs or values of `gamma_AH`, `gamma_HA`, `kappa_A`, `kappa_H`, `Xi`, capability indices, or singularity dates must remain external measurements or explicit hypotheses.
3. **Do not infer the full loop from one edge.** Evidence for `AI -> Human` does not establish `Human -> AI`, and evidence for either edge alone does not establish self-acceleration.
4. **Do not equate productivity with learning.** Shorter task completion time is not durable epistemic-capability growth unless retention or later unaided capability is measured.
5. **Do not equate product releases with capability generations.** `T_A` and `T_H` require fixed, reproducible transition criteria.
6. **Do not claim a physical singularity from a convergent time series.** `sum T_n < infinity` is a mathematical property of a chosen recurrence, not proof of an infinite physical supertask or unbounded capability.
7. **Keep the v0.1 coupling bounded.** The canonical saturation functions are `A/(A_0+A)` and `H/(H_0+H)`. `log(1+x)` must not be described as saturating.
8. **Preserve the corrected stability invariant.** For the minimal continuous positive-coupling Jacobian `[[ -p, b ], [ c, -q ]]`, the local stability condition is `bc < pq`, with `p,q>0` and `b,c>=0`.
9. **Preserve the real-eigenvalue invariant.** The discriminant `(p-q)^2 + 4bc` is nonnegative for `b,c>=0`. Do not introduce a Hopf/Neimark-Sacker claim into the two-state positive-coupling core.
10. **Keep capability, timescale, and verification dynamics separate.** Do not collapse `A/H`, `T_A/T_H`, and `B/Xi` into one scalar without a documented model extension.
11. **Verification load is a queue/load ratio, not a Reynolds number.** Do not restore an `Evolutionary Reynolds Number` unless a genuine force/diffusion derivation is supplied and reviewed.
12. **Physical floors stay positive.** The canonical telescopic-time recurrence converges toward `T_min > 0`; it must not silently revert to a zero-time limit.
13. **No theorem placeholders in trusted formal sources.** Lean project theorem files must contain no `sorry`, `admit`, or project-defined `axiom` declarations.
14. **Review source provenance, not declaration names alone.** Future formal-audit workflows must authenticate reviewed theorem sources and must not trust prebuilt objects merely because expected declaration names exist.

## Canonical contract files

Treat these as normative for v0.1:

- `docs/MATHEMATICAL-CORE-v0.1.md`
- `docs/EMPIRICAL-CONTRACT.md`
- `spec/ctc-core-v0.1.yaml`
- `docs/FORMALIZATION-PLAN.md`

If these disagree, stop and resolve the disagreement explicitly before implementation.

## Evidence labels

Use only these labels unless the contract is deliberately versioned:

- `OBSERVED`
- `ESTIMATED`
- `CAUSAL`
- `FORMAL`
- `HYPOTHESIS`
- `SPECULATIVE`

## Change discipline

Any change to a core equation, variable meaning, stability condition, or falsification criterion must:

1. identify the prior invariant being changed;
2. explain the mathematical or empirical reason;
3. update the human-readable contract and `spec/ctc-core-v0.1.yaml` together;
4. update or add formal proofs and deterministic tests when they exist;
5. avoid retroactively changing the meaning of an already released version.

## Formalisation order

Follow `docs/FORMALIZATION-PLAN.md`. Prefer elementary, inspectable results before advanced dynamical-systems machinery.

## Agent completion rule

Before declaring a CTC task complete, check:

- equations match the canonical contract;
- directional subscripts `AH` and `HA` have not been swapped;
- no empirical assumption has been silently promoted to fact;
- new claims have an evidence label;
- formal claims have proof or remain explicitly planned;
- counterexamples and falsification paths remain representable.
