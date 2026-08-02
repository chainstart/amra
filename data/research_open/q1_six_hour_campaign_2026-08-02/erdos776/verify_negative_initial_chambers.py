#!/usr/bin/env python3
"""Exact guards for NEGATIVE_INITIAL_CHAMBERS.md."""

from __future__ import annotations

import importlib.util
import json
from math import comb
from pathlib import Path


HERE = Path(__file__).resolve().parent
BASE_PATH = HERE / "verify_left_b5_obstruction.py"
SPEC = importlib.util.spec_from_file_location("negative_initial_base", BASE_PATH)
assert SPEC is not None and SPEC.loader is not None
BASE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BASE)

upper = BASE.upper


def local_orbit(half: int, offset: int, through_rank: int = 5) -> dict[int, int]:
    top = half + offset - 2
    tax = 2 * half + offset - 3
    x_value = comb(top, 3) + comb(offset - 1, 2) + 2 - 2 * half
    y_value = comb(top + 1, 3) + comb(offset, 2) + 2 - 2 * half
    gamma: dict[int, int] = {}
    for rank in range(3, through_rank + 1):
        x_next = upper(x_value, rank) - tax
        y_next = upper(y_value, rank) - tax - 1
        gamma[rank] = y_next - x_value - upper(x_value, rank)
        x_value, y_value = x_next, y_next
    return gamma


def check_asymmetric_chamber(through_offset: int = 500) -> dict[str, int]:
    checked = {"q_at_least_two": 0, "q_one": 0}
    for offset in range(31, through_offset + 1):
        base = comb(offset - 1, 2) + 2
        for q_value in range(1, offset):
            if (base + q_value) % 2:
                continue
            half = (base + q_value) // 2
            if half < 224 or offset >= half:
                continue
            r_value = offset - 1 - q_value
            predicted_three = (
                q_value * (2 * half + 2 * offset - q_value - 7) // 2
                + upper(r_value, 2)
                - (2 * half + offset - 2)
            )
            gamma = local_orbit(half, offset, 4)
            assert gamma[3] == predicted_three
            if q_value >= 2:
                assert gamma[3] > 0
                checked["q_at_least_two"] += 1
                continue

            c_value = half + offset - 2
            tax_y = 2 * half + offset - 2
            r_y = offset - 7 + upper(offset - 2, 2)
            predicted_four = (
                comb(c_value - 4, 2)
                + comb(r_y, 2)
                - comb(offset - 9, 2)
                - tax_y
            )
            assert gamma[4] == predicted_four > 0
            checked["q_one"] += 1
    assert all(checked.values()), checked
    return checked


def dimensionless_state(half: int, offset: int) -> dict[str, int]:
    n_value = comb(offset - 1, 2) + 2 - 2 * half
    assert n_value >= 0
    h_value = comb(offset, 2) + 1
    m_value = offset - 1
    tau = h_value - n_value
    z_value = upper(n_value, 2)
    w_value = upper(n_value + m_value, 2)
    delta = w_value - z_value
    gamma_three = delta - h_value
    x_zero = n_value + z_value - h_value + 1
    y_zero = n_value + z_value + gamma_three
    return {
        "n": n_value,
        "H": h_value,
        "m": m_value,
        "tau": tau,
        "z": z_value,
        "w": w_value,
        "delta": delta,
        "gamma3": gamma_three,
        "x0": x_zero,
        "y0": y_zero,
    }


def check_dimensionless_chart() -> None:
    samples = 0
    for offset in range(31, 181):
        maximum_half = (comb(offset - 1, 2) + 2) // 2
        if maximum_half < 224:
            continue
        candidates = {
            max(224, offset + 1),
            maximum_half,
            (max(224, offset + 1) + maximum_half) // 2,
        }
        for half in sorted(candidates):
            n_value = comb(offset - 1, 2) + 2 - 2 * half
            if n_value < 0 or offset >= half:
                continue
            state = dimensionless_state(half, offset)
            gamma = local_orbit(half, offset, 5)
            assert gamma[3] == state["gamma3"]
            if gamma[3] >= 0:
                continue
            assert state["y0"] - state["x0"] == state["delta"] - 1
            c_value = half + offset - 2
            tax_y = state["tau"]
            x_four = comb(c_value, 4) + state["x0"]
            y_four = comb(c_value + 1, 4) + state["y0"]
            assert x_four == upper(
                comb(c_value, 3) + state["n"], 3
            ) - (tax_y - 1)
            assert y_four == upper(
                comb(c_value + 1, 3) + state["n"] + state["m"], 3
            ) - tax_y
            if state["x0"] >= 0:
                assert state["x0"] + tax_y == state["z"] + 1
                predicted_four = (
                    upper(state["y0"], 3)
                    - upper(state["x0"], 3)
                    - state["x0"]
                    - tax_y
                )
                d_value = state["y0"] - state["x0"]
                assert predicted_four == (
                    upper(state["x0"] + d_value, 3)
                    - upper(state["x0"], 3)
                    - state["z"]
                    - 1
                )
                assert gamma[4] == predicted_four
                if gamma[4] < 0:
                    x_one = upper(state["x0"], 3) - tax_y + 1
                    y_one = upper(state["y0"], 3) - tax_y
                    assert x_one + tax_y == upper(state["x0"], 3) + 1
                    predicted_five = (
                        upper(y_one, 4)
                        - upper(x_one, 4)
                        - x_one
                        - tax_y
                    )
                    e_value = y_one - x_one
                    assert predicted_five == (
                        upper(x_one + e_value, 4)
                        - upper(x_one, 4)
                        - upper(state["x0"], 3)
                        - 1
                    )
                    assert gamma[5] == predicted_five
            samples += 1
    assert samples > 0


def finite_low_block_guard(through_offset: int = 250) -> dict[str, int]:
    antecedent = 0
    minimum_x_one: tuple[int, int, int, int] | None = None
    minimum_y_one: tuple[int, int, int, int] | None = None
    for offset in range(31, through_offset + 1):
        maximum_half = (comb(offset - 1, 2) + 2) // 2
        for half in range(max(224, offset + 1), maximum_half + 1):
            state = dimensionless_state(half, offset)
            if state["gamma3"] >= 0 or state["x0"] < 0:
                continue
            gamma_four = (
                upper(state["y0"], 3)
                - upper(state["x0"], 3)
                - state["x0"]
                - state["tau"]
            )
            if gamma_four >= 0:
                continue
            antecedent += 1
            x_one = upper(state["x0"], 3) - state["tau"] + 1
            y_one = upper(state["y0"], 3) - state["tau"]
            x_candidate = (x_one, offset, half, state["n"])
            y_candidate = (y_one, offset, half, state["n"])
            minimum_x_one = (
                x_candidate
                if minimum_x_one is None
                else min(minimum_x_one, x_candidate)
            )
            minimum_y_one = (
                y_candidate
                if minimum_y_one is None
                else min(minimum_y_one, y_candidate)
            )
            assert x_one > 0
            assert y_one > 0
    assert antecedent > 0
    assert minimum_x_one is not None and minimum_y_one is not None
    return {
        "through_offset": through_offset,
        "antecedent_points": antecedent,
        "minimum_x_one": minimum_x_one[0],
        "minimum_y_one": minimum_y_one[0],
    }


def finite_no_borrow_falsifier(through_j: int = 10) -> dict[str, int]:
    negative_four = 0
    negative_five = 0
    minimum_five: tuple[int, int, int] | None = None
    for j in range(2, through_j + 1):
        half = 112 * (1 << (j - 1))
        for offset in range(5, half):
            n_value = comb(offset - 1, 2) + 2 - 2 * half
            if n_value < 0:
                continue
            gamma = local_orbit(half, offset, 5)
            if gamma[3] < 0 and gamma[4] < 0:
                negative_four += 1
                candidate = (gamma[5], j, offset)
                minimum_five = (
                    candidate if minimum_five is None else min(minimum_five, candidate)
                )
                if gamma[5] < 0:
                    negative_five += 1
    assert negative_four > 0
    assert negative_five == 0
    assert minimum_five is not None
    return {
        "through_j": through_j,
        "negative_rank_four": negative_four,
        "negative_rank_five": negative_five,
        "minimum_gamma_five": minimum_five[0],
        "minimum_j": minimum_five[1],
        "minimum_offset": minimum_five[2],
    }


def main() -> None:
    asymmetric = check_asymmetric_chamber()
    check_dimensionless_chart()
    low_blocks = finite_low_block_guard()
    finite = finite_no_borrow_falsifier()
    print(
        json.dumps(
            {
                "status": "PASS",
                "asymmetric": asymmetric,
                "low_blocks": low_blocks,
                "finite": finite,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
