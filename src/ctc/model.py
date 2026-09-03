"""Deterministic numerical reference implementation of the frozen CTC v0.1.0 model."""

from __future__ import annotations

from dataclasses import dataclass
import math

from .saturation import saturation
from .timescale import next_interval, compression_ratio, timescale_ratio
from .verification import backlog_next, load_ratio


def _finite(name: str, value: float) -> float:
    value = float(value)
    if not math.isfinite(value):
        raise ValueError(f"{name} must be finite")
    return value


@dataclass(frozen=True)
class CapabilityParameters:
    A_0: float
    H_0: float
    K_A: float
    K_H: float
    alpha_A: float
    alpha_H: float
    gamma_HA: float
    gamma_AH: float

    def __post_init__(self) -> None:
        for name in ("A_0", "H_0", "K_A", "K_H", "alpha_A", "alpha_H"):
            value = _finite(name, getattr(self, name))
            if value <= 0.0:
                raise ValueError(f"{name} must be > 0")
            object.__setattr__(self, name, value)
        for name in ("gamma_HA", "gamma_AH"):
            value = _finite(name, getattr(self, name))
            if value < 0.0:
                raise ValueError(f"{name} must be >= 0")
            object.__setattr__(self, name, value)


@dataclass(frozen=True)
class TimescaleParameters:
    T_A_min: float
    T_H_min: float
    eta_A: float
    eta_H: float
    xi_HA: float
    xi_AH: float

    def __post_init__(self) -> None:
        for name in ("T_A_min", "T_H_min", "eta_A", "eta_H"):
            value = _finite(name, getattr(self, name))
            if value <= 0.0:
                raise ValueError(f"{name} must be > 0")
            object.__setattr__(self, name, value)
        for name in ("xi_HA", "xi_AH"):
            value = _finite(name, getattr(self, name))
            if value < 0.0:
                raise ValueError(f"{name} must be >= 0")
            object.__setattr__(self, name, value)


@dataclass(frozen=True)
class VerificationParameters:
    lambda_A: float
    mu_H: float

    def __post_init__(self) -> None:
        for name in ("lambda_A", "mu_H"):
            value = _finite(name, getattr(self, name))
            if value <= 0.0:
                raise ValueError(f"{name} must be > 0")
            object.__setattr__(self, name, value)


@dataclass(frozen=True)
class Parameters:
    capability: CapabilityParameters
    timescale: TimescaleParameters
    verification: VerificationParameters


@dataclass(frozen=True)
class State:
    A: float
    H: float
    T_A: float
    T_H: float
    B: float

    def validate(self, params: Parameters) -> "State":
        values = {name: _finite(name, getattr(self, name)) for name in ("A", "H", "T_A", "T_H", "B")}
        if values["A"] <= 0.0 or values["H"] <= 0.0:
            raise ValueError("A and H must be > 0")
        if values["T_A"] < params.timescale.T_A_min:
            raise ValueError("T_A must be >= T_A_min")
        if values["T_H"] < params.timescale.T_H_min:
            raise ValueError("T_H must be >= T_H_min")
        if values["B"] < 0.0:
            raise ValueError("B must be >= 0")
        return State(**values)


@dataclass(frozen=True)
class SimulationConfig:
    delta_t: float = 1.0
    ode_substeps: int = 16
    t0: float = 0.0

    def __post_init__(self) -> None:
        delta_t = _finite("delta_t", self.delta_t)
        t0 = _finite("t0", self.t0)
        if delta_t <= 0.0:
            raise ValueError("delta_t must be > 0")
        if not isinstance(self.ode_substeps, int) or isinstance(self.ode_substeps, bool):
            raise TypeError("ode_substeps must be an integer")
        if self.ode_substeps < 1:
            raise ValueError("ode_substeps must be >= 1")
        object.__setattr__(self, "delta_t", delta_t)
        object.__setattr__(self, "t0", t0)


@dataclass(frozen=True)
class EpochRecord:
    n: int
    t: float
    state: State
    S_A: float
    S_H: float
    Xi: float
    kappa_A: float | None
    kappa_H: float | None
    tau: float


def capability_derivative(A: float, H: float, p: CapabilityParameters) -> tuple[float, float]:
    if A <= 0.0 or H <= 0.0:
        raise ValueError("capability state must remain positive")
    S_A = saturation(p.A_0, A)
    S_H = saturation(p.H_0, H)
    dA = A * (p.alpha_A * (1.0 - A / p.K_A) + p.gamma_HA * S_H)
    dH = H * (p.alpha_H * (1.0 - H / p.K_H) + p.gamma_AH * S_A)
    return dA, dH


def _rk4_one(A: float, H: float, dt: float, p: CapabilityParameters) -> tuple[float, float]:
    a1, h1 = capability_derivative(A, H, p)
    a2, h2 = capability_derivative(A + 0.5 * dt * a1, H + 0.5 * dt * h1, p)
    a3, h3 = capability_derivative(A + 0.5 * dt * a2, H + 0.5 * dt * h2, p)
    a4, h4 = capability_derivative(A + dt * a3, H + dt * h3, p)
    A_next = A + (dt / 6.0) * (a1 + 2.0 * a2 + 2.0 * a3 + a4)
    H_next = H + (dt / 6.0) * (h1 + 2.0 * h2 + 2.0 * h3 + h4)
    if not math.isfinite(A_next) or not math.isfinite(H_next):
        raise ArithmeticError("capability integration produced a non-finite value")
    if A_next <= 0.0 or H_next <= 0.0:
        raise ArithmeticError("fixed-step RK4 left the positive domain; reduce delta_t or increase ode_substeps")
    return A_next, H_next


def integrate_capability_epoch(A: float, H: float, p: CapabilityParameters, config: SimulationConfig) -> tuple[float, float]:
    dt = config.delta_t / config.ode_substeps
    for _ in range(config.ode_substeps):
        A, H = _rk4_one(A, H, dt, p)
    return A, H


def advance_state(state: State, params: Parameters, config: SimulationConfig) -> State:
    """Advance exactly one common model epoch using A[n], H[n] for discrete updates."""
    state = state.validate(params)
    cap = params.capability
    timep = params.timescale
    verp = params.verification
    S_A = saturation(cap.A_0, state.A)
    S_H = saturation(cap.H_0, state.H)
    T_A_next = next_interval(current=state.T_A, floor=timep.T_A_min, eta=timep.eta_A, xi=timep.xi_HA, exposure=S_H)
    T_H_next = next_interval(current=state.T_H, floor=timep.T_H_min, eta=timep.eta_H, xi=timep.xi_AH, exposure=S_A)
    B_next = backlog_next(B=state.B, lambda_a=verp.lambda_A, mu_h=verp.mu_H, A=state.A, H=state.H)
    A_next, H_next = integrate_capability_epoch(state.A, state.H, cap, config)
    return State(A=A_next, H=H_next, T_A=T_A_next, T_H=T_H_next, B=B_next).validate(params)


def make_record(n: int, t: float, state: State, params: Parameters, nxt: State | None) -> EpochRecord:
    cap = params.capability
    verp = params.verification
    state = state.validate(params)
    kappa_A = None if nxt is None else compression_ratio(current=state.T_A, nxt=nxt.T_A)
    kappa_H = None if nxt is None else compression_ratio(current=state.T_H, nxt=nxt.T_H)
    return EpochRecord(
        n=n, t=t, state=state,
        S_A=saturation(cap.A_0, state.A), S_H=saturation(cap.H_0, state.H),
        Xi=load_ratio(lambda_a=verp.lambda_A, mu_h=verp.mu_H, A=state.A, H=state.H),
        kappa_A=kappa_A, kappa_H=kappa_H,
        tau=timescale_ratio(human=state.T_H, ai=state.T_A),
    )


def simulate(initial: State, params: Parameters, *, epochs: int, config: SimulationConfig = SimulationConfig()) -> tuple[EpochRecord, ...]:
    if not isinstance(epochs, int) or isinstance(epochs, bool):
        raise TypeError("epochs must be an integer")
    if epochs < 0:
        raise ValueError("epochs must be >= 0")
    current = initial.validate(params)
    records: list[EpochRecord] = []
    for n in range(epochs):
        nxt = advance_state(current, params, config)
        records.append(make_record(n, config.t0 + n * config.delta_t, current, params, nxt))
        current = nxt
    records.append(make_record(epochs, config.t0 + epochs * config.delta_t, current, params, None))
    return tuple(records)
