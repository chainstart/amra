#!/usr/bin/env python3
"""Exact guards for the negative-side moving-b pre-cap recurrence.

Universal claims are proved symbolically in ``NEGATIVE_PRECAP_ATLAS.md``.
The strip loop at the end is explicitly a finite falsifier search.
"""

from __future__ import annotations

import importlib.util
import json
from math import comb
from pathlib import Path


HERE = Path(__file__).resolve().parent
BASE_PATH = HERE / "verify_left_b5_obstruction.py"
SPEC = importlib.util.spec_from_file_location("left_b5_base", BASE_PATH)
assert SPEC is not None and SPEC.loader is not None
BASE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BASE)

upper = BASE.upper
canonical = BASE.canonical
word_value = BASE.word_value


def offset_constants(offset: int, through: int):
    a_values = {3: comb(offset + 1, 2) - 6}
    b_values = {3: comb(offset + 2, 2) - 6}
    for rank in range(3, through):
        a_values[rank + 1] = (
            comb(a_values[rank], 2) + offset + 6 - 6 * rank
        )
        b_values[rank + 1] = (
            comb(b_values[rank], 2) + offset + 7 - 6 * rank
        )
    return a_values, b_values


def stable_word(half: int, offset: int, rank: int, constant: int, adjacent: bool):
    shift = 1 if adjacent else 0
    result = [(half + offset - 3 + shift, rank)]
    result.extend(
        (half + offset + 3 * lower - 3 * rank - 3 + shift, lower)
        for lower in range(rank - 1, 2, -1)
    )
    result.append((half + offset + 4 - 3 * rank + shift, 2))
    result.append((constant, 1))
    return result


def formal_constant(offset: int, a_value: int, b_value: int) -> int:
    return comb(b_value, 2) - comb(a_value + 1, 2) - (offset - 2)


def check_pre_cap_words() -> None:
    half = 112 * (1 << 200)
    for offset in range(5, 31):
        a_values, b_values = offset_constants(offset, 9)
        tax = 2 * half + offset - 3
        x_value = word_value(stable_word(half, offset, 3, a_values[3], False))
        y_value = word_value(stable_word(half, offset, 3, b_values[3], True))
        previous_constant = None
        for rank in range(3, 8):
            x_word = stable_word(half, offset, rank, a_values[rank], False)
            y_word = stable_word(half, offset, rank, b_values[rank], True)
            assert canonical(x_value, rank) == x_word
            assert canonical(y_value, rank) == y_word
            gamma = upper(y_value, rank) - tax - 1 - x_value - upper(x_value, rank)
            constant = formal_constant(offset, a_values[rank], b_values[rank])
            assert gamma == constant - 2 * half
            if previous_constant is not None:
                assert constant > previous_constant
            previous_constant = constant
            x_value = upper(x_value, rank) - tax
            y_value = upper(y_value, rank) - tax - 1


def check_offset_monotonicity() -> None:
    previous: dict[int, int] | None = None
    for offset in range(5, 101):
        a_values, b_values = offset_constants(offset, 10)
        constants = {
            rank: formal_constant(offset, a_values[rank], b_values[rank])
            for rank in range(3, 10)
        }
        if previous is not None:
            assert all(constants[rank] > previous[rank] for rank in constants)
        previous = constants


def phi(tail: int, increment: int, tax: int) -> int:
    return upper(tail + increment, 2) - tail - upper(tail, 2) - tax


def check_first_wall_atlas() -> None:
    checked = {"none": 0, "y_only": 0, "both": 0}
    # The identities are checked on actual recurrence constants, but directly
    # at the low block so no assumption about an outer scan enters the test.
    for j in range(2, 13):
        half = 112 * (1 << (j - 1))
        for offset in range(5, min(2_000, half + 1)):
            a_values, b_values = offset_constants(offset, 7)
            for rank in range(3, 7):
                d_value = half + offset + 4 - 3 * rank
                if d_value < 3:
                    continue
                a_value = a_values[rank]
                b_value = b_values[rank]
                difference = b_value - a_value
                tax = 2 * half + offset - 2
                nx = comb(d_value, 2) + a_value
                ny = comb(d_value + 1, 2) + b_value
                block_x = comb(d_value + 2, 3) + nx
                block_y = comb(d_value + 3, 3) + ny
                direct = upper(block_y, 3) - block_x - upper(block_x, 3) - tax
                x_cross = nx >= comb(d_value + 2, 2)
                y_cross = ny >= comb(d_value + 3, 2)
                if not x_cross and not y_cross:
                    predicted = phi(nx, d_value + difference, tax)
                    checked["none"] += 1
                elif not x_cross and y_cross:
                    ry = b_value - (2 * d_value + 3)
                    if not (0 <= ry < comb(d_value + 4, 2)):
                        continue
                    predicted = (
                        comb(d_value + 3, 3)
                        + upper(ry, 2)
                        - nx
                        - upper(nx, 2)
                        - tax
                    )
                    checked["y_only"] += 1
                elif x_cross and y_cross:
                    rx = a_value - (2 * d_value + 1)
                    ry = b_value - (2 * d_value + 3)
                    if not (
                        0 <= rx < comb(d_value + 3, 2)
                        and 0 <= ry < comb(d_value + 4, 2)
                    ):
                        continue
                    predicted = phi(rx, difference - 2, tax)
                    checked["both"] += 1
                else:
                    raise AssertionError((j, offset, rank, nx, ny))
                assert direct == predicted, (j, offset, rank, direct, predicted)
    assert all(checked[state] > 0 for state in checked), checked


def first_cap_falsifier(through_j: int = 12) -> dict[str, int]:
    negative_first_caps = 0
    negative_without_next_seed = 0
    cap_points = 0
    for j in range(2, through_j + 1):
        half = 112 * (1 << (j - 1))
        for offset in range(5, half + 1):
            signed_y = comb(offset - 1, 2) - (2 * half - offset - 1)
            if signed_y >= 0:
                break
            a_values, b_values = offset_constants(offset, 9)
            tax = 2 * half + offset - 3
            c_value = half + offset - 2
            x_value = comb(c_value, 3) + comb(offset - 1, 2) + 2 - 2 * half
            y_value = comb(c_value + 1, 3) + comb(offset, 2) + 2 - 2 * half
            first_cap = None
            gamma: dict[int, int] = {}
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
                gamma[rank] = y_next - x_value - upper(x_value, rank)
                x_value, y_value = x_next, y_next
            if first_cap is not None:
                cap_points += 1
                if gamma[first_cap] < 0:
                    negative_first_caps += 1
                    if gamma.get(first_cap + 1, -1) < 0:
                        negative_without_next_seed += 1
    assert negative_first_caps > 0
    assert negative_without_next_seed == 0
    return {
        "through_j": through_j,
        "first_cap_points": cap_points,
        "negative_first_caps": negative_first_caps,
        "negative_without_next_seed": negative_without_next_seed,
    }


def main() -> None:
    check_pre_cap_words()
    check_offset_monotonicity()
    check_first_wall_atlas()
    finite = first_cap_falsifier()
    print(json.dumps({"status": "PASS", "finite_falsifier": finite}, indent=2))


if __name__ == "__main__":
    main()
