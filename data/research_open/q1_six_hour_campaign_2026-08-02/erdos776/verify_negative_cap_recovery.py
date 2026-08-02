#!/usr/bin/env python3
"""Exact guards for ``NEGATIVE_CAP_RECOVERY.md``.

The uniform later-cap result is proved symbolically/asymptotically in the
note.  This verifier independently checks every initial-cap identity over a
large abstract parameter box, the gap invariant over recurrence samples,
and a finite strip falsifier for later first caps.
"""

from __future__ import annotations

import importlib.util
import json
from math import comb
from pathlib import Path


HERE = Path(__file__).resolve().parent
PRECAP_PATH = HERE / "verify_negative_precap.py"
SPEC = importlib.util.spec_from_file_location("negative_precap", PRECAP_PATH)
assert SPEC is not None and SPEC.loader is not None
PRECAP = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PRECAP)

upper = PRECAP.upper
canonical = PRECAP.canonical
offset_constants = PRECAP.offset_constants
stable_word = PRECAP.stable_word


def initial_orbit(half: int, offset: int) -> dict[int, int]:
    tax = 2 * half + offset - 3
    top = half + offset - 2
    x_value = comb(top, 3) + comb(offset - 1, 2) + 2 - 2 * half
    y_value = comb(top + 1, 3) + comb(offset, 2) + 2 - 2 * half
    gamma: dict[int, int] = {}
    for rank in range(3, 5):
        x_next = upper(x_value, rank) - tax
        y_next = upper(y_value, rank) - tax - 1
        gamma[rank] = y_next - x_value - upper(x_value, rank)
        x_value, y_value = x_next, y_next
    return gamma


def check_gap_invariant() -> None:
    for offset in range(5, 101):
        a_values, b_values = offset_constants(offset, 9)
        for rank in range(3, 9):
            a_value = a_values[rank]
            gap = b_values[rank] - a_value
            assert a_value >= offset
            assert gap > 0
            assert gap * gap >= 2 * a_value
            if rank < 8:
                expected = gap * a_value + comb(gap, 2) + 1
                assert b_values[rank + 1] - a_values[rank + 1] == expected


def check_initial_recovery_identities(through_offset: int = 250) -> dict[str, int]:
    checked = {"y_only": 0, "v_zero": 0, "q_nonnegative": 0, "q_negative": 0}
    for offset in range(22, through_offset + 1):
        # The unique negative y-only cap has w=1 and h=C(b,2).
        half = comb(offset, 2)
        d_value = half + offset - 5
        tax_y = 2 * half + offset - 2
        gamma = initial_orbit(half, offset)
        predicted = (
            comb(d_value - 2, 2)
            + comb(d_value - offset - 3, 2)
            - comb(offset - 11, 2)
            - tax_y
        )
        assert gamma[3] < 0
        assert gamma[4] == predicted > 0
        checked["y_only"] += 1

        # Both stable rank-two tails cap.  Enumerate every v allowed by
        # gamma_3<0, not merely values attained on dyadic strips.
        for v_value in range((offset - 1) // 2 + 1):
            half = comb(offset, 2) - v_value - 1
            if half < 224:
                continue
            d_value = half + offset - 5
            tax_y = 2 * half + offset - 2
            gamma = initial_orbit(half, offset)
            if gamma[3] >= 0:
                continue
            r_x = offset + comb(v_value, 2) - 10
            q_value = tax_y - comb(offset + v_value, 2)
            if q_value >= 0 and v_value == 0:
                predicted = (
                    comb(d_value - 3, 2)
                    - comb(offset - 9, 2)
                    - tax_y
                )
                checked["v_zero"] += 1
            elif q_value >= 0:
                r_y = offset * v_value + comb(v_value + 1, 2) - 2
                predicted = (
                    comb(d_value - 1, 2)
                    + comb(r_y, 2)
                    - comb(r_x + 1, 2)
                    - tax_y
                )
                checked["q_nonnegative"] += 1
            else:
                predicted = (
                    comb(d_value, 2)
                    + comb(d_value - 1, 2)
                    - comb(r_x + 1, 2)
                    + upper(-q_value, 2)
                    - tax_y
                )
                checked["q_negative"] += 1
            assert gamma[4] == predicted > 0, (
                offset,
                v_value,
                q_value,
                gamma,
                predicted,
            )
    assert all(checked.values()), checked
    return checked


def later_first_cap_falsifier(through_j: int = 13) -> dict[str, int]:
    points = 0
    minimum: tuple[int, int, int, int] | None = None
    for j in range(2, through_j + 1):
        half = 112 * (1 << (j - 1))
        for offset in range(5, half + 1):
            signed_y = comb(offset - 1, 2) - (2 * half - offset - 1)
            if signed_y >= 0:
                break
            a_values, b_values = offset_constants(offset, 9)
            tax = 2 * half + offset - 3
            top = half + offset - 2
            x_value = comb(top, 3) + comb(offset - 1, 2) + 2 - 2 * half
            y_value = comb(top + 1, 3) + comb(offset, 2) + 2 - 2 * half
            first_cap = None
            for rank in range(3, 9):
                if first_cap is None and (
                    canonical(x_value, rank)
                    != stable_word(half, offset, rank, a_values[rank], False)
                    or canonical(y_value, rank)
                    != stable_word(half, offset, rank, b_values[rank], True)
                ):
                    first_cap = rank
                x_next = upper(x_value, rank) - tax
                y_next = upper(y_value, rank) - tax - 1
                gamma = y_next - x_value - upper(x_value, rank)
                if first_cap == rank and rank >= 4:
                    points += 1
                    candidate = (gamma, j, offset, rank)
                    minimum = candidate if minimum is None else min(minimum, candidate)
                    assert gamma > 0, candidate
                x_value, y_value = x_next, y_next
    assert points > 0 and minimum is not None
    return {
        "through_j": through_j,
        "later_first_cap_points": points,
        "minimum_gamma": minimum[0],
        "minimum_j": minimum[1],
        "minimum_offset": minimum[2],
        "minimum_rank": minimum[3],
    }


def main() -> None:
    check_gap_invariant()
    initial = check_initial_recovery_identities()
    finite = later_first_cap_falsifier()
    print(
        json.dumps(
            {"status": "PASS", "initial_identities": initial, "finite": finite},
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
