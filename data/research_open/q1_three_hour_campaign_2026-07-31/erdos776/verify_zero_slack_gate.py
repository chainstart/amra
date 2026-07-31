#!/usr/bin/env python3
"""Exact guard for the new #776 rank-18 zero-slack gate.

The all-parameter implication is proved symbolically in FIRST_ATTACK.md.
Finite computations here are regression/falsifier evidence only.
"""

from __future__ import annotations

import importlib.util
import json
from fractions import Fraction
from math import comb, factorial
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
    if number < 0 or rank < 1:
        raise ValueError((number, rank))
    result: list[tuple[int, int]] = []
    remaining = number
    cap: int | None = None
    for lower in range(rank, 0, -1):
        if remaining == 0:
            break
        low = lower - 1
        high = cap if cap is not None else max(lower + 1, 2 * lower)
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


def upper_raise(number: int, rank: int) -> int:
    return sum(
        comb(upper, lower + 1)
        for upper, lower in canonical(number, rank)
    )


def p(parameter: int, rank: int) -> int:
    return (
        comb(parameter - 12, rank)
        + comb(parameter - 13, rank - 1)
    )


def choose(upper: int, lower: int) -> int:
    """Binomial coefficient with the zero convention used in the proof."""
    if lower < 0 or upper < lower:
        return 0
    return comb(upper, lower)


def moving_h(parameter: int, residual_rank: int) -> int:
    rank = residual_rank + 15
    return choose(parameter - 12, rank) + sum(
        choose(
            parameter - 28 + index,
            residual_rank + index,
        )
        for index in range(1, 15)
    )


def state_at_rank(engine, parameter: int, target_rank: int):
    rank = parameter - 12
    runs = []
    while rank > target_rank:
        runs = engine.defect_step(runs, rank, parameter)
        rank -= 1
    return runs


def actual_rank8_margin(engine, parameter: int) -> int:
    runs = state_at_rank(engine, parameter, 8)
    return comb(parameter - 11, 8) - engine.runs_value(runs)


def actual_rank18_slack(engine, parameter: int) -> int:
    runs = state_at_rank(engine, parameter, 18)
    return p(parameter, 18) - engine.runs_value(runs)


def first_moving_entry(engine, parameter: int) -> dict[str, int]:
    rank = parameter - 12
    runs = []
    while rank >= 18:
        value = engine.runs_value(runs)
        residual_rank = rank - 15
        baseline = moving_h(parameter, residual_rank)
        if value >= baseline:
            excess = value - baseline
            assert 0 <= excess <= parameter
            return {
                "V": parameter,
                "rank": rank,
                "s": residual_rank,
                "entry_excess": excess,
            }
        if rank == 18:
            break
        runs = engine.defect_step(runs, rank, parameter)
        rank -= 1
    raise AssertionError(("no entry through rank 18", parameter))


def complement_endpoint(parameter: int) -> int:
    """Run the globally audited one-binomial complementary descent."""
    rank = parameter - 29
    value = comb(parameter - 13, rank)
    while rank > 2:
        value = kk(value + parameter, rank)
        rank -= 1
    return value


def transformed_rank5_margin(engine, parameter: int) -> int:
    """Margin in the second-complement fixed-rank-five formulation."""
    transformed_parameter = parameter - 25
    rank = transformed_parameter - 1
    runs = []
    while rank > 5:
        runs = engine.defect_step(runs, rank, parameter)
        rank -= 1
    return comb(transformed_parameter, 5) - engine.runs_value(runs)


def entry_coefficients(entry_rank: int) -> dict[int, int]:
    result = {entry_rank: 1}
    value = 1
    for rank in range(entry_rank, 3, -1):
        value = 1 + rank * value
        result[rank - 1] = value
    return result


def factorial_entry_gate(parameter: int, entry_rank: int) -> bool:
    reservoir_top = parameter - 27
    return (
        2 * entry_rank <= reservoir_top
        and parameter * factorial(entry_rank + 1)
        < 24 * comb(reservoir_top, 3)
    )


def exact_entry_bootstrap(parameter: int, entry_rank: int) -> int:
    """Synthetic regression for the proved conditional entry theorem."""
    assert factorial_entry_gate(parameter, entry_rank)
    return exact_separated_descent(parameter, entry_rank)


def exact_separated_descent(parameter: int, entry_rank: int) -> int:
    """Descend the worst synthetic entry Z_s=V and check every reservoir."""
    reservoir_top = parameter - 27
    value = parameter
    for rank in range(entry_rank, 2, -1):
        assert value < comb(reservoir_top, rank)
        if rank > 3:
            value = parameter + kk(value, rank)
    assert value < comb(reservoir_top, 3)
    return value


def ceiling_fraction(value: Fraction) -> int:
    return (
        value.numerator + value.denominator - 1
    ) // value.denominator


def subadditive_entry_certificate() -> dict[str, object]:
    """Exact 26-constant certificate for the uniform s<=28 gate."""
    base = 288
    constants: dict[int, Fraction] = {28: Fraction(1)}
    transition_rows = []
    for rank in range(28, 3, -1):
        current = constants[rank]
        block = ceiling_fraction(current * base)
        shadow = kk(block, rank)
        next_constant = Fraction(1) + Fraction(2 * shadow, base)
        constants[rank - 1] = next_constant
        transition_rows.append(
            {
                "r": rank,
                "K_r": str(current),
                "M_r": block,
                "KK_r_M_r": shadow,
                "K_next": str(next_constant),
            }
        )

    separation_rows = []
    for rank in range(3, 29):
        scaled = ceiling_fraction(constants[rank] * base)
        reservoir = comb(base - 27, rank)
        assert scaled < reservoir
        separation_rows.append(
            {
                "r": rank,
                "K_r": str(constants[rank]),
                "ceil_288_K_r": scaled,
                "base_reservoir": reservoir,
                "base_margin": reservoir - scaled,
            }
        )

    assert constants[3] == Fraction(58_691, 48)
    assert min(
        row["base_margin"] for row in separation_rows
    ) == 2_577_144
    return {
        "base": base,
        "K3": str(constants[3]),
        "minimum_base_separation_margin": min(
            row["base_margin"] for row in separation_rows
        ),
        "transition_rows": transition_rows,
        "separation_rows": separation_rows,
    }


def largest_factorial_entry_rank(parameter: int) -> int:
    rank = 3
    last = 2
    while factorial_entry_gate(parameter, rank):
        last = rank
        rank += 1
    return last


def coefficients(initial: int) -> dict[int, int]:
    result = {14: initial}
    value = initial
    for rank in range(14, 6, -1):
        value = 1 + rank * value
        result[rank - 1] = value
    return result


def zero_slack_majorizer(parameter: int) -> dict[str, int]:
    """Descend the hypothesis endpoint P18 through ranks 17 and 16."""
    majorizer18 = p(parameter, 18)
    majorizer17 = parameter + kk(majorizer18, 18)
    majorizer16 = parameter + kk(majorizer17, 17)
    residual16 = majorizer16 - p(parameter, 16)
    expected = parameter + kk(parameter, 15)
    assert majorizer17 == p(parameter, 17) + parameter
    assert majorizer16 == p(parameter, 16) + expected
    assert residual16 == expected
    assert residual16 <= 16 * parameter
    return {
        "V": parameter,
        "rank16_residual": residual16,
        "sixteen_V_margin": 16 * parameter - residual16,
    }


def check_g2_endpoint_identity(parameter: int) -> None:
    """Check the symbolic final-step threshold at adjacent V,V+1."""
    t_v = comb(parameter - 11, 2) - parameter
    s2_t = t_v + upper_raise(t_v, 2)
    threshold = s2_t - (parameter + 1)
    closed = (
        comb(parameter - 12, 3)
        + comb(parameter - 26, 2)
        + parameter
        - 52
    )
    assert threshold == closed

    next_parameter = parameter + 1
    same_in_next_notation = (
        comb(next_parameter - 13, 3)
        + comb(next_parameter - 27, 2)
        + next_parameter
        - 53
    )
    assert threshold == same_in_next_notation


def main() -> None:
    engine = load_engine()

    analytic_base = 288
    fixed_coefficients = coefficients(16)
    base_margins = {
        rank: comb(analytic_base - 13, rank)
        - coefficient * analytic_base
        for rank, coefficient in fixed_coefficients.items()
    }
    assert all(margin > 0 for margin in base_margins.values())

    # Exact finite bridge.  It is a finite part of the conditional theorem,
    # not evidence for the open zero-slack premise beyond the checked range.
    finite_margins = {
        parameter: actual_rank8_margin(engine, parameter)
        for parameter in range(40, analytic_base)
    }
    assert min(finite_margins.values()) > 0

    strategic_parameters = [288, 379, 1_000, 6_329, 10_000]
    majorizer_rows = [
        zero_slack_majorizer(parameter)
        for parameter in strategic_parameters
    ]

    # Falsifier checks for the open premise only.
    slack_parameters = [40, 69, 70, 100, 175, 288, 379, 1_000, 6_329]
    slack_rows = [
        {
            "V": parameter,
            "P18_minus_actual_D18": actual_rank18_slack(
                engine, parameter
            ),
        }
        for parameter in slack_parameters
    ]
    assert slack_rows[0]["P18_minus_actual_D18"] < 0
    assert all(
        row["P18_minus_actual_D18"] >= 0
        for row in slack_rows
        if row["V"] >= 69
    )

    for parameter in [70, 100, 175, 288, 379, 1_000]:
        check_g2_endpoint_identity(parameter)

    # Algebraic identities in the second attack.  These loops are
    # regression checks for the displayed proofs, not finite extrapolation.
    for parameter in [40, 70, 100, 288, 379]:
        for residual_rank in range(3, parameter - 26):
            rank = residual_rank + 15
            assert (
                p(parameter, rank)
                - moving_h(parameter, residual_rank)
                == comb(parameter - 27, residual_rank)
            )

    entry_rows = [
        first_moving_entry(engine, parameter)
        for parameter in [40, 69, 70, 100, 175, 288, 379, 1_000]
    ]

    # The complementary endpoint is exactly one below its target at these
    # selected parameters.  In particular V=288 is a genuine counterexample
    # to the stronger universal proposal C2<=T-2.
    complement_rows = []
    for parameter in [70, 100, 175, 288, 379, 1_000]:
        target = comb(parameter - 11, 2) - parameter
        endpoint = complement_endpoint(parameter)
        assert endpoint == target - 1
        complement_rows.append(
            {
                "V": parameter,
                "C2": endpoint,
                "T": target,
                "T_minus_C2": target - endpoint,
            }
        )

    # The second complement is a global sign equivalence.  Equality of the
    # two margins is asserted only on the successful side.
    second_complement_rows = []
    for parameter in [
        40,
        41,
        42,
        43,
        44,
        50,
        69,
        70,
        100,
        175,
        288,
        379,
    ]:
        rank18_margin = actual_rank18_slack(engine, parameter)
        rank5_margin = transformed_rank5_margin(engine, parameter)
        assert (rank18_margin >= 0) == (rank5_margin >= 0)
        if rank18_margin >= 0:
            assert rank18_margin == rank5_margin
        second_complement_rows.append(
            {
                "V": parameter,
                "rank18_margin": rank18_margin,
                "transformed_rank5_margin": rank5_margin,
                "same_sign": (
                    (rank18_margin >= 0) == (rank5_margin >= 0)
                ),
            }
        )

    synthetic_entry_cases = [(288, 7), (1_000, 9), (1_000_000, 14)]
    entry_gate_rows = []
    for parameter, entry_rank in synthetic_entry_cases:
        coefficient_rows = entry_coefficients(entry_rank)
        assert coefficient_rows[3] <= factorial(entry_rank + 1) // 24
        final_residual = exact_entry_bootstrap(parameter, entry_rank)
        entry_gate_rows.append(
            {
                "V": parameter,
                "s": entry_rank,
                "B3": coefficient_rows[3],
                "factorial_B3_upper": (
                    factorial(entry_rank + 1) // 24
                ),
                "synthetic_Z3": final_residual,
                "rank3_reservoir": comb(parameter - 27, 3),
            }
        )

    factorial_scale_rows = [
        {
            "V": parameter,
            "largest_s_passing_displayed_factorial_gate": (
                largest_factorial_entry_rank(parameter)
            ),
        }
        for parameter in [288, 1_000, 10**6, 10**12, 10**30]
    ]

    subadditive_certificate = subadditive_entry_certificate()
    fixed_rank_28_rows = []
    for parameter in [288, 379, 1_000, 10_000]:
        final_residual = exact_separated_descent(parameter, 28)
        fixed_rank_28_rows.append(
            {
                "V": parameter,
                "synthetic_entry_s": 28,
                "synthetic_Z3": final_residual,
                "rank3_reservoir": comb(parameter - 27, 3),
            }
        )

    rank44_rows = []
    for parameter in [288, 379, 1_000, 6_329, 10_000]:
        rank44_value = engine.runs_value(
            state_at_rank(engine, parameter, 44)
        )
        margin = moving_h(parameter, 29) - rank44_value
        assert margin > 0
        rank44_rows.append(
            {
                "V": parameter,
                "H44_minus_D44": margin,
            }
        )

    result = {
        "status": "PASS",
        "scope": "FINITE GUARD PLUS SYMBOLIC-IDENTITY REGRESSION",
        "proved_in_markdown": (
            "For V>=288, D18<=P18 implies D8<C(V-11,8)."
        ),
        "open_premise": "D18<=P18 for every V>=288.",
        "analytic_base": analytic_base,
        "fixed_depth_coefficients": fixed_coefficients,
        "base_separation_margins": base_margins,
        "finite_bridge": [40, analytic_base - 1],
        "minimum_finite_rank8_margin": min(finite_margins.values()),
        "strategic_majorizer_rows": majorizer_rows,
        "zero_slack_falsifier_rows": slack_rows,
        "g2_endpoint_identity_parameters": [
            70,
            100,
            175,
            288,
            379,
            1_000,
        ],
        "second_attack": {
            "global_complement_audit": "PASS",
            "moving_block_identity": "PASS",
            "first_entry_rows_falsifier_only": entry_rows,
            "one_binomial_endpoint_rows_falsifier_only": complement_rows,
            "stronger_T_minus_2_claim": (
                "FALSE: V=288 has C2=T-1."
            ),
            "second_complement_rows_falsifier_only": (
                second_complement_rows
            ),
            "proved_conditional_entry_gate_regressions": entry_gate_rows,
            "factorial_scale_rows": factorial_scale_rows,
            "subadditive_rank28_certificate": (
                subadditive_certificate
            ),
            "fixed_rank28_gate_regressions": fixed_rank_28_rows,
            "rank44_target_rows_falsifier_only": rank44_rows,
            "new_equivalent_open_target": (
                "For N=V-25, E_(N-1)=0 and "
                "E_(q-1)=V+KK_q(E_q) imply E5<=C(N,5)."
            ),
        },
        "warning": (
            "The selected zero-slack rows do not prove the open premise "
            "for unbounded V.  Entry rows and endpoint rows are "
            "falsifier/regression evidence only."
        ),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
