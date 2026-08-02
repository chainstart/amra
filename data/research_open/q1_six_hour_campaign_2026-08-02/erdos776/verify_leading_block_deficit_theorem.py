#!/usr/bin/env python3
"""Exact guards for LEADING_BLOCK_DEFICIT_THEOREM.md.

The finite loops below certify only the explicitly bounded bases of the
two all-parameter convolution lemmas.  Their infinite tails are covered by
the rational anchor and derivative checks in ``check_asymptotic_tails``.
"""

from __future__ import annotations

import importlib.util
import json
from fractions import Fraction
from math import comb
from pathlib import Path


HERE = Path(__file__).resolve().parent
BASE_PATH = HERE / "verify_left_b5_obstruction.py"
SPEC = importlib.util.spec_from_file_location("deficit_base", BASE_PATH)
assert SPEC is not None and SPEC.loader is not None
BASE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BASE)

upper = BASE.upper


def loss(rank: int, cap_index: int, deficit: int) -> int:
    """Full-block loss Lambda_{rank,cap_index}(deficit)."""

    cap = comb(cap_index, rank)
    assert 0 <= deficit <= cap
    return comb(cap_index, rank + 1) - upper(cap - deficit, rank)


def check_loss_transport(through_index: int = 14) -> dict[str, int]:
    """Finite regression guard for the two symbolically proved loss laws."""

    checked = 0
    minimum_deficit_slack: int | None = None
    minimum_vertical_slack: int | None = None
    for rank in (2, 3):
        for cap_index in range(rank + 1, through_index + 1):
            cap = comb(cap_index, rank)
            values = [loss(rank, cap_index, d) for d in range(cap + 1)]

            for deficit, value in enumerate(values):
                slack = value - upper(deficit, rank)
                assert slack >= 0
                minimum_deficit_slack = (
                    slack
                    if minimum_deficit_slack is None
                    else min(minimum_deficit_slack, slack)
                )

                vertical_slack = deficit - (
                    loss(rank, cap_index + 1, deficit) - value
                )
                assert vertical_slack >= 0
                minimum_vertical_slack = (
                    vertical_slack
                    if minimum_vertical_slack is None
                    else min(minimum_vertical_slack, vertical_slack)
                )

            for smaller in range(cap + 1):
                for larger in range(smaller, cap + 1):
                    assert values[larger] - values[smaller] >= upper(
                        larger - smaller, rank
                    )
                    checked += 1

    assert minimum_deficit_slack == 0
    assert minimum_vertical_slack == 0
    return {
        "transport_pairs_checked": checked,
        "minimum_deficit_slack": minimum_deficit_slack,
        "minimum_vertical_slack": minimum_vertical_slack,
    }


def check_rank_two_convolution_base() -> dict[str, object]:
    """The exact base 32 <= u <= 421 of Convolution Lemma A."""

    global_minimum: tuple[int, int, int, int, int] | None = None
    for u_value in range(32, 422):
        total = 3 * u_value - 7
        candidates = [
            upper(left, 2) + upper(total - left, 2) - 1
            for left in range(total + 1)
        ]
        promoted = min(candidates)
        left_witness = candidates.index(promoted)
        margin = (
            upper(promoted, 3)
            + promoted
            - comb(u_value, 2)
            - 1
        )
        assert margin > 0
        candidate = (
            margin,
            u_value,
            total,
            promoted,
            left_witness,
        )
        global_minimum = (
            candidate if global_minimum is None else min(global_minimum, candidate)
        )

    assert global_minimum == (178, 32, 89, 215, 40)
    return {
        "range": [32, 421],
        "minimum_margin": global_minimum[0],
        "witness_u_total_promoted_left": list(global_minimum[1:]),
    }


def check_rank_three_convolution_base() -> dict[str, object]:
    """The exact base 32 <= r <= 277 of Convolution Lemma B."""

    global_minimum: tuple[int, int, int, int, int] | None = None
    for r_value in range(32, 278):
        promoted_total = upper(3 * r_value + 2, 2) - 1
        candidates = [
            upper(left, 3) + upper(promoted_total - left, 3)
            for left in range(promoted_total + 1)
        ]
        raised_sum = min(candidates)
        left_witness = candidates.index(raised_sum)
        margin = raised_sum - comb(r_value, 2) - 1
        assert margin > 0
        candidate = (
            margin,
            r_value,
            promoted_total,
            raised_sum,
            left_witness,
        )
        global_minimum = (
            candidate if global_minimum is None else min(global_minimum, candidate)
        )

    assert global_minimum == (258, 32, 384, 755, 188)
    return {
        "range": [32, 277],
        "minimum_margin": global_minimum[0],
        "witness_r_total_raised_left": list(global_minimum[1:]),
    }


def check_asymptotic_tails() -> dict[str, object]:
    """Exact rational guards for both analytic tail anchors/derivatives."""

    # Lemma A: u >= 422.  Here w=sqrt(3u-7)-3 and
    # t=(2w^3-6)^(1/3).  The chosen rationals lie strictly below w,t.
    w_a = Fraction(812, 25)
    t_a = Fraction(1023, 25)
    assert (w_a + 3) ** 2 < 1259
    assert t_a**3 < 2 * w_a**3 - 6
    anchor_a = (
        (t_a - 4) ** 4 / 24
        + w_a**3 / 3
        - 1
        - Fraction(422 * 421, 2)
        - 1
    )
    assert anchor_a == Fraction(51111641, 9375000) > 0

    derivative_a_at_32 = (
        Fraction(437, 5250) * 32**2 - 2 * 32 - Fraction(29, 6)
    )
    derivative_a_slope_at_32 = Fraction(874, 5250) * 32 - 2
    assert derivative_a_at_32 > 0
    assert derivative_a_slope_at_32 > 0

    # Lemma B: r >= 278.  Here w=sqrt(6r+4)-3 and
    # t=(w^3/2-3)^(1/3).
    w_b = Fraction(3789, 100)
    t_b = Fraction(3759, 125)
    assert (w_b + 3) ** 2 < 1672
    assert t_b**3 < w_b**3 / 2 - 3
    anchor_b = (
        (t_b - 4) ** 4 / 12
        - Fraction(278 * 277, 2)
        - 1
    )
    assert anchor_b == Fraction(2674108561, 2929687500) > 0

    coefficient_b = Fraction(450179, 2099520)
    derivative_b_at_37 = (
        (coefficient_b - Fraction(1, 6)) * 37**2
        - 37
        - Fraction(1, 3)
    )
    derivative_b_slope_at_37 = (
        2 * (coefficient_b - Fraction(1, 6)) * 37 - 1
    )
    assert derivative_b_at_37 > 0
    assert derivative_b_slope_at_37 > 0

    return {
        "rank_two_tail_starts": 422,
        "rank_two_anchor_margin": str(anchor_a),
        "rank_three_tail_starts": 278,
        "rank_three_anchor_margin": str(anchor_b),
    }


def check_double_negative_to_single_borrow_base() -> dict[str, object]:
    """Complete q <= 215 base for both remaining first-(--) chambers."""

    single_borrow_witnesses: list[tuple[int, ...]] = []
    double_borrow_witnesses: list[tuple[int, ...]] = []
    antecedents = 0
    for q_value in range(2, 216):
        for k_value in range(4, q_value + 2):
            offset = q_value + k_value
            for r_value in range(q_value - k_value + 2):
                u_value = r_value + k_value - 1
                assert 0 <= u_value < q_value + 1

                twice_half = (
                    (k_value - 1) * q_value
                    + comb(k_value - 1, 2)
                    + 2
                    - r_value
                )
                if twice_half % 2:
                    continue
                half = twice_half // 2
                if half < 224 or offset >= half:
                    continue

                tau = k_value * q_value + comb(k_value, 2) + 1 - r_value
                r_tail = comb(r_value, 2) - tau + 1
                s_tail = comb(u_value, 2) - tau
                x_zero = comb(q_value, 3) + r_tail
                y_zero = comb(q_value + 1, 3) + s_tail
                gamma_three = (k_value - 1) * r_value - k_value * (
                    q_value + 1
                )
                if gamma_three >= 0 or x_zero < 0:
                    continue
                gamma_four = (
                    upper(y_zero, 3)
                    - upper(x_zero, 3)
                    - x_zero
                    - tau
                )
                if gamma_four >= 0:
                    continue
                antecedents += 1

                if not (r_tail < 0 and s_tail < 0):
                    continue
                a_value = q_value - 1
                alpha = r_tail + comb(q_value - 1, 2)
                beta = s_tail + comb(q_value, 2)
                if not (
                    0 <= alpha < comb(a_value, 2)
                    and 0 <= beta < comb(a_value + 1, 2)
                ):
                    continue
                p_raw = upper(alpha, 2) - tau + 1
                q_raw = upper(beta, 2) - tau
                if p_raw >= 0:
                    continue

                cap_index = q_value - 2
                deficit = -p_raw
                p_tail = comb(cap_index, 3) - deficit
                assert 0 <= p_tail < comb(cap_index, 3)

                if q_raw >= 0:
                    v_tail = q_raw
                    assert 0 <= v_tail < comb(cap_index + 2, 3)
                    gamma_five = (
                        loss(3, cap_index, deficit)
                        + upper(v_tail, 3)
                        - upper(alpha, 2)
                        - 1
                    )
                    assert gamma_five > 0
                    single_borrow_witnesses.append(
                        (
                            gamma_five,
                            q_value,
                            k_value,
                            r_value,
                            offset,
                            half,
                            tau,
                            alpha,
                            beta,
                            deficit,
                            v_tail,
                        )
                    )
                    continue

                right_deficit = -q_raw
                v_tail = comb(cap_index + 1, 3) - right_deficit
                assert 0 <= v_tail < comb(cap_index + 1, 3)
                deficit_gap = deficit - right_deficit
                lower_margin = upper(deficit_gap, 3) + deficit_gap - tau
                gamma_five = (
                    upper(v_tail, 3)
                    - upper(p_tail, 3)
                    - p_tail
                    - tau
                )
                assert gamma_five >= lower_margin > 0
                double_borrow_witnesses.append(
                    (
                        gamma_five,
                        lower_margin,
                        q_value,
                        k_value,
                        r_value,
                        offset,
                        half,
                        tau,
                        alpha,
                        beta,
                        deficit,
                        right_deficit,
                        deficit_gap,
                    )
                )

    assert antecedents == 133
    assert single_borrow_witnesses == [
        (4923, 35, 13, 0, 48, 244, 534, 28, 127, 477, 47)
    ]
    assert double_borrow_witnesses == [
        (4222, 1236, 34, 13, 0, 47, 238, 521, 8, 106, 515, 66, 449),
        (4599, 1274, 36, 14, 0, 50, 274, 596, 0, 112, 595, 120, 475),
        (9010, 2548, 41, 16, 0, 57, 361, 777, 4, 148, 775, 31, 744),
    ]
    return {
        "q_range": [2, 215],
        "antecedents": antecedents,
        "target_points": len(single_borrow_witnesses),
        "unique_witness": list(single_borrow_witnesses[0]),
        "double_borrow_points": len(double_borrow_witnesses),
        "double_borrow_minimum": list(min(double_borrow_witnesses)),
    }


def main() -> int:
    result = {
        "loss_transport": check_loss_transport(),
        "rank_two_convolution_base": check_rank_two_convolution_base(),
        "rank_three_convolution_base": check_rank_three_convolution_base(),
        "asymptotic_tails": check_asymptotic_tails(),
        "double_negative_to_single_borrow_base": (
            check_double_negative_to_single_borrow_base()
        ),
        "pass": True,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
