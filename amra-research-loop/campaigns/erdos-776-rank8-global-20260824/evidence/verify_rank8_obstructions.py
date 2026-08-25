#!/usr/bin/env python3
"""Exact obstruction guards for the Erdős #776 rank-8 campaign.

The canonical-run evaluator is independent of the old campaign scripts.  All
bounded scans are falsifiers only.  Algebraic identities and displayed exact
counterexamples have the scope stated in RANK8_OBSTRUCTION_ANALYSIS.md.
"""

from __future__ import annotations

from hashlib import sha256
from math import ceil, comb, log2
from pathlib import Path
import json


Run = tuple[int, int, int]


def canonical(number: int, rank: int) -> list[tuple[int, int]]:
    if number < 0 or rank < 1:
        raise ValueError((number, rank))
    result: list[tuple[int, int]] = []
    remainder = number
    cap: int | None = None
    for lower in range(rank, 0, -1):
        if remainder == 0:
            break
        lo = lower - 1
        hi = cap if cap is not None else max(lower + 1, 2 * lower)
        if cap is None:
            while comb(hi, lower) <= remainder:
                hi *= 2
        while lo + 1 < hi:
            middle = (lo + hi) // 2
            if comb(middle, lower) <= remainder:
                lo = middle
            else:
                hi = middle
        upper = lo if cap is None else min(lo, cap - 1)
        while upper >= lower and comb(upper, lower) > remainder:
            upper -= 1
        if upper >= lower:
            result.append((upper, lower))
            remainder -= comb(upper, lower)
            cap = upper
    if remainder:
        raise AssertionError((number, rank, remainder, result))
    return result


def kk(number: int, rank: int) -> int:
    return sum(comb(upper, lower - 1) for upper, lower in canonical(number, rank))


def canonical_runs(number: int, rank: int) -> list[Run]:
    remainder = number
    lower = rank
    offset_cap: int | None = None
    runs: list[Run] = []
    while remainder:
        if lower < 1:
            raise AssertionError((number, rank, remainder, runs))
        if offset_cap is None:
            hi = 1
            while comb(lower + hi, hi) <= remainder:
                hi *= 2
        else:
            hi = offset_cap + 1
        lo = -1
        while lo + 1 < hi:
            middle = (lo + hi) // 2
            if comb(lower + middle, middle) <= remainder:
                lo = middle
            else:
                hi = middle
        offset = lo
        if offset < 0:
            raise AssertionError((number, rank, remainder, lower))
        left, right = 1, lower
        while left < right:
            length = (left + right + 1) // 2
            low_rank = lower - length + 1
            value = comb(lower + offset + 1, offset + 1) - comb(
                low_rank + offset, offset + 1
            )
            if value <= remainder:
                left = length
            else:
                right = length - 1
        low_rank = lower - left + 1
        value = comb(lower + offset + 1, offset + 1) - comb(
            low_rank + offset, offset + 1
        )
        runs.append((lower, low_rank, offset))
        remainder -= value
        lower -= left
        offset_cap = offset
    return runs


def runs_value(runs: list[Run]) -> int:
    return sum(
        comb(high + offset + 1, offset + 1)
        - comb(low + offset, offset + 1)
        for high, low, offset in runs
    )


def add_to_runs(runs: list[Run], rank: int, increment: int) -> list[Run]:
    tail = 0
    for index in range(len(runs) - 1, -1, -1):
        high, low, offset = runs[index]
        if low > 1 and tail + increment < comb(low + offset, offset + 1):
            return runs[: index + 1] + canonical_runs(tail + increment, low - 1)
        tail += comb(high + offset + 1, offset + 1) - comb(
            low + offset, offset + 1
        )
    return canonical_runs(tail + increment, rank)


def defect_step(runs: list[Run], rank: int, parameter: int) -> list[Run]:
    shadow: list[Run] = []
    rank_zero_terms = 0
    for high, low, offset in runs:
        if high >= 2:
            shadow.append((high - 1, max(low, 2) - 1, offset + 1))
        if low == 1:
            rank_zero_terms += 1
    return add_to_runs(shadow, rank - 1, parameter + rank_zero_terms)


def orbit(parameter: int, target: int = 8) -> dict[int, int]:
    rank = parameter - 12
    runs: list[Run] = []
    values = {rank: 0}
    while rank > target:
        runs = defect_step(runs, rank, parameter)
        rank -= 1
        values[rank] = runs_value(runs)
    return values


def rank8_row(
    parameter: int, values: dict[int, int] | None = None
) -> dict[str, object]:
    if values is None:
        values = orbit(parameter)
    d8 = values[8]
    baseline = comb(parameter - 12, 8) + comb(parameter - 13, 7)
    w6 = d8 - baseline
    cap = comb(parameter - 13, 6)
    word = canonical(w6, 6)
    return {
        "V": parameter,
        "D8": d8,
        "W6": w6,
        "W6_cap": cap,
        "margin": cap - w6,
        "W6_word": word,
        "W6_top": word[0][0] if word else 5,
    }


def shadow_to_rank8(number: int, start_rank: int) -> int:
    value = number
    for rank in range(start_rank, 8, -1):
        value = kk(value, rank)
    return value


def prefix_cancellation_checks() -> dict[str, object]:
    """Exhaust finite witnesses for the separately proved concatenation lemma.

    This does not prove that adjacent defect orbits possess a common prefix.
    It guards only the exact algebra used after such a prefix is available.
    """

    cases = 0
    for rank in range(2, 11):
        for suffix_rank in range(1, rank):
            prefix_low = suffix_rank + 1
            for offset in range(0, 7):
                prefix_word = [
                    (lower + offset, lower)
                    for lower in range(rank, prefix_low - 1, -1)
                ]
                prefix_value = sum(comb(upper, lower) for upper, lower in prefix_word)
                prefix_shadow = sum(
                    comb(upper, lower - 1) for upper, lower in prefix_word
                )
                separator = prefix_low + offset
                # x<C(separator,suffix_rank) is exactly the condition that
                # the top upper index of its suffix word is <separator.
                for suffix in range(comb(separator, suffix_rank)):
                    expected_word = prefix_word + canonical(suffix, suffix_rank)
                    assert canonical(prefix_value + suffix, rank) == expected_word
                    assert kk(prefix_value + suffix, rank) == (
                        prefix_shadow + kk(suffix, suffix_rank)
                    )
                    cases += 1
    return {
        "checked_cases": cases,
        "rank_range": [2, 10],
        "prefix_offset_range": [0, 6],
        "scope": "finite executable guard for an exact symbolic concatenation identity; not evidence that adjacent orbit states share the required prefix",
    }


def one_sided_carry_checks() -> dict[str, object]:
    """Guard KK_r(x+h)-KK_r(x)<=KK_r(h)<=r*h on small exact cases."""

    cases = 0
    for rank in range(1, 9):
        for base in range(0, 201):
            for increment in range(0, 51):
                shadow_jump = kk(base + increment, rank) - kk(base, rank)
                assert shadow_jump <= kk(increment, rank)
                assert kk(increment, rank) <= rank * increment
                cases += 1
    return {
        "checked_cases": cases,
        "rank_range": [1, 8],
        "base_range": [0, 200],
        "increment_range": [0, 50],
        "scope": "finite executable guard; the all-parameter proof uses disjoint-ground-set shadow subadditivity and the canonical term bound KK_r(h)<=r*h",
    }


def exact_route_kills() -> dict[str, object]:
    # A successful two-binomial rank-18 gate is not an invariant barrier.
    v = 288
    values = orbit(v)
    p18 = comb(v - 12, 18) + comb(v - 13, 17)
    p16 = comb(v - 12, 16) + comb(v - 13, 15)
    assert values[18] < p18
    assert values[16] == p16 + 67

    # Blind subadditive adjacent coupling starts with V+1 and shadows the
    # increment independently.  Even deleting every later +1 tax leaves a
    # majorizer with a full extra rank-8 term.
    v = 40
    strict_blind = shadow_to_rank8(v + 1, v - 12)
    assert strict_blind == comb(v - 11, 8) + comb(v - 12, 7)
    desired_adjacent_cap = comb(v - 11, 7)
    assert strict_blind > desired_adjacent_cap

    # Splitting every +V tax into independent shadow contributions already
    # fails after the second contribution: the first is exactly the two-term
    # rank-8 baseline, while the second exceeds the entire residual budget.
    first_tax = shadow_to_rank8(v, v - 13)
    second_tax = shadow_to_rank8(v, v - 14)
    baseline = comb(v - 12, 8) + comb(v - 13, 7)
    residual_cap = comb(v - 13, 6)
    assert first_tax == baseline
    assert second_tax > residual_cap

    row50 = rank8_row(50)
    row51 = rank8_row(51)
    assert row51["W6"] == row50["W6"] + 2
    row40 = rank8_row(40)
    row41 = rank8_row(41)
    assert row41["W6"] == row40["W6"] - 8_905

    # There is no single canonical cell valid from the base onward.  In
    # particular the word length changes already between V=42 and V=43.
    row42 = rank8_row(42)
    row43 = rank8_row(43)
    assert len(row42["W6_word"]) == 6
    assert len(row43["W6_word"]) == 5

    # Macaulay/order monotonicity by itself cannot yield the normalized-ratio
    # inequality.  The valid residual integers x<=y below have increasing
    # normalized ratio for the adjacent V=40 capacities.
    x, y = 1, 2
    cap40, cap41 = comb(27, 6), comb(28, 6)
    assert x <= y
    assert y * cap40 > x * cap41

    # The colex "last omitted set" condition is literally the same numerical
    # entry gate after the proved two-term chart is substituted.
    baseline40 = comb(28, 8) + comb(27, 7)
    assert comb(29, 8) - baseline40 == comb(27, 6)

    # A common-prefix hypothesis cannot simply be imposed through every
    # residual carry wall.  This first displayed wall has positive input jump
    # but no common leading rank-7 term; the one-sided carry inequality still
    # controls its shadow jump.
    v = 56
    values56 = orbit(v)
    values57 = orbit(v + 1)
    w7_56 = values56[9] - comb(v - 12, 9) - comb(v - 13, 8)
    w7_57 = values57[9] - comb(v - 11, 9) - comb(v - 12, 8)
    word7_56 = canonical(w7_56, 7)
    word7_57 = canonical(w7_57, 7)
    assert w7_57 - w7_56 == 8
    assert word7_56[0] != word7_57[0]
    assert kk(w7_57, 7) - kk(w7_56, 7) == 15
    return {
        "two_binomial_not_invariant": {
            "V": 288,
            "D18_minus_P18": values[18] - p18,
            "D16_minus_P16": values[16] - p16,
            "scope": "kills propagation of P_q as an invariant cap; it does not kill the proved rank-18-to-rank-8 residual theorem",
        },
        "blind_adjacent_subadditivity": {
            "V": 40,
            "strict_blind_rank8_majorizer": strict_blind,
            "desired_D8_cap_increment": desired_adjacent_cap,
            "overshoot": strict_blind - desired_adjacent_cap,
            "scope": "kills any adjacent proof that shadows the whole increment independently of the common canonical prefix",
        },
        "independent_tax_superposition": {
            "V": 40,
            "first_tax_contribution": first_tax,
            "two_term_baseline": baseline,
            "second_tax_contribution": second_tax,
            "residual_cap": residual_cap,
            "scope": "kills termwise tax accounting without overlap credit",
        },
        "scalar_W6_monotonicity": {
            "decrease": {"V_to_Vplus1": [40, 41], "jump": -8_905},
            "increase": {"V_to_Vplus1": [50, 51], "jump": 2},
            "scope": "kills either one-sided monotonicity of W6 itself; margin or normalized potentials remain open",
        },
        "fixed_canonical_cell": {
            "V42_word": row42["W6_word"],
            "V43_word": row43["W6_word"],
            "scope": "kills a single fixed six-term affine canonical cell beginning at V=40; piecewise or carry-aware word theorems remain open",
        },
        "order_alone_does_not_normalize": {
            "x": x,
            "y": y,
            "cap_V40": cap40,
            "cap_V41": cap41,
            "y_times_cap_V40": y * cap40,
            "x_times_cap_V41": x * cap41,
            "scope": "kills derivation of normalized-ratio decay from scalar order preservation alone; it does not refute the actual W6 ratio statement",
        },
        "protected_missing_set_is_equivalent_gate": {
            "V": 40,
            "target_minus_two_term_baseline": comb(29, 8) - baseline40,
            "residual_cap": comb(27, 6),
            "scope": "a named last omitted colex set with no preimage invariant only restates the rank-8 gate",
        },
        "uniform_residual_prefix": {
            "V_to_Vplus1": [56, 57],
            "rank": 7,
            "W7_jump": w7_57 - w7_56,
            "W7_V_word": word7_56,
            "W7_Vplus1_word": word7_57,
            "shadow_jump": kk(w7_57, 7) - kk(w7_56, 7),
            "scope": "kills any proof that assumes adjacent residual words always share a leading term; it does not kill one-sided carry control or an independently established higher-rank separator",
        },
    }


def finite_survivor_falsifiers() -> dict[str, object]:
    orbit_rows = {v: orbit(v) for v in range(40, 501)}
    rows = [rank8_row(v, orbit_rows[v]) for v in range(40, 501)]
    first_ratio_increase = None
    first_adjacent_cap_failure = None
    first_log_height_failure = None
    maximum_w_jump = (-10**30, 0)
    for before, after in zip(rows, rows[1:]):
        v = int(before["V"])
        jump = int(after["W6"]) - int(before["W6"])
        if jump > maximum_w_jump[0]:
            maximum_w_jump = (jump, v)
        if (
            int(after["W6"]) * int(before["W6_cap"])
            > int(before["W6"]) * int(after["W6_cap"])
            and first_ratio_increase is None
        ):
            first_ratio_increase = v
        if jump >= comb(v - 13, 5) and first_adjacent_cap_failure is None:
            first_adjacent_cap_failure = v
    for row in rows:
        bound = ceil(log2(int(row["V"]))) + 13
        if int(row["W6_top"]) > bound:
            first_log_height_failure = int(row["V"])
            break
    assert min(int(row["margin"]) for row in rows) > 0
    induction_base = [row for row in rows if int(row["V"]) <= 125]
    assert len(induction_base) == 86
    row125 = induction_base[-1]
    assert int(row125["V"]) == 125
    assert int(row125["margin"]) == 2_392_397_730
    high_residuals: dict[int, dict[int, int]] = {}
    first_high_separator_failure = None
    for v, values in orbit_rows.items():
        residuals = {
            rank: (
                values[rank + 2]
                - comb(v - 12, rank + 2)
                - comb(v - 13, rank + 1)
            )
            for rank in range(7, 15)
        }
        high_residuals[v] = residuals
        for rank, residual in residuals.items():
            if not 0 <= residual < comb(v - 13, rank):
                first_high_separator_failure = {
                    "V": v,
                    "rank": rank,
                    "residual": residual,
                    "separator_cap": comb(v - 13, rank),
                }
                break
        if first_high_separator_failure is not None:
            break
    maximum_rank14_jump = max(
        (
            high_residuals[v + 1][14] - high_residuals[v][14],
            v,
        )
        for v in range(40, 500)
    )
    rank14_lipschitz_constant = 1
    fixed_depth_bounds = {14: rank14_lipschitz_constant}
    for rank in range(14, 6, -1):
        fixed_depth_bounds[rank - 1] = 1 + rank * fixed_depth_bounds[rank]
    assert fixed_depth_bounds[6] == 130_455_928
    assert comb(125 - 13, 5) == 134_153_712
    assert fixed_depth_bounds[6] < comb(125 - 13, 5)
    return {
        "V_range": [40, 500],
        "rows": len(rows),
        "minimum_rank8_margin": min(int(row["margin"]) for row in rows),
        "first_normalized_ratio_increase": first_ratio_increase,
        "first_adjacent_cap_failure": first_adjacent_cap_failure,
        "first_log_height_failure": first_log_height_failure,
        "maximum_W6_jump": {"jump": maximum_w_jump[0], "at_V": maximum_w_jump[1]},
        "high_rank_bridge": {
            "rank_range": [7, 14],
            "first_separator_failure": first_high_separator_failure,
            "maximum_rank14_jump": {
                "jump": maximum_rank14_jump[0],
                "at_V": maximum_rank14_jump[1],
            },
            "conditional_fixed_depth_bounds": fixed_depth_bounds,
            "analytic_start_if_rank14_jump_at_most_one": 125,
            "cap_increment_at_125": comb(125 - 13, 5),
            "scope": "finite falsifier for the high-rank lemma; the fixed-depth implication from that lemma is exact and all-parameter",
        },
        "exact_induction_base": {
            "V_range": [40, 125],
            "rows": len(induction_base),
            "minimum_margin": min(int(row["margin"]) for row in induction_base),
            "margin_at_125": int(row125["margin"]),
            "scope": "complete finite base for the conditional V>=125 induction, not an extrapolation",
        },
        "scope": "finite falsifier evidence only; none of the scanned all-V statements follows from this scan",
    }


def main() -> None:
    payload = {
        "status": "PASS",
        "source_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
        "prefix_cancellation_checks": prefix_cancellation_checks(),
        "one_sided_carry_checks": one_sided_carry_checks(),
        "exact_route_kills": exact_route_kills(),
        "finite_survivor_falsifiers": finite_survivor_falsifiers(),
        "scope": "Exact arithmetic and exact finite counterexamples; the bounded V scan is not extrapolated.",
    }
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
