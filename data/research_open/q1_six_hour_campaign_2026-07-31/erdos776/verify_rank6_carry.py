#!/usr/bin/env python3
"""Exact guards for the refuted fixed rank-six gate in Erdős #776.

The default checks use two separately coded Macaulay implementations, an
explicit closed-form canonical certificate, and the uncompressed global
adjacent orbit.  ``--exhaustive-first`` additionally repeats the finite
minimality audit; that scan is not used to prove the infinite family.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from math import comb
from pathlib import Path


HERE = Path(__file__).resolve().parent
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
CERTIFICATE_PATH = HERE / "rank6_counterexample_certificate.json"


def load_inherited_engine():
    spec = importlib.util.spec_from_file_location("inherited_776", ENGINE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(ENGINE_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


ENGINE = load_inherited_engine()


def independent_canonical(number: int, rank: int) -> list[tuple[int, int]]:
    """Second greedy combinadic implementation, independent of ENGINE."""
    if number < 0 or rank < 1:
        raise ValueError((number, rank))
    remaining = number
    ceiling: int | None = None
    word: list[tuple[int, int]] = []
    for lower in range(rank, 0, -1):
        if not remaining:
            break
        if ceiling is None:
            left = lower - 1
            right = lower
            while comb(right, lower) <= remaining:
                left = right
                right = max(right + 1, 2 * right)
        else:
            left = lower - 1
            right = ceiling
        while left + 1 < right:
            middle = (left + right) // 2
            if comb(middle, lower) <= remaining:
                left = middle
            else:
                right = middle
        upper = left
        if upper >= lower:
            word.append((upper, lower))
            remaining -= comb(upper, lower)
            ceiling = upper
    if remaining:
        raise AssertionError((number, rank, remaining, word))
    return word


def independent_upper(number: int, rank: int) -> int:
    return sum(
        comb(upper, lower + 1)
        for upper, lower in independent_canonical(number, rank)
    )


def independent_lower(number: int, rank: int) -> int:
    return sum(
        comb(upper, lower - 1)
        for upper, lower in independent_canonical(number, rank)
    )


def local_orbit(upper, lower) -> dict[str, int]:
    j = 10
    length = 224 * (1 << (j - 1))
    half = length // 2
    b_value = half + 5
    c_value = 2 * half + 3
    tax = 3 * half + 2
    ambient = tax - 221
    x_values = {
        3: comb(c_value, 3) + comb(b_value - 1, 2) + 2 - length
    }
    y_values = {
        3: comb(c_value + 1, 3) + comb(b_value, 2) + 2 - length
    }
    gamma: dict[int, int] = {}
    delta: dict[int, int] = {}
    for rank in (3, 4, 5):
        x_values[rank + 1] = upper(x_values[rank], rank) - tax
        y_values[rank + 1] = upper(y_values[rank], rank) - (tax + 1)
        gamma[rank] = y_values[rank + 1] - (
            x_values[rank] + upper(x_values[rank], rank)
        )
        delta[rank] = gamma[rank] + tax + 1

    shifted = x_values[5] + upper(x_values[5], 5)
    lower_shifted = lower(shifted, 6)
    lower_filled = lower(shifted + tax + 1, 6)
    reserve = y_values[5] - lower_shifted
    return {
        "j": j,
        "L": length,
        "h": half,
        "b": b_value,
        "c": c_value,
        "M": ambient,
        "T": tax,
        **{f"x{rank}": value for rank, value in x_values.items()},
        **{f"y{rank}": value for rank, value in y_values.items()},
        **{f"gamma{rank}": value for rank, value in gamma.items()},
        **{f"delta{rank}": value for rank, value in delta.items()},
        "T_plus_1": tax + 1,
        "A_S5_x5": shifted,
        "A_plus_T_plus_1": shifted + tax + 1,
        "KK6_A": lower_shifted,
        "KK6_A_plus_T_plus_1": lower_filled,
        "carry_increment": lower_filled - lower_shifted,
        "reserve_R": reserve,
        "reserve_minus_increment": reserve - (lower_filled - lower_shifted),
    }


def explicit_words(half: int) -> dict[str, list[tuple[int, int]]]:
    return {
        "x3": [(2 * half + 3, 3), (half + 2, 2), (7, 1)],
        "y3": [(2 * half + 4, 3), (half + 3, 2), (9, 1)],
        "x4": [
            (2 * half + 3, 4),
            (half + 1, 3),
            (half - 2, 2),
            (16, 1),
        ],
        "y4": [
            (2 * half + 4, 4),
            (half + 2, 3),
            (half - 1, 2),
            (33, 1),
        ],
        "x5": [
            (2 * half + 3, 5),
            (half + 1, 4),
            (half - 3, 3),
            (half - 6, 2),
            (103, 1),
        ],
        "y5": [
            (2 * half + 4, 5),
            (half + 2, 4),
            (half - 2, 3),
            (half - 5, 2),
            (513, 1),
        ],
    }


def word_value(word: list[tuple[int, int]]) -> int:
    return sum(comb(upper, lower) for upper, lower in word)


def check_closed_form_family() -> None:
    for j in range(4, 31):
        half = 112 * (1 << (j - 1))
        words = explicit_words(half)
        for name, word in words.items():
            rank = int(name[-1])
            value = word_value(word)
            assert independent_canonical(value, rank) == word

        tax = 3 * half + 2
        assert independent_upper(word_value(words["x3"]), 3) - tax == word_value(
            words["x4"]
        )
        assert independent_upper(word_value(words["y3"]), 3) - tax - 1 == word_value(
            words["y4"]
        )
        assert independent_upper(word_value(words["x4"]), 4) - tax == word_value(
            words["x5"]
        )
        assert independent_upper(word_value(words["y4"]), 4) - tax - 1 == word_value(
            words["y5"]
        )
        gamma5 = (
            independent_upper(word_value(words["y5"]), 5)
            - tax
            - 1
            - word_value(words["x5"])
            - independent_upper(word_value(words["x5"]), 5)
        )
        assert gamma5 == 125_969 - 3 * half
        assert (gamma5 < 0) == (j >= 10)


def constants(through: int) -> tuple[dict[int, int], dict[int, int]]:
    a_values = {3: 7}
    b_values = {3: 9}
    for rank in range(3, through):
        a_values[rank + 1] = comb(a_values[rank], 2) - (12 * rank - 31)
        b_values[rank + 1] = comb(b_values[rank], 2) - (12 * rank - 33)
    return a_values, b_values


def stable_word(half: int, rank: int, constant: int, adjacent: bool):
    shift = 1 if adjacent else 0
    word = [(2 * half + 3 + shift, rank)]
    word.extend(
        (half + 4 * lower - 4 * rank + 5 + shift, lower)
        for lower in range(rank - 1, 2, -1)
    )
    word.append((half + 14 - 4 * rank + shift, 2))
    word.append((constant, 1))
    return word


def check_fixed_rank_obstruction() -> None:
    a_values, b_values = constants(9)
    expected_a = [7, 16, 103, 5224, 13642435, 93058009543342]
    expected_b = [9, 33, 513, 131301, 8619910611, 37151429466505241304]
    assert [a_values[r] for r in range(3, 9)] == expected_a
    assert [b_values[r] for r in range(3, 9)] == expected_b

    # This enormous half-length is deliberate: it lies beyond every fixed
    # canonicality threshold through rank 9, so (4.4) is checked literally.
    half = 112 * (1 << 149)
    tax = 3 * half + 2
    for rank in range(3, 9):
        x_word = stable_word(half, rank, a_values[rank], False)
        y_word = stable_word(half, rank, b_values[rank], True)
        assert independent_canonical(word_value(x_word), rank) == x_word
        assert independent_canonical(word_value(y_word), rank) == y_word
        x_next = independent_upper(word_value(x_word), rank) - tax
        y_next = independent_upper(word_value(y_word), rank) - tax - 1
        assert x_next == word_value(
            stable_word(half, rank + 1, a_values[rank + 1], False)
        )
        assert y_next == word_value(
            stable_word(half, rank + 1, b_values[rank + 1], True)
        )
        gamma = y_next - (
            word_value(x_word) + independent_upper(word_value(x_word), rank)
        )
        assert gamma == (
            comb(b_values[rank], 2)
            - comb(a_values[rank] + 1, 2)
            - 3 * half
            - 3
        )


def first_family_seed(j: int, maximum_rank: int = 15) -> int:
    half = 112 * (1 << (j - 1))
    tax = 3 * half + 2
    x_value = comb(2 * half + 3, 3) + comb(half + 4, 2) + 2 - 2 * half
    y_value = comb(2 * half + 4, 3) + comb(half + 5, 2) + 2 - 2 * half
    for rank in range(3, maximum_rank + 1):
        x_next = independent_upper(x_value, rank) - tax
        y_next = independent_upper(y_value, rank) - tax - 1
        gamma = y_next - (x_value + independent_upper(x_value, rank))
        if gamma >= 0:
            return rank
        x_value, y_value = x_next, y_next
    raise AssertionError((j, maximum_rank))


def check_adaptive_candidate() -> None:
    a_values, b_values = constants(15)
    for rank in range(4, 15):
        assert a_values[rank] * 2 <= b_values[rank]
        obstruction = (
            comb(b_values[rank], 2)
            - comb(a_values[rank] + 1, 2)
            - 3
        )
        assert b_values[rank] ** 2 // 4 <= obstruction
        if rank >= 5:
            assert a_values[rank] ** 4 <= b_values[rank] ** 3

    # These include the first two cap-overflow transitions (j=10,26)
    # and much later stable/overflow chambers.  They guard the theorem's
    # case split but remain finite regression checks, not its proof.
    for j in (4, 9, 10, 25, 26, 60, 100, 150, 250, 300):
        half = 112 * (1 << (j - 1))
        candidate = next(
            rank
            for rank in range(3, 16)
            if (
                comb(b_values[rank], 2)
                - comb(a_values[rank] + 1, 2)
                - 3
                >= 3 * half
            )
        )
        assert first_family_seed(j) == candidate


def offset_constants(offset: int, through: int):
    a_values = {3: 2 * offset - 3}
    b_values = {3: 2 * offset - 1}
    for rank in range(3, through):
        a_values[rank + 1] = (
            comb(a_values[rank], 2) + 2 * offset + 21 - 12 * rank
        )
        b_values[rank + 1] = (
            comb(b_values[rank], 2) + 2 * offset + 23 - 12 * rank
        )
    return a_values, b_values


def check_critical_offset_chamber() -> None:
    previous: dict[int, int] | None = None
    for offset in range(5, 16):
        a_values, b_values = offset_constants(offset, 9)
        constants = {
            rank: (
                comb(b_values[rank], 2)
                - comb(a_values[rank] + 1, 2)
                - (offset - 2)
            )
            for rank in range(3, 10)
        }
        if previous is not None:
            assert all(constants[rank] > previous[rank] for rank in constants)
        previous = constants

        half = 112 * (1 << 149)
        tax = 3 * half + offset - 3
        x_word = [
            (2 * half + offset - 2, 3),
            (half + offset - 3, 2),
            (a_values[3], 1),
        ]
        y_word = [
            (2 * half + offset - 1, 3),
            (half + offset - 2, 2),
            (b_values[3], 1),
        ]
        x_value, y_value = word_value(x_word), word_value(y_word)
        for rank in range(3, 9):
            expected_x = [
                (2 * half + offset - 2, rank),
                *[
                    (half + 4 * lower - 4 * rank + offset, lower)
                    for lower in range(rank - 1, 2, -1)
                ],
                (half + offset + 9 - 4 * rank, 2),
                (a_values[rank], 1),
            ]
            expected_y = [
                (2 * half + offset - 1, rank),
                *[
                    (half + 4 * lower - 4 * rank + offset + 1, lower)
                    for lower in range(rank - 1, 2, -1)
                ],
                (half + offset + 10 - 4 * rank, 2),
                (b_values[rank], 1),
            ]
            assert independent_canonical(x_value, rank) == expected_x
            assert independent_canonical(y_value, rank) == expected_y
            x_next = independent_upper(x_value, rank) - tax
            y_next = independent_upper(y_value, rank) - tax - 1
            gamma = y_next - (x_value + independent_upper(x_value, rank))
            assert gamma == constants[rank] - 3 * half
            x_value, y_value = x_next, y_next


def offset_orbit(half: int, offset: int, through: int = 5):
    """Return exact adjacent local surpluses for b=h+offset."""
    length = 2 * half
    b_value = half + offset
    c_value = b_value + half - 2
    tax = length + b_value - 3
    x_value = comb(c_value, 3) + comb(b_value - 1, 2) + 2 - length
    y_value = comb(c_value + 1, 3) + comb(b_value, 2) + 2 - length
    gamma: dict[int, int] = {}
    words: dict[str, list[tuple[int, int]]] = {}
    for rank in range(3, through + 1):
        words[f"x{rank}"] = independent_canonical(x_value, rank)
        words[f"y{rank}"] = independent_canonical(y_value, rank)
        x_next = independent_upper(x_value, rank) - tax
        y_next = independent_upper(y_value, rank) - tax - 1
        gamma[rank] = y_next - (x_value + independent_upper(x_value, rank))
        x_value, y_value = x_next, y_next
    return gamma, words


def check_exceptional_offsets() -> None:
    """Guard Proposition 4.5 on every allowed small offset."""
    for j in (2, 3, 10, 30):
        half = 112 * (1 << (j - 1))
        expected_words = {
            1: {
                "x3": [(2 * half - 1, 3), (half - 3, 2), (half - 4, 1)],
                "y3": [(2 * half, 3), (half - 1, 2), (1, 1)],
                "x4": [
                    (2 * half - 1, 4),
                    (half - 3, 3),
                    (half - 8, 2),
                    (half - 24, 1),
                ],
                "y4": [
                    (2 * half, 4),
                    (half - 2, 3),
                    (half - 6, 2),
                    (half - 17, 1),
                ],
            },
            2: {
                "x4": [
                    (2 * half, 4),
                    (half - 2, 3),
                    (half - 6, 2),
                    (half - 17, 1),
                ],
                "y4": [
                    (2 * half + 1, 4),
                    (half - 1, 3),
                    (half - 5, 2),
                    (half - 11, 1),
                ],
            },
            3: {
                "x4": [
                    (2 * half + 1, 4),
                    (half - 1, 3),
                    (half - 5, 2),
                    (half - 11, 1),
                ],
                "y4": [
                    (2 * half + 2, 4),
                    (half, 3),
                    (half - 3, 2),
                    (3, 1),
                ],
            },
            4: {
                "x5": [
                    (2 * half + 2, 5),
                    (half, 4),
                    (half - 4, 3),
                    (half - 8, 2),
                    (half - 24, 1),
                ],
                "y5": [
                    (2 * half + 3, 5),
                    (half + 1, 4),
                    (half - 3, 3),
                    (half - 6, 2),
                    (103, 1),
                ],
            },
        }
        expected_gamma = {
            1: {
                3: -2 * half - 2,
                4: comb(half - 7, 2) + 3 * half - 122,
            },
            2: {3: 2 - 3 * half, 4: 2 * half - 70},
            3: {3: 3 - 3 * half, 4: 3 * half - 43},
            4: {3: 4 - 3 * half, 4: 112 - 3 * half, 5: 13 * half + 5003},
        }
        first_expected = {1: 4, 2: 4, 3: 4, 4: 5}
        for offset in range(1, 5):
            gamma, words = offset_orbit(half, offset)
            for name, word in expected_words[offset].items():
                assert words[name] == word
            for rank, value in expected_gamma[offset].items():
                assert gamma[rank] == value
            assert min(rank for rank, value in gamma.items() if value >= 0) == (
                first_expected[offset]
            )


def triangular_coordinates(number: int) -> tuple[int, int]:
    """Unique n=C(q,2)+r with q>=1 and 0<=r<q."""
    if number < 0:
        raise ValueError(number)
    left, right = 1, 2
    while comb(right, 2) <= number:
        left, right = right, 2 * right
    while left + 1 < right:
        middle = (left + right) // 2
        if comb(middle, 2) <= number:
            left = middle
        else:
            right = middle
    return left, number - comb(left, 2)


def rank2_phi(number: int, increment: int, tax: int) -> int:
    return (
        independent_upper(number + increment, 2)
        - number
        - independent_upper(number, 2)
        - tax
    )


def check_rank2_endpoint_principle() -> None:
    for number in range(0, 300):
        q_value, remainder = triangular_coordinates(number)
        assert number == comb(q_value, 2) + remainder
        assert 0 <= remainder < q_value
        for increment in range(0, 80):
            final_q, final_remainder = triangular_coordinates(number + increment)
            carry_count = final_q - q_value
            constant = (
                increment
                - carry_count * q_value
                - comb(carry_count, 2)
            )
            assert final_remainder == remainder + constant
            direct = rank2_phi(number, increment, 17)
            endpoint_formula = (
                comb(final_q, 3)
                - comb(q_value + 1, 3)
                + (constant - 1) * (2 * remainder + constant) // 2
                - 17
            )
            assert direct == endpoint_formula


def check_moving_rank4_atlas() -> None:
    """Exact finite guards for Corollary 4.8; not its universal proof."""
    for j in (2, 4, 10):
        half = 112 * (1 << (j - 1))
        asymmetric: list[int] = []
        for offset in range(5, half - 1):
            d_value = half + offset - 7
            a_value = 2 * offset * offset - 5 * offset - 9
            b_value = 2 * offset * offset - offset - 12
            difference = 4 * offset - 3
            f_value = 2 * offset * offset - 8 * offset + 9
            g_value = 2 * offset * offset - 4 * offset + 3
            tax_adjacent = 3 * half + offset - 2

            gamma, _ = offset_orbit(half, offset, through=4)
            actual = gamma[4]
            if g_value < 3 * half:
                low_x = comb(d_value, 2) + a_value
                predicted = rank2_phi(
                    low_x,
                    d_value + difference,
                    tax_adjacent,
                )
            elif f_value < 3 * half < g_value:
                asymmetric.append(offset)
                epsilon = 3 * half - f_value
                q_value = half + offset - 4
                predicted = (
                    comb(q_value, 2)
                    - comb(q_value - epsilon, 2)
                    + independent_upper(4 * offset - 6 - epsilon, 2)
                    - tax_adjacent
                )
                assert epsilon >= 5
                assert predicted > 0
            else:
                assert 3 * half < f_value
                predicted = rank2_phi(
                    f_value - 3 * half,
                    4 * offset - 6,
                    tax_adjacent,
                )
                assert f_value - 3 * half < comb(d_value + 4, 2)
                assert g_value - 3 * half < comb(d_value + 5, 2)
            assert actual == predicted, (j, offset, actual, predicted)

            # The smallest subchamber has no rank-one cap and recovers
            # the polynomial K_4(k)-3h literally.
            if a_value < d_value and b_value < d_value + 1:
                formal_constant = (
                    8 * offset**3
                    - 20 * offset**2
                    - 31 * offset
                    + 44
                )
                assert actual == formal_constant - 3 * half
        assert len(asymmetric) == 1

        gamma_h_minus_1, _ = offset_orbit(half, half - 1, through=5)
        assert gamma_h_minus_1[4] == 2 * half * half - 11 * half - 27
        assert gamma_h_minus_1[4] > 0
        gamma_h, _ = offset_orbit(half, half, through=5)
        assert gamma_h[4] == -2 * half - 9
        assert gamma_h[5] == comb(2 * half - 14, 2) + 4 * half - 144
        assert gamma_h[5] > 0


def synchronized_chart_values(half: int, offset: int) -> tuple[int, int]:
    """Equations (4.54) and (4.57), with h eliminated internally."""
    f_value = 2 * offset * offset - 8 * offset + 9
    number = f_value - 3 * half
    if number < 0:
        raise ValueError((half, offset, number))
    increment = 4 * offset - 6
    tau = 2 * offset * offset - 7 * offset + 7 - number
    top = (2 * offset * offset - 5 * offset - number) // 3
    assert top == half + offset - 3
    tax = tau - 1
    z_value = independent_upper(number, 2)
    w_value = independent_upper(number + increment, 2)
    gamma4 = w_value - z_value - (2 * offset * offset - 7 * offset + 7)
    x_tail = comb(top, 4) + z_value - tax
    y_tail = comb(top + 1, 4) + w_value - tau
    gamma5 = (
        independent_upper(y_tail, 4)
        - x_tail
        - independent_upper(x_tail, 4)
        - tau
    )
    return gamma4, gamma5


def check_double_borrow_endpoint(
    half: int,
    offset: int,
    number: int,
) -> None:
    increment = 4 * offset - 6
    h_constant = 2 * offset * offset - 7 * offset + 7
    z_value = independent_upper(number, 2)
    delta = independent_upper(number + increment, 2) - z_value
    gamma4 = delta - h_constant
    s_value = number + z_value
    x_algebraic = s_value - h_constant + 1
    y_algebraic = s_value + gamma4
    if not (gamma4 < 0 and x_algebraic < 0 and y_algebraic < 0):
        return

    a_value = -x_algebraic
    b_value = -y_algebraic
    e_value = half + offset - 5
    tau = h_constant - number
    p_value = comb(e_value, 2) - a_value
    q_value = comb(e_value + 1, 2) - b_value
    reduced = (
        independent_upper(q_value, 2)
        - p_value
        - independent_upper(p_value, 2)
        - tau
    )
    _, gamma5 = synchronized_chart_values(half, offset)
    assert reduced == gamma5
    assert 0 < b_value < a_value < 3 * e_value - 6

    def deficit_row(cap: int, deficit: int) -> int:
        row = 1
        while comb(cap, 2) - comb(cap - row, 2) < deficit:
            row += 1
        return row

    i_value = deficit_row(e_value, a_value)
    j_value = deficit_row(e_value + 1, b_value)
    assert 1 <= j_value <= i_value <= 3
    d_i = i_value * e_value - comb(i_value + 1, 2)
    d_j = j_value * (e_value + 1) - comb(j_value + 1, 2)
    remainder = d_i - a_value
    constant = delta - 1 + d_j - d_i
    exact = (
        comb(e_value + 1 - j_value, 3)
        - comb(e_value - i_value + 1, 3)
        + comb(remainder + constant, 2)
        - comb(remainder + 1, 2)
        - tau
    )
    assert exact == gamma5

    if i_value == j_value:
        lower_bound = comb(delta, 2) - tau
    elif i_value == j_value + 1 and constant >= 1:
        lower_bound = comb(e_value - j_value, 2) - tau
    elif i_value == j_value + 1:
        lower_bound = (
            comb(delta + j_value - 2, 2)
            + e_value
            - j_value
            - 1
            - tau
        )
    elif constant >= 1:
        assert (i_value, j_value) == (3, 1)
        lower_bound = (
            comb(e_value - 1, 2)
            + comb(e_value - 2, 2)
            - tau
        )
    else:
        assert (i_value, j_value) == (3, 1)
        lower_bound = (
            delta * delta
            - 2 * delta * e_value
            + delta
            + 2 * e_value * e_value
            - 2 * e_value
            - 4
        ) // 2 - tau
    assert gamma5 >= lower_bound > 0


def check_asymmetric_borrow_endpoint(
    half: int,
    offset: int,
    number: int,
) -> None:
    increment = 4 * offset - 6
    h_constant = 2 * offset * offset - 7 * offset + 7
    z_value = independent_upper(number, 2)
    delta = independent_upper(number + increment, 2) - z_value
    gamma4 = delta - h_constant
    s_value = number + z_value
    a_value = h_constant - 1 - s_value
    ell_value = s_value + gamma4
    if not (gamma4 < 0 and a_value > 0 and ell_value >= 0):
        return

    e_value = half + offset - 5
    tau = h_constant - number
    p_value = comb(e_value, 2) - a_value
    reduced = (
        comb(e_value + 1, 3)
        + independent_upper(ell_value, 3)
        - p_value
        - independent_upper(p_value, 2)
        - tau
    )
    _, gamma5 = synchronized_chart_values(half, offset)
    assert reduced == gamma5 > 0

    row = 1
    while comb(e_value, 2) - comb(e_value - row, 2) < a_value:
        row += 1
    assert 1 <= row <= 3
    if row >= 2:
        assert gamma5 >= comb(e_value, 2) + e_value - 2 - tau > 0
    elif a_value >= 4:
        assert gamma5 >= 4 * e_value - 10 - tau > 0


def promotion_profile(leading: int, increment: int) -> int:
    """Rank-three gain from the bottom of a fixed leading row."""
    return (
        independent_upper(comb(leading, 3) + increment, 3)
        - comb(leading, 4)
    )


def check_no_borrow_bridge() -> None:
    """Exact finite endpoints left by the proof of Theorem 4.14.

    The infinite ranges are discharged symbolically in the manuscript.  This
    guard checks only the two explicitly finite endpoint sets used there; it
    is not a scan offered in place of the infinite argument.
    """
    # In the large-leading case q >= 52 is covered by nine symbolic row
    # promotions.  These are the remaining finite q endpoints.
    finite_promotion_margins = []
    for leading_q in range(16, 52):
        base = leading_q // 2
        increment = 3 * comb(leading_q, 2) - 1
        finite_promotion_margins.append(
            (
                promotion_profile(base, increment)
                - comb(leading_q + 1, 3),
                leading_q,
            )
        )
    assert min(finite_promotion_margins) == (386, 16)

    # In the small-leading case q >= 92 is covered by the explicit real-root
    # estimate.  Feasibility bounds K, leaving exactly these (odd K,q)
    # endpoints.  The chunk lower bound is
    # J*C(q,2)+C(v,2)-1, where 2K=Jq+v.
    direct_endpoint_count = 0
    finite_direct_margins = []
    for leading_q in range(16, 92):
        base = leading_q // 2
        root_threshold = comb(leading_q + 1, 3) - comb(base, 3)
        maximum_shadow = comb(leading_q + 1, 3) + comb(leading_q, 2)
        for central_index in range(39, 1_001, 2):
            if comb(central_index, 2) > maximum_shadow:
                break
            if leading_q >= -(-(2 * central_index) // 3):
                continue
            if comb(central_index, 2) <= root_threshold:
                continue
            quotient, remainder = divmod(2 * central_index, leading_q)
            chunk_bound = (
                quotient * comb(leading_q, 2)
                + comb(remainder, 2)
                - 1
            )
            margin = (
                independent_upper(chunk_bound, 3)
                - comb(leading_q + 1, 3)
            )
            direct_endpoint_count += 1
            finite_direct_margins.append(
                (margin, central_index, leading_q)
            )
    assert direct_endpoint_count == 738
    assert min(finite_direct_margins) == (1_150, 39, 16)

    # Polynomial identities for the nine-row infinite tail, split by parity.
    for half_q in (26, 27, 100, 1_000):
        for leading_q, expected_capacity, expected_margin in (
            (
                2 * half_q,
                (3 * half_q * half_q - 69 * half_q - 170) // 2,
                (
                    half_q**3
                    + 81 * half_q**2
                    + 416 * half_q
                    + 756
                )
                // 6,
            ),
            (
                2 * half_q + 1,
                (3 * half_q * half_q - 57 * half_q - 170) // 2,
                (
                    half_q**3
                    + 69 * half_q**2
                    + 410 * half_q
                    + 756
                )
                // 6,
            ),
        ):
            base = leading_q // 2
            assert (
                3 * comb(leading_q, 2)
                - 1
                - (comb(base + 9, 3) - comb(base, 3))
                == expected_capacity
            )
            assert (
                comb(base + 9, 4)
                - comb(base, 4)
                - comb(leading_q + 1, 3)
                == expected_margin
            )


def check_synchronized_chart() -> None:
    for offset in range(5, 1001):
        increment = 4 * offset - 6
        quotient, remainder = divmod(increment, 3)
        chunks = [quotient + (index < remainder) for index in range(3)]
        assert sum(comb(chunk, 2) for chunk in chunks) > (
            2 * offset * offset - 7 * offset + 7
        )

    finite_bridge_points = 0
    for j in (2, 4, 10, 20):
        half = 112 * (1 << (j - 1))
        offset = 5
        f_value = lambda value: 2 * value * value - 8 * value + 9
        while f_value(offset) < 3 * half:
            offset += 1
        observed_negative = False
        # The negative reset interval lies immediately after the wall.
        for current in range(offset, min(half - 1, 2 * offset + 10)):
            reduced4, reduced5 = synchronized_chart_values(half, current)
            if j <= 10:
                gamma, _ = offset_orbit(half, current, through=5)
                assert reduced4 == gamma[4]
                assert reduced5 == gamma[5]
            if reduced4 < 0:
                observed_negative = True
                finite_bridge_points += 1
                number = f_value(current) - 3 * half
                leading, _ = triangular_coordinates(number)
                assert leading < -(-(4 * current - 6) // 3)
                assert reduced5 > 0
                check_double_borrow_endpoint(half, current, number)
                check_asymmetric_borrow_endpoint(half, current, number)
            elif observed_negative:
                break
        assert observed_negative

    # A denser non-dyadic lattice falsifier search.  This is deliberately
    # recorded as finite evidence, never as the proof of (4.58).
    for offset in range(5, 81):
        f_value = 2 * offset * offset - 8 * offset + 9
        maximum_number = 2 * offset * offset - 11 * offset + 3
        for number in range(f_value % 3, maximum_number + 1, 3):
            half = (f_value - number) // 3
            if half < 224:
                continue
            reduced4, reduced5 = synchronized_chart_values(half, offset)
            if reduced4 < 0:
                finite_bridge_points += 1
                leading, _ = triangular_coordinates(number)
                assert leading < -(-(4 * offset - 6) // 3)
                assert reduced5 > 0
                check_double_borrow_endpoint(half, offset, number)
                check_asymmetric_borrow_endpoint(half, offset, number)
    assert finite_bridge_points > 0

    expected_row_minima = {
        20: 101,
        21: 65,
        22: 189,
        23: 324,
        24: 507,
        25: 725,
        26: 1001,
        27: 1305,
        28: 1678,
        29: 2105,
    }
    observed_row_minima: dict[int, int] = {}
    for offset in range(53, 111):
        value = 4 * offset - 6
        leading, _ = triangular_coordinates(value)
        margin = (
            independent_upper(independent_upper(value, 2) - 4, 3)
            - (2 * offset * offset - 7 * offset + 7)
        )
        if leading < 30:
            observed_row_minima[leading] = min(
                observed_row_minima.get(leading, margin),
                margin,
            )
    assert observed_row_minima == expected_row_minima

    expected_small_asymmetric = [
        (224, 22, 129, 95, 19_749),
        (448, 29, 115, 870, 217_989),
        (896, 40, 201, 1530, 808_309),
    ]
    observed_small_asymmetric: list[tuple[int, int, int, int, int]] = []
    for half in (224, 448, 896):
        for offset in range(21, 53):
            number = 2 * offset * offset - 8 * offset + 9 - 3 * half
            if number < 0:
                continue
            reduced4, reduced5 = synchronized_chart_values(half, offset)
            h_constant = 2 * offset * offset - 7 * offset + 7
            s_value = number + independent_upper(number, 2)
            a_value = h_constant - 1 - s_value
            ell_value = s_value + reduced4
            if reduced4 < 0 and a_value > 0 and ell_value >= 0:
                observed_small_asymmetric.append(
                    (half, offset, number, a_value, reduced5)
                )
    assert observed_small_asymmetric == expected_small_asymmetric
    check_no_borrow_bridge()


def check_global_orbit(expected_gamma: int) -> None:
    ambient = 171_813
    f_value = ambient
    g_value = ambient + 1
    observed = None
    for rank in range(1, 14):
        g_next = ENGINE.upper_raise(g_value, rank) - (ambient + 222)
        gamma = g_next - (f_value + ENGINE.upper_raise(f_value, rank))
        if rank == 13:
            observed = gamma
        f_value = ENGINE.upper_raise(f_value, rank) - (ambient + 221)
        g_value = g_next
    assert observed == expected_gamma == -46_063


def check_extended_local_to_global() -> None:
    """Guard the fixed-rank extension of the inherited cancellation."""
    for j, maximum_local_rank in ((10, 7), (30, 8), (60, 9)):
        half = 112 * (1 << (j - 1))
        tax = 3 * half + 2
        ambient = tax - 221
        x_value = comb(2 * half + 3, 3) + comb(half + 4, 2) + 2 - 2 * half
        y_value = comb(2 * half + 4, 3) + comb(half + 5, 2) + 2 - 2 * half
        local: dict[int, int] = {}
        for rank in range(3, maximum_local_rank + 1):
            x_next = ENGINE.upper_raise(x_value, rank) - tax
            y_next = ENGINE.upper_raise(y_value, rank) - tax - 1
            local[rank] = y_next - (
                x_value + ENGINE.upper_raise(x_value, rank)
            )
            x_value, y_value = x_next, y_next

        f_value = ambient
        g_value = ambient + 1
        global_surplus: dict[int, int] = {}
        final_global_rank = j + maximum_local_rank - 2
        for rank in range(1, final_global_rank + 1):
            g_next = ENGINE.upper_raise(g_value, rank) - (ambient + 222)
            global_surplus[rank] = g_next - (
                f_value + ENGINE.upper_raise(f_value, rank)
            )
            f_value = ENGINE.upper_raise(f_value, rank) - (ambient + 221)
            g_value = g_next
        for rank, gamma in local.items():
            assert global_surplus[j + rank - 2] == gamma


def local_gamma5(length: int, b_value: int) -> int:
    c_value = b_value + length // 2 - 2
    tax = length + b_value - 3
    x_value = comb(c_value, 3) + comb(b_value - 1, 2) + 2 - length
    y_value = comb(c_value + 1, 3) + comb(b_value, 2) + 2 - length
    gamma = 0
    for rank in (3, 4, 5):
        x_next = independent_upper(x_value, rank) - tax
        y_next = independent_upper(y_value, rank) - tax - 1
        gamma = y_next - (x_value + independent_upper(x_value, rank))
        x_value, y_value = x_next, y_next
    return gamma


def exhaustive_first_failure() -> dict[str, object]:
    digest = hashlib.sha256()
    first: tuple[int, int, int] | None = None
    tenth_negative: list[tuple[int, int]] = []
    for j in range(2, 11):
        length = 224 * (1 << (j - 1))
        for b_value in range(1, length + 1):
            gamma = local_gamma5(length, b_value)
            digest.update(f"{j}:{b_value}:{gamma};".encode())
            if gamma < 0:
                if first is None:
                    first = (j, b_value, gamma)
                if j == 10:
                    tenth_negative.append((b_value, gamma))
    assert first == (10, 57_349, -46_063)
    assert tenth_negative == [(57_349, -46_063)]
    return {
        "first_failure": first,
        "tenth_strip_negative_points": tenth_negative,
        "sha256": digest.hexdigest(),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--exhaustive-first", action="store_true")
    args = parser.parse_args()

    certificate = json.loads(CERTIFICATE_PATH.read_text())
    inherited = local_orbit(ENGINE.upper_raise, ENGINE.lower_shadow)
    independent = local_orbit(independent_upper, independent_lower)
    for key, expected in certificate.items():
        if key in inherited:
            assert inherited[key] == expected, (key, inherited[key], expected)
            assert independent[key] == expected, (key, independent[key], expected)

    check_global_orbit(certificate["global_Gamma_13"])
    check_extended_local_to_global()
    check_closed_form_family()
    check_fixed_rank_obstruction()
    check_adaptive_candidate()
    check_critical_offset_chamber()
    check_exceptional_offsets()
    check_rank2_endpoint_principle()
    check_moving_rank4_atlas()
    check_synchronized_chart()

    result: dict[str, object] = {
        "status": "PASS",
        "two_local_implementations_agree": True,
        "closed_form_family_checked_j": [4, 30],
        "first_symbolic_negative_j": 10,
        "global_Gamma_13": certificate["global_Gamma_13"],
        "fixed_rank_recurrence_checked_through": 9,
        "adaptive_candidate_strategic_checks": 10,
        "critical_offsets_checked": [5, 15],
        "exceptional_offsets_checked": [1, 4],
        "rank2_endpoint_cases_checked": 24_000,
        "moving_rank4_atlas_strips_checked": [2, 4, 10],
        "synchronized_bridge_dense_offset_through": 80,
        "no_borrow_finite_promotion_q": [16, 51],
        "no_borrow_finite_direct_endpoints": 738,
        "extended_local_to_global_checked": [[10, 7], [30, 8], [60, 9]],
    }
    if args.exhaustive_first:
        result["exhaustive_minimality"] = exhaustive_first_failure()
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
