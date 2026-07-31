#!/usr/bin/env python3
"""Exact audit for the rank-16 linear gate in the Erdős #776 attack.

The finite evaluations in this file are regression/falsifier evidence.  The
all-parameter implication is the fixed-depth monotonicity argument recorded in
FINAL_REPORT.md.
"""

from __future__ import annotations

import importlib.util
import json
from math import comb
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
ENGINE_PATH = (
    ROOT
    / "artifacts"
    / "erdos_master_rotation"
    / "R002"
    / "core_776_635"
    / "776"
    / "verify_rank5_rotation.py"
)


def load_engine():
    spec = importlib.util.spec_from_file_location("r002_rank5", ENGINE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(ENGINE_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def canonical(number: int, rank: int) -> list[tuple[int, int]]:
    """Independent ordinary greedy combinadic expansion."""
    if number < 0 or rank < 1:
        raise ValueError((number, rank))
    result: list[tuple[int, int]] = []
    remaining = number
    cap: int | None = None
    for lower in range(rank, 0, -1):
        if remaining == 0:
            break
        low = lower - 1
        high = cap if cap is not None else max(2 * lower, lower + 1)
        if cap is None:
            while comb(high, lower) <= remaining:
                high *= 2
        while low + 1 < high:
            middle = (low + high) // 2
            if comb(middle, lower) <= remaining:
                low = middle
            else:
                high = middle
        upper = low if cap is None else min(low, cap - 1)
        while upper >= lower and comb(upper, lower) > remaining:
            upper -= 1
        if upper >= lower:
            result.append((upper, lower))
            remaining -= comb(upper, lower)
            cap = upper
    if remaining:
        raise AssertionError((number, rank, result, remaining))
    return result


def kk(number: int, rank: int) -> int:
    return sum(
        comb(upper, lower - 1)
        for upper, lower in canonical(number, rank)
    )


def ordinary_rank8_margin(parameter: int) -> int:
    rank = parameter - 12
    value = 0
    while rank > 8:
        value = parameter + kk(value, rank)
        rank -= 1
    return comb(parameter - 11, 8) - value


def state_at_rank(engine, parameter: int, target_rank: int):
    rank = parameter - 12
    runs = []
    while rank > target_rank:
        runs = engine.defect_step(runs, rank, parameter)
        rank -= 1
    return runs


def rank16_residual(engine, parameter: int) -> dict[str, object]:
    runs = state_at_rank(engine, parameter, 16)
    value = engine.runs_value(runs)
    prefix = comb(parameter - 12, 16) + comb(parameter - 13, 15)
    residual = value - prefix
    return {
        "V": parameter,
        "D16": value,
        "W14": residual,
        "linear_gate_margin": parameter - 1 - residual,
        "canonical_runs": runs,
    }


def actual_rank8_margin(engine, parameter: int) -> int:
    runs = state_at_rank(engine, parameter, 8)
    return comb(parameter - 11, 8) - engine.runs_value(runs)


def fixed_depth_coefficients() -> dict[int, int]:
    """If W_14<V, bound W_r<c_r V under W_(r-1)=V+KK_r(W_r)."""
    coefficients = {14: 1}
    coefficient = 1
    for rank in range(14, 6, -1):
        coefficient = 1 + rank * coefficient
        coefficients[rank - 1] = coefficient
    return coefficients


def main() -> None:
    engine = load_engine()
    coefficients = fixed_depth_coefficients()

    # For V>=175, C(V-13,r)/V is strictly increasing in V.  Hence these
    # eight integer checks certify c_r V<C(V-13,r) for every V>=175.
    analytic_base = 175
    base_margins = {
        rank: comb(analytic_base - 13, rank)
        - coefficient * analytic_base
        for rank, coefficient in coefficients.items()
    }
    assert all(margin > 0 for margin in base_margins.values())

    # Exact finite closure below the analytic gate.  This is a finite part of
    # the theorem, not evidence for the still-open rank-16 premise above it.
    finite_margins = {
        parameter: actual_rank8_margin(engine, parameter)
        for parameter in range(40, analytic_base)
    }
    independent_finite_margins = {
        parameter: ordinary_rank8_margin(parameter)
        for parameter in range(40, analytic_base)
    }
    assert independent_finite_margins == finite_margins
    assert min(finite_margins.values()) > 0

    # These selected values only try to falsify the proposed rank-16 premise.
    strategic_parameters = [175, 379, 1_000, 6_329, 10_000]
    strategic = [
        rank16_residual(engine, parameter)
        for parameter in strategic_parameters
    ]
    assert all(row["linear_gate_margin"] >= 0 for row in strategic)

    result = {
        "status": "PASS",
        "theorem_audited": (
            "For V>=175, D16<=C(V-12,16)+C(V-13,15)+V-1 "
            "implies D8<C(V-11,8)."
        ),
        "fixed_depth_coefficients": coefficients,
        "analytic_base_parameter": analytic_base,
        "base_binomial_separation_margins": base_margins,
        "finite_exact_range": [40, analytic_base - 1],
        "independent_ordinary_engine_agrees": True,
        "minimum_finite_rank8_margin": min(finite_margins.values()),
        "strategic_rank16_falsifier_checks": strategic,
        "open_statement": (
            "The rank-16 linear gate itself is not proved for every V>=175."
        ),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
