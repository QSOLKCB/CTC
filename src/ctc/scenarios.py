"""Synthetic deterministic scenarios for exercising the CTC numerical reference.

These scenarios are fixtures, not forecasts, measurements, or parameter estimates.
"""

from __future__ import annotations

from dataclasses import asdict, replace
import hashlib
import json
from typing import Callable

from .diagnostics import find_interior_equilibrium, jacobian_terms, upper_barriers
from .model import CapabilityParameters, Parameters, SimulationConfig, State, TimescaleParameters, VerificationParameters, simulate

REFERENCE_FORMAT = "CTC-NUMERICAL-REFERENCE-v0.1"
REFERENCE_EPOCHS = 24


def base_parameters() -> Parameters:
    return Parameters(
        capability=CapabilityParameters(A_0=1.4, H_0=1.8, K_A=8.0, K_H=7.0, alpha_A=0.22, alpha_H=0.16, gamma_HA=0.0, gamma_AH=0.0),
        timescale=TimescaleParameters(T_A_min=2.0, T_H_min=3.0, eta_A=0.06, eta_H=0.045, xi_HA=0.0, xi_AH=0.0),
        verification=VerificationParameters(lambda_A=0.18, mu_H=0.32),
    )


def base_state() -> State:
    return State(A=1.0, H=1.0, T_A=12.0, T_H=18.0, B=0.0)


def _scenario_definitions() -> tuple[tuple[str, str, Callable[[Parameters], Parameters]], ...]:
    return (
        ("decoupled-growth", "Capability coupling disabled in both directions; only intrinsic capability dynamics remain.", lambda p: p),
        ("ai-assisted-humanity-only", "AI-to-human capability coupling enabled; human-to-AI capability coupling remains zero.", lambda p: replace(p, capability=replace(p.capability, gamma_AH=0.10, gamma_HA=0.0))),
        ("human-driven-ai-only", "Human-to-AI capability coupling enabled; AI-to-human capability coupling remains zero.", lambda p: replace(p, capability=replace(p.capability, gamma_HA=0.12, gamma_AH=0.0))),
        ("bidirectional-bounded-coevolution", "Both bounded capability-coupling directions enabled; cross-timescale coupling remains zero.", lambda p: replace(p, capability=replace(p.capability, gamma_HA=0.12, gamma_AH=0.10))),
        ("baseline-telescoping-no-cross-timescale", "Intervals compress from eta alone; xi_HA and xi_AH remain exactly zero.", lambda p: replace(p, capability=replace(p.capability, gamma_HA=0.12, gamma_AH=0.10), timescale=replace(p.timescale, eta_A=0.10, eta_H=0.08, xi_HA=0.0, xi_AH=0.0))),
        ("coupled-telescopic-coevolution", "Both capability and cross-timescale coupling coefficients are nonzero in this synthetic fixture.", lambda p: replace(p, capability=replace(p.capability, gamma_HA=0.12, gamma_AH=0.10), timescale=replace(p.timescale, xi_HA=0.08, xi_AH=0.07))),
        ("verification-limited-coevolution", "Synthetic bidirectional coupling with verification demand configured above service capacity.", lambda p: replace(p, capability=replace(p.capability, gamma_HA=0.12, gamma_AH=0.10), timescale=replace(p.timescale, xi_HA=0.08, xi_AH=0.07), verification=VerificationParameters(lambda_A=0.55, mu_H=0.12))),
    )


def _canon_float(value: float | None) -> str | None:
    if value is None:
        return None
    return format(float(value), ".12g")


def scenario_payload() -> dict[str, object]:
    config = SimulationConfig(delta_t=1.0, ode_substeps=32, t0=0.0)
    scenarios: list[dict[str, object]] = []
    for scenario_id, description, mutate in _scenario_definitions():
        params = mutate(base_parameters())
        records = simulate(base_state(), params, epochs=REFERENCE_EPOCHS, config=config)
        final = records[-1]
        eq = find_interior_equilibrium(
            A_0=params.capability.A_0, H_0=params.capability.H_0,
            K_A=params.capability.K_A, K_H=params.capability.K_H,
            alpha_A=params.capability.alpha_A, alpha_H=params.capability.alpha_H,
            gamma_HA=params.capability.gamma_HA, gamma_AH=params.capability.gamma_AH,
        )
        jt = jacobian_terms(
            equilibrium=eq, A_0=params.capability.A_0, H_0=params.capability.H_0,
            K_A=params.capability.K_A, K_H=params.capability.K_H,
            alpha_A=params.capability.alpha_A, alpha_H=params.capability.alpha_H,
            gamma_HA=params.capability.gamma_HA, gamma_AH=params.capability.gamma_AH,
        )
        barrier_A, barrier_H = upper_barriers(
            K_A=params.capability.K_A, K_H=params.capability.K_H,
            alpha_A=params.capability.alpha_A, alpha_H=params.capability.alpha_H,
            gamma_HA=params.capability.gamma_HA, gamma_AH=params.capability.gamma_AH,
        )
        scenarios.append({
            "id": scenario_id,
            "description": description,
            "classification": "SYNTHETIC_REFERENCE_FIXTURE",
            "forecast": False,
            "epochs": REFERENCE_EPOCHS,
            "delta_t": _canon_float(config.delta_t),
            "ode_substeps": config.ode_substeps,
            "parameters": {
                "capability": {k: _canon_float(v) for k, v in asdict(params.capability).items()},
                "timescale": {k: _canon_float(v) for k, v in asdict(params.timescale).items()},
                "verification": {k: _canon_float(v) for k, v in asdict(params.verification).items()},
            },
            "final": {
                "A": _canon_float(final.state.A), "H": _canon_float(final.state.H),
                "T_A": _canon_float(final.state.T_A), "T_H": _canon_float(final.state.T_H),
                "B": _canon_float(final.state.B), "Xi": _canon_float(final.Xi), "tau": _canon_float(final.tau),
            },
            "equilibrium_witness": {
                "A": _canon_float(eq.A), "H": _canon_float(eq.H),
                "A_barrier": _canon_float(barrier_A), "H_barrier": _canon_float(barrier_H),
                "trace": _canon_float(jt.trace), "determinant": _canon_float(jt.determinant),
                "discriminant": _canon_float(jt.discriminant), "stable": jt.stable,
                "eigenvalues": [_canon_float(x) for x in jt.eigenvalues],
            },
        })
    return {
        "format": REFERENCE_FORMAT,
        "forecast": False,
        "note": "Synthetic deterministic fixtures only; not empirical estimates or forecasts.",
        "scenarios": scenarios,
    }


def render_reference() -> str:
    return json.dumps(scenario_payload(), indent=2, sort_keys=True, ensure_ascii=True) + "\n"


def reference_sha256() -> str:
    return hashlib.sha256(render_reference().encode("utf-8")).hexdigest()
