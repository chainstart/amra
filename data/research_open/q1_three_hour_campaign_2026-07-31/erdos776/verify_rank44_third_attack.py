#!/usr/bin/env python3
"""Independent exact guard for the third #776 rank-44 attack.

All unbounded-parameter implications are proved in THIRD_ATTACK.md.  The
finite rows below are identity regression, falsifier checks, or explicit
counterexamples to stronger proposed barriers.  They are never extrapolated.
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
    """Independent ordinary greedy Macaulay expansion."""
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


def choose(upper: int, lower: int) -> int:
    if lower < 0 or upper < lower:
        return 0
    return comb(upper, lower)


def moving_h(parameter: int, residual_rank: int) -> int:
    rank = residual_rank + 15
    return choose(parameter - 12, rank) + sum(
        choose(parameter - 28 + index, residual_rank + index)
        for index in range(1, 15)
    )


def algebraic_j44(parameter: int) -> int:
    return (
        comb(parameter - 12, 44)
        + sum(
            comb(parameter - 57 + lower, lower)
            for lower in range(31, 44)
        )
        + sum(
            comb(parameter - 58 + lower, lower)
            for lower in range(3, 31)
        )
    )


def ordinary_d44(parameter: int) -> int:
    rank = parameter - 12
    value = 0
    while rank > 44:
        value = parameter + kk(value, rank)
        rank -= 1
    return value


def compressed_d44(engine, parameter: int) -> tuple[int, list[tuple[int, int, int]]]:
    rank = parameter - 12
    runs = []
    while rank > 44:
        runs = engine.defect_step(runs, rank, parameter)
        rank -= 1
    return engine.runs_value(runs), runs


def rank44_complement_endpoint(parameter: int) -> tuple[int, int, int]:
    """Two-binomial-plus-one Galois descent for D44 < H44."""
    ambient = parameter - 11
    rank = parameter - 55
    value = (
        comb(parameter - 13, rank)
        + comb(parameter - 27, rank - 1)
        + 1
    )
    while rank > 2:
        value = kk(value + parameter, rank)
        rank -= 1
    target = comb(ambient, 2) - parameter
    return value, target, target - value


def inflated_tax_e31(parameter: int) -> tuple[int, int, int]:
    """Second complement at fixed rank 31."""
    transformed = parameter - 25
    rank = transformed - 1
    value = 0
    while rank > 31:
        value = parameter + kk(value, rank)
        rank -= 1
    target = (
        comb(transformed - 1, 31)
        + comb(transformed - 2, 30)
    )
    return value, target, target - value


def reverse_zero_test(parameter: int, start: int) -> dict[str, int | str]:
    rank = 44
    value = start
    while rank < parameter - 12:
        if value < parameter:
            return {
                "status": "FAIL",
                "rank": rank,
                "value": value,
            }
        value = upper_raise(value - parameter, rank)
        rank += 1
    return {
        "status": "END",
        "rank": rank,
        "value": value,
    }


def expected_rank44_template(
    parameter: int,
    residual: int,
) -> list[tuple[int, int]]:
    result = [(parameter - 12, 44)]
    result.extend(
        (parameter - 57 + lower, lower)
        for lower in range(43, 30, -1)
    )
    result.extend(
        (parameter - 58 + lower, lower)
        for lower in range(30, 2, -1)
    )
    result.extend(canonical(residual, 2))
    return result


def strict_subadditivity_regression() -> int:
    """Finite regression for the set-family lemma proved in the note."""
    checks = 0
    for rank in range(2, 9):
        for left in range(1, 81):
            for right in range(1, 81):
                assert (
                    kk(left + right, rank)
                    <= kk(left, rank) + kk(right, rank) - 1
                )
                checks += 1
    return checks


def adjacent_strict_subadditive_majorizer(parameter: int) -> int:
    """Best direct bound obtained by iterating the strict one-unit saving."""
    value = 1 + kk(parameter + 1, parameter - 12)
    for rank in range(parameter - 13, 44, -1):
        value = kk(value, rank)
    return value


def main() -> None:
    engine = load_engine()

    # The exact algebraic telescoping is independent of the observed chart.
    for parameter in [100, 128, 288, 379, 1_000, 10_000]:
        assert (
            moving_h(parameter, 29) - algebraic_j44(parameter)
            == comb(parameter - 55, 2)
        )
        rank = parameter - 55
        complement_start = (
            comb(parameter - 13, rank)
            + comb(parameter - 27, rank - 1)
            + 1
        )
        assert complement_start == (
            comb(parameter - 11, 44)
            - (moving_h(parameter, 29) - 1)
        )

    # Cross both truth values, so the Galois and second-complement checks are
    # not merely successful-side arithmetic.
    equivalence_rows = []
    for parameter in [100, 128, 288, 379]:
        direct = ordinary_d44(parameter)
        direct_margin = moving_h(parameter, 29) - direct
        c2, c2_target, c2_margin = rank44_complement_endpoint(parameter)
        e31, e31_target, e31_margin = inflated_tax_e31(parameter)
        assert (direct_margin > 0) == (c2 <= c2_target)
        assert (direct_margin > 0) == (e31 < e31_target)
        if direct_margin > 0:
            assert e31_margin == direct_margin
        equivalence_rows.append(
            {
                "V": parameter,
                "H44_minus_D44": direct_margin,
                "C2": c2,
                "C2_target": c2_target,
                "E31_target_minus_E31": e31_margin,
                "same_strict_sign": (
                    (direct_margin > 0)
                    == (c2 <= c2_target)
                    == (e31 < e31_target)
                ),
            }
        )

    # Selected stable-template rows are falsifier evidence only.
    template_rows = []
    for parameter in [288, 379, 1_000, 6_329, 10_000]:
        value, runs = compressed_d44(engine, parameter)
        residual = value - algebraic_j44(parameter)
        assert canonical(value, 44) == expected_rank44_template(
            parameter,
            residual,
        )
        assert residual < comb(parameter - 55, 2)
        template_rows.append(
            {
                "V": parameter,
                "R2_equals_D44_minus_J44": residual,
                "R2_canonical": canonical(residual, 2),
                "H44_minus_D44": (
                    comb(parameter - 55, 2) - residual
                ),
                "compressed_runs": runs,
            }
        )

    # A contiguous finite falsifier window.  It is deliberately recorded as
    # finite and does not carry any universal quantifier.
    finite_window = []
    values: dict[int, int] = {}
    for parameter in range(288, 502):
        value, _ = compressed_d44(engine, parameter)
        values[parameter] = value
        residual = value - algebraic_j44(parameter)
        margin = moving_h(parameter, 29) - value
        assert margin > 0
        assert residual <= 7 * parameter
        assert canonical(value, 44) == expected_rank44_template(
            parameter,
            residual,
        )
        if parameter <= 500:
            next_value = None
            finite_window.append(
                {
                    "V": parameter,
                    "H44_minus_D44": margin,
                    "R2": residual,
                    "placeholder_next": next_value,
                }
            )

    adjacent_rows = []
    for parameter in [288, 379, 500]:
        current_margin = (
            moving_h(parameter, 29) - values[parameter]
        )
        next_margin = (
            moving_h(parameter + 1, 29) - values[parameter + 1]
        )
        increment = next_margin - current_margin
        direct_delta = values[parameter + 1] - values[parameter]
        assert (
            moving_h(parameter, 28) - direct_delta
            == increment
        )
        assert increment > 0
        adjacent_rows.append(
            {
                "V": parameter,
                "margin_increment": increment,
                "H43_minus_D44_diagonal_increment": (
                    moving_h(parameter, 28) - direct_delta
                ),
            }
        )

    # The closest natural integer-linear tail barriers at the analytic
    # anchor: coefficient 6 is false, coefficient 7 is still only a
    # candidate outside this one exact row.
    anchor = 288
    anchor_d = values[anchor]
    anchor_j = algebraic_j44(anchor)
    anchor_residual = anchor_d - anchor_j
    assert anchor_residual == 1_970
    assert anchor_residual > 6 * anchor
    assert anchor_residual <= 7 * anchor
    six_reverse = reverse_zero_test(anchor, anchor_j + 6 * anchor)
    seven_reverse = reverse_zero_test(anchor, anchor_j + 7 * anchor)
    assert six_reverse == {
        "status": "FAIL",
        "rank": 275,
        "value": 287,
    }
    assert seven_reverse == {
        "status": "END",
        "rank": 276,
        "value": 0,
    }
    assert anchor_j + 7 * anchor < moving_h(anchor, 29)

    # A stronger almost-linear diagonal conjecture also has a strict exact
    # counterexample, even though monotonicity itself survives the row.
    diagonal_counterexample_parameter = 1_361
    d_1361, _ = compressed_d44(engine, diagonal_counterexample_parameter)
    d_1362, _ = compressed_d44(
        engine,
        diagonal_counterexample_parameter + 1,
    )
    f_1361 = (
        moving_h(diagonal_counterexample_parameter, 29) - d_1361
    )
    f_1362 = (
        moving_h(diagonal_counterexample_parameter + 1, 29) - d_1362
    )
    diagonal_increment = f_1362 - f_1361
    assert diagonal_increment == diagonal_counterexample_parameter - 58
    assert diagonal_increment < diagonal_counterexample_parameter - 57

    # Strict subadditivity is true, but its direct adjacent majorizer misses
    # the desired H43 cap by an enormous exact amount at V=288.
    strict_checks = strict_subadditivity_regression()
    adjacent_majorizer = adjacent_strict_subadditive_majorizer(anchor)
    h43_anchor = moving_h(anchor, 28)
    strict_majorizer_overshoot = adjacent_majorizer - h43_anchor
    assert adjacent_majorizer == (
        3_475_140_719_231_442_109_223_817_014_401_697_283_918_257_441_646_960
    )
    assert strict_majorizer_overshoot == (
        2_924_584_541_354_331_641_346_522_299_842_429_145_390_984_457_003_360
    )

    result = {
        "status": "PASS",
        "scope": "SYMBOLIC IDENTITY REGRESSION PLUS FINITE FALSIFIERS",
        "global_equivalences_checked_at_both_signs": equivalence_rows,
        "proved_symbolically_in_markdown": {
            "rank44_complement_start": (
                "C(V-13,V-55)+C(V-27,V-56)+1"
            ),
            "fixed_rank31_target": (
                "E31<C(V-26,31)+C(V-27,30)"
            ),
            "algebraic_tail_identity": (
                "H44-D44=C(V-55,2)-(D44-J44)"
            ),
            "adjacent_identity": (
                "F(V+1)-F(V)=H43(V)-"
                "(D44(V+1)-D44(V))"
            ),
        },
        "finite_template_rows_falsifier_only": template_rows,
        "finite_contiguous_window_falsifier_only": {
            "V_range": [288, 501],
            "minimum_margin": min(
                row["H44_minus_D44"] for row in finite_window
            ),
            "maximum_R2_over_V_numerator_denominator": max(
                (
                    row["R2"] / row["V"],
                    row["R2"],
                    row["V"],
                )
                for row in finite_window
            ),
        },
        "adjacent_rows_falsifier_only": adjacent_rows,
        "six_V_barrier_counterexample": {
            "V": anchor,
            "R2": anchor_residual,
            "6V": 6 * anchor,
            "reverse_certificate": six_reverse,
        },
        "seven_V_anchor_only": {
            "V": anchor,
            "R2": anchor_residual,
            "7V": 7 * anchor,
            "reverse_certificate": seven_reverse,
            "warning": "This one row is not an all-V theorem.",
        },
        "strong_diagonal_bound_counterexample": {
            "V": diagonal_counterexample_parameter,
            "actual_margin_increment": diagonal_increment,
            "false_proposed_lower_bound": (
                diagonal_counterexample_parameter - 57
            ),
        },
        "strict_subadditivity": {
            "finite_regression_checks": strict_checks,
            "V288_adjacent_majorizer": adjacent_majorizer,
            "V288_H43": h43_anchor,
            "overshoot": strict_majorizer_overshoot,
            "verdict": "TRUE LEMMA, FAR TOO COARSE FOR THE TARGET",
        },
        "open": [
            "D44<H44 for every V>=288",
            "D44<=J44+7V for every V>=288",
            "H44-D44 is nondecreasing for every V>=288",
            "the selected rank44 canonical template is uniform in V",
        ],
        "warning": (
            "No finite window, selected template row, or successful reverse "
            "anchor is extrapolated to unbounded V."
        ),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
