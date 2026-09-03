"""Deterministic numerical reference implementation of the frozen CTC v0.1.0 model."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
import math

from .saturation import saturation_approx
from .timescale import next_interval, compression_ratio, timescale_ratio
from .verification import backlog_next, load_ratio


def _finite(name: str, value: float) -> float:
    value = float(value)
    if not math.isfinite(value):
        raise ValueError(f"{name} must be finite")
    return value


def _fraction(value: float) -> Fraction:
    return Fraction.from_float(float(value))


def _runtime_float(name: str, value: Fraction) -> float:
    """Convert an exact binary64-input expression without hiding over/underflow."""
    try:
        result = float(value)
    except OverflowError as exc:
        raise ArithmeticError(f"{name} is outside the finite binary64 range") from exc
    if not math.isfinite(result):
        raise ArithmeticError(f"{name} is outside the finite binary64 range")
    if result == 0.0 and value != 0:
        raise ArithmeticError(f"{name} is nonzero but below binary64 resolution")
    return result


def _epoch_time(config: "SimulationConfig", n: int) -> float:
    exact = _fraction(config.t0) + n * _fraction(config.delta_t)
    return _runtime_float("model epoch timestamp", exact)


def _epoch_times(config: "SimulationConfig", epochs: int) -> tuple[float, ...]:
    """Return all declared model-clock epochs, rejecting collapsed float times."""
    times: list[float] = []
    previous: float | None = None
    for n in range(epochs + 1):
        current = _epoch_time(config, n)
        if previous is not None and current <= previous:
            raise ArithmeticError(
                "distinct model epochs are not representable as distinct increasing binary64 timestamps"
            )
        times.append(current)
        previous = current
    return tuple(times)


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


def _intrinsic_growth(*, state: float, alpha: float, K: float) -> Fraction:
    """Evaluate alpha*(1-state/K) without overflowing state/K."""
    return _fraction(alpha) - _fraction(alpha) * _fraction(state) / _fraction(K)


def _coupling_growth(*, gamma: float, reference: float, value: float) -> Fraction:
    """Evaluate gamma*value/(reference+value) before any saturation rounding."""
    if gamma == 0.0:
        return Fraction(0, 1)
    return _fraction(gamma) * _fraction(value) / (_fraction(reference) + _fraction(value))


def _capability_barrier_exact(*, K: float, alpha: float, gamma: float) -> Fraction:
    """Return K*(1+gamma/alpha) exactly from binary64 inputs."""
    return _fraction(K) + _fraction(K) * _fraction(gamma) / _fraction(alpha)


def _capability_derivative_exact(
    A: float, H: float, p: CapabilityParameters
) -> tuple[Fraction, Fraction]:
    """Return exact derivatives of the accepted binary64 state."""
    A = _finite("A", A)
    H = _finite("H", H)
    if A <= 0.0 or H <= 0.0:
        raise ValueError("capability state must remain positive")

    growth_A = _intrinsic_growth(state=A, alpha=p.alpha_A, K=p.K_A) + _coupling_growth(
        gamma=p.gamma_HA, reference=p.H_0, value=H
    )
    growth_H = _intrinsic_growth(state=H, alpha=p.alpha_H, K=p.K_H) + _coupling_growth(
        gamma=p.gamma_AH, reference=p.A_0, value=A
    )
    return _fraction(A) * growth_A, _fraction(H) * growth_H


def capability_derivative(A: float, H: float, p: CapabilityParameters) -> tuple[float, float]:
    dA_exact, dH_exact = _capability_derivative_exact(A, H, p)
    return _runtime_float("AI capability derivative", dA_exact), _runtime_float(
        "human capability derivative", dH_exact
    )


def _rk4_stage(base: float, dt: Fraction, derivative: Fraction, factor: Fraction, name: str) -> float:
    exact = _fraction(base) + factor * dt * derivative
    if exact <= 0:
        raise ArithmeticError("fixed-step RK4 left the positive domain; reduce delta_t or increase ode_substeps")
    return _runtime_float(name, exact)


def _rk4_finish(
    base: float,
    dt: Fraction,
    stages: tuple[Fraction, Fraction, Fraction, Fraction],
    name: str,
) -> float:
    weighted = stages[0] + 2 * stages[1] + 2 * stages[2] + stages[3]
    exact = _fraction(base) + dt * weighted / 6
    if exact <= 0:
        raise ArithmeticError("fixed-step RK4 left the positive domain; reduce delta_t or increase ode_substeps")
    result = _runtime_float(name, exact)
    if result == base and exact != _fraction(base):
        raise ArithmeticError(
            "nonzero RK4 substep motion is not representable in binary64; reduce ode_substeps or increase epoch width"
        )
    return result


def _rk4_one(A: float, H: float, dt: Fraction, p: CapabilityParameters) -> tuple[float, float]:
    a1, h1 = _capability_derivative_exact(A, H, p)
    A2 = _rk4_stage(A, dt, a1, Fraction(1, 2), "RK4 AI stage 2")
    H2 = _rk4_stage(H, dt, h1, Fraction(1, 2), "RK4 human stage 2")
    a2, h2 = _capability_derivative_exact(A2, H2, p)
    A3 = _rk4_stage(A, dt, a2, Fraction(1, 2), "RK4 AI stage 3")
    H3 = _rk4_stage(H, dt, h2, Fraction(1, 2), "RK4 human stage 3")
    a3, h3 = _capability_derivative_exact(A3, H3, p)
    A4 = _rk4_stage(A, dt, a3, Fraction(1, 1), "RK4 AI stage 4")
    H4 = _rk4_stage(H, dt, h3, Fraction(1, 1), "RK4 human stage 4")
    a4, h4 = _capability_derivative_exact(A4, H4, p)
    A_next = _rk4_finish(A, dt, (a1, a2, a3, a4), "RK4 AI result")
    H_next = _rk4_finish(H, dt, (h1, h2, h3, h4), "RK4 human result")
    return A_next, H_next


def _reject_upward_barrier_crossing(
    *, before: float, after: float, barrier: Fraction, name: str
) -> None:
    """Reject a numerical step that crosses a forward upper barrier from below."""
    f_before = _fraction(before)
    f_after = _fraction(after)
    if f_before <= barrier and f_after > barrier:
        raise ArithmeticError(
            f"{name} RK4 substep crossed the canonical upper barrier; reduce delta_t or increase ode_substeps"
        )


def integrate_capability_epoch(A: float, H: float, p: CapabilityParameters, config: SimulationConfig) -> tuple[float, float]:
    dt_exact = _fraction(config.delta_t) / config.ode_substeps
    if dt_exact <= 0:
        raise ArithmeticError("RK4 substep width must remain positive")

    A_barrier = _capability_barrier_exact(K=p.K_A, alpha=p.alpha_A, gamma=p.gamma_HA)
    H_barrier = _capability_barrier_exact(K=p.K_H, alpha=p.alpha_H, gamma=p.gamma_AH)
    for _ in range(config.ode_substeps):
        A_before, H_before = A, H
        A, H = _rk4_one(A, H, dt_exact, p)
        _reject_upward_barrier_crossing(before=A_before, after=A, barrier=A_barrier, name="AI capability")
        _reject_upward_barrier_crossing(before=H_before, after=H, barrier=H_barrier, name="human capability")
    return A, H


def advance_state(state: State, params: Parameters, config: SimulationConfig) -> State:
    """Advance exactly one common model epoch using A[n], H[n] for discrete updates."""
    state = state.validate(params)
    cap = params.capability
    timep = params.timescale
    verp = params.verification
    S_A = 0.0 if timep.xi_AH == 0.0 else saturation_approx(cap.A_0, state.A)
    S_H = 0.0 if timep.xi_HA == 0.0 else saturation_approx(cap.H_0, state.H)
    T_A_next = next_interval(current=state.T_A, floor=timep.T_A_min, eta=timep.eta_A, xi=timep.xi_HA, exposure=S_H)
    T_H_next = next_interval(current=state.T_H, floor=timep.T_H_min, eta=timep.eta_H, xi=timep.xi_AH, exposure=S_A)
    B_next = backlog_next(B=state.B, lambda_a=verp.lambda_A, mu_h=verp.mu_H, A=state.A, H=state.H)
    A_next, H_next = integrate_capability_epoch(state.A, state.H, cap, config)
    return State(A=A_next, H=H_next, T_A=T_A_next, T_H=T_H_next, B=B_next).validate(params)


def make_record(n: int, t: float, state: State, params: Parameters, nxt: State | None) -> EpochRecord:
    cap = params.capability
    verp = params.verification
    t = _finite("t", t)
    state = state.validate(params)
    kappa_A = None if nxt is None else compression_ratio(current=state.T_A, nxt=nxt.T_A)
    kappa_H = None if nxt is None else compression_ratio(current=state.T_H, nxt=nxt.T_H)
    return EpochRecord(
        n=n, t=t, state=state,
        S_A=saturation_approx(cap.A_0, state.A), S_H=saturation_approx(cap.H_0, state.H),
        Xi=load_ratio(lambda_a=verp.lambda_A, mu_h=verp.mu_H, A=state.A, H=state.H),
        kappa_A=kappa_A, kappa_H=kappa_H,
        tau=timescale_ratio(human=state.T_H, ai=state.T_A),
    )


def simulate(initial: State, params: Parameters, *, epochs: int, config: SimulationConfig = SimulationConfig()) -> tuple[EpochRecord, ...]:
    if not isinstance(epochs, int) or isinstance(epochs, bool):
        raise TypeError("epochs must be an integer")
    if epochs < 0:
        raise ValueError("epochs must be >= 0")

    epoch_times = _epoch_times(config, epochs)

    current = initial.validate(params)
    records: list[EpochRecord] = []
    for n in range(epochs):
        nxt = advance_state(current, params, config)
        records.append(make_record(n, epoch_times[n], current, params, nxt))
        current = nxt
    records.append(make_record(epochs, epoch_times[epochs], current, params, None))
    return tuple(records)
