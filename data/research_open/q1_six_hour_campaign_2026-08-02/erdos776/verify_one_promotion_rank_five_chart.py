#!/usr/bin/env python3
"""Exact finite guards for ONE_PROMOTION_RANK_FIVE_CHART.md."""

from __future__ import annotations

import importlib.util
import json
from math import comb
from pathlib import Path


HERE = Path(__file__).resolve().parent
BASE_PATH = HERE / "verify_negative_initial_chambers.py"
SPEC = importlib.util.spec_from_file_location("rank_five_chart_base", BASE_PATH)
assert SPEC is not None and SPEC.loader is not None
BASE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BASE)

upper = BASE.upper
local_orbit = BASE.local_orbit


EXPECTED_COUNTS = {
    "-- -> ++": 164,
    "-- -> --": 3,
    "-- -> -+": 1,
    "-+ -> +-": 1,
    "++ -> --": 31,
    "++ -> -+": 19,
}


def _sign_pair(left: int, right: int) -> str:
    return ("-" if left < 0 else "+") + ("-" if right < 0 else "+")


def _loss(rank: int, cap_index: int, deficit: int) -> int:
    assert 0 <= deficit <= comb(cap_index, rank)
    return comb(cap_index, rank + 1) - upper(
        comb(cap_index, rank) - deficit,
        rank,
    )


def finite_unified_chart(through_offset: int = 250) -> dict[str, object]:
    counts: dict[str, int] = {}
    minima: dict[str, tuple[int, tuple[int, ...]]] = {}
    proved_lower_margins: dict[str, int] = {}
    checked = 0

    for offset in range(31, through_offset + 1):
        for q_value in range(2, offset):
            k_value = offset - q_value
            for r_value in range(q_value):
                u_value = r_value + k_value - 1
                if not 0 <= u_value < q_value + 1:
                    continue

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

                n_value = comb(q_value, 2) + r_value
                h_value = comb(offset, 2) + 1
                tau = h_value - n_value
                gamma_three = (k_value - 1) * r_value - k_value * (q_value + 1)

                r_tail = (
                    comb(r_value + 1, 2)
                    - k_value * q_value
                    - comb(k_value, 2)
                )
                s_tail = (
                    r_tail + comb(u_value, 2) - comb(r_value, 2) - 1
                )
                x_zero = comb(q_value, 3) + r_tail
                y_zero = comb(q_value + 1, 3) + s_tail
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

                epsilon_x = int(r_tail < 0)
                epsilon_y = int(s_tail < 0)
                a_value = q_value - epsilon_x
                gap = 1 + epsilon_x - epsilon_y
                alpha = r_tail + epsilon_x * comb(q_value - 1, 2)
                beta = s_tail + epsilon_y * comb(q_value, 2)
                assert 0 <= alpha < comb(a_value, 2)
                assert 0 <= beta < comb(a_value + gap, 2)
                assert x_zero == comb(a_value, 3) + alpha
                assert y_zero == comb(a_value + gap, 3) + beta

                p_raw = upper(alpha, 2) - tau + 1
                q_raw = upper(beta, 2) - tau
                delta_x = int(p_raw < 0)
                delta_y = int(q_raw < 0)
                a_next = a_value - delta_x
                b_next = a_value + gap - delta_y
                p_tail = p_raw + delta_x * comb(a_value - 1, 3)
                v_tail = q_raw + delta_y * comb(a_value + gap - 1, 3)
                assert 0 <= p_tail < comb(a_next, 3)
                assert 0 <= v_tail < comb(b_next, 3)

                x_one = upper(x_zero, 3) - tau + 1
                y_one = upper(y_zero, 3) - tau
                assert x_one == comb(a_next, 4) + p_tail
                assert y_one == comb(b_next, 4) + v_tail

                predicted_five = (
                    comb(b_next, 5)
                    - comb(a_next, 5)
                    - comb(a_next, 4)
                    + upper(v_tail, 3)
                    - upper(p_tail, 3)
                    - upper(alpha, 2)
                    - 1
                    - delta_x * comb(a_value - 1, 3)
                )
                gamma_five = (
                    upper(y_one, 4)
                    - upper(x_one, 4)
                    - x_one
                    - tau
                )
                assert predicted_five == gamma_five > 0

                orbit = local_orbit(half, offset, 5)
                assert orbit[3] == gamma_three
                assert orbit[4] == gamma_four
                assert orbit[5] == gamma_five

                first_chamber = _sign_pair(r_tail, s_tail)
                second_chamber = _sign_pair(p_raw, q_raw)
                chamber = f"{first_chamber} -> {second_chamber}"

                deficit_left = comb(a_next, 3) - p_tail
                if b_next == a_next + 1:
                    deficit_right = comb(b_next, 3) - v_tail
                    deficit_prediction = (
                        _loss(3, a_next, deficit_left)
                        - _loss(3, b_next, deficit_right)
                        + deficit_left
                        - tau
                    )
                    assert deficit_prediction == gamma_five
                    if chamber in {"++ -> --", "-+ -> +-"}:
                        deficit_gap = deficit_left - deficit_right
                        lower_margin = upper(deficit_gap, 3) + deficit_gap - tau
                        assert deficit_gap >= 0
                        assert gamma_five >= lower_margin > 0
                        proved_lower_margins[chamber] = min(
                            proved_lower_margins.get(chamber, lower_margin),
                            lower_margin,
                        )
                elif b_next == a_next + 2:
                    deficit_prediction = (
                        _loss(3, a_next, deficit_left)
                        + upper(v_tail, 3)
                        - upper(alpha, 2)
                        - 1
                    )
                    assert deficit_prediction == gamma_five
                    if chamber == "++ -> -+":
                        lower_margin = (
                            upper(deficit_left, 3)
                            + upper(v_tail, 3)
                            - upper(alpha, 2)
                            - 1
                        )
                        assert gamma_five >= lower_margin > 0
                        proved_lower_margins[chamber] = min(
                            proved_lower_margins.get(chamber, lower_margin),
                            lower_margin,
                        )
                else:
                    raise AssertionError((chamber, a_next, b_next))

                counts[chamber] = counts.get(chamber, 0) + 1
                witness = (
                    q_value,
                    k_value,
                    r_value,
                    offset,
                    half,
                    gap,
                )
                candidate = (gamma_five, witness)
                minima[chamber] = min(minima.get(chamber, candidate), candidate)
                checked += 1

    if through_offset == 250:
        assert counts == EXPECTED_COUNTS
        assert checked == 219
    global_minimum = min(
        (value, chamber, witness)
        for chamber, (value, witness) in minima.items()
    )
    if through_offset == 250:
        assert global_minimum == (4222, "-- -> --", (34, 13, 0, 47, 238, 1))
    return {
        "through_offset": through_offset,
        "antecedent_points": checked,
        "chamber_counts": counts,
        "chamber_minima": {
            chamber: {"gamma5": value, "q_K_r_b_h_g": list(witness)}
            for chamber, (value, witness) in sorted(minima.items())
        },
        "global_minimum_gamma5": global_minimum[0],
        "global_minimum_chamber": global_minimum[1],
        "global_minimum_witness": list(global_minimum[2]),
        "proved_chamber_lower_margins": proved_lower_margins,
        "pass": True,
    }


def main() -> int:
    result = finite_unified_chart()
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
