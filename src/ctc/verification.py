"""Verification-load and backlog recurrence for CTC v0.1.0."""

from __future__ import annotations

import math


def _positive(name: str, value: float) -> float:
    value = float(value)
    if not math.isfinite(value) or value <= 0.0:
        raise ValueError(f"{name} must be finite and > 0")
    return value


def load_ratio(*, lambda_a: float, mu_h: float, A: float, H: float) -> float:
    lambda_a = _positive("lambda_a", lambda_a)
    mu_h = _positive("mu_h", mu_h)
    A = _positive("A", A)
    H = _positive("H", H)
    return (lambda_a * A) / (mu_h * H)


def backlog_next(*, B: float, lambda_a: float, mu_h: float, A: float, H: float) -> float:
    B = float(B)
    if not math.isfinite(B) or B < 0.0:
        raise ValueError("B must be finite and >= 0")
    lambda_a = _positive("lambda_a", lambda_a)
    mu_h = _positive("mu_h", mu_h)
    A = _positive("A", A)
    H = _positive("H", H)
    return max(0.0, B + lambda_a * A - mu_h * H)
