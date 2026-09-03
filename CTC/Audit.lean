import Lean.CoreM
import Lean.Environment
import Lean.Util.CollectAxioms

/-!
# CTC v0.1.0 theorem dependency audit

This executable loads the compiled `CTC.All` environment without executing imported
project initializers, verifies that every frozen CTC-MATH target is a theorem, and
checks its transitive axiom dependencies against the explicit classical trust base.
-/

open Lean

private def auditedTargets : Array Name := #[
  `CTC.saturation_pos,
  `CTC.saturation_lt_one,
  `CTC.geometric_compression_hasSum,
  `CTC.positive_floor_not_summable,
  `CTC.telescopic_floor_preserved,
  `CTC.telescopic_strict_compression,
  `CTC.telescopic_converges_to_floor,
  `CTC.verification_load_iff,
  `CTC.verification_backlog_nonincreasing,
  `CTC.jacobian_trace_negative,
  `CTC.jacobian_det_formula,
  `CTC.jacobian_discriminant_nonnegative,
  `CTC.local_stability_inequality,
  `CTC.saturation_strict_mono,
  `CTC.telescopic_iterate_antitone,
  `CTC.interior_equilibrium_exists
]

private def allowedAxioms : Array Name := #[
  `propext,
  `Classical.choice,
  `Quot.sound
]

private def auditTargets (env : Environment) : IO Unit :=
  Core.CoreM.toIO'
    (ctx := { fileName := "ctc-axiom-audit", fileMap := default })
    (s := { env }) do
      unless auditedTargets.size == 16 do
        throwError "CTC audit target table must contain exactly 16 declarations"

      for target in auditedTargets do
        let some info := (← getEnv).find? target
          | throwError "missing CTC audit declaration {target}"
        match info with
        | .thmInfo _ => pure ()
        | _ => throwError "CTC audit declaration {target} is not a theorem"

        let axioms ← Lean.collectAxioms target
        for ax in axioms do
          unless allowedAxioms.contains ax do
            throwError "{target} depends on disallowed foundational assumption {ax}"

        IO.println s!"audited theorem {target}"
        for ax in axioms do
          IO.println s!"  allowed dependency: {ax}"

unsafe def main : IO Unit := do
  Lean.withImportModules #[{ module := `CTC.All : Lean.Import }] {} fun env => do
    auditTargets env
    IO.println
      "CTC_AXIOM_AUDIT_COMPLETE targets=16 theorem_kinds=verified allowlist=verified project_initializers=not_executed"
