#!/usr/bin/env python3
"""Exact guards for FINAL_CHAMBER_COUNTERFAMILY.md.

The symbolic all-parameter proof is written in the note.  This verifier
checks every displayed canonical word and identity, the complete finite
dyadic base before the stable rank-six word, and the first rank-five
failure with two separately implemented Macaulay raisers.
"""

from __future__ import annotations

import importlib.util
import json
from math import comb
from pathlib import Path
from typing import Callable


HERE = Path(__file__).resolve().parent
BASE_PATH = HERE / "verify_left_b5_obstruction.py"
SPEC = importlib.util.spec_from_file_location("final_chamber_base", BASE_PATH)
assert SPEC is not None and SPEC.loader is not None
BASE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BASE)
INHERITED_UPPER = BASE.ENGINE.upper_raise


def canonical(number: int, rank: int) -> list[tuple[int, int]]:
    """A local greedy combinadic implementation with binary searches."""
    if number < 0 or rank < 1:
        raise ValueError((number, rank))
    remainder = number
    cap: int | None = None
    word: list[tuple[int, int]] = []
    for lower in range(rank, 0, -1):
        if remainder == 0:
            break
        low = lower - 1
        if cap is None:
            high = 2 * lower
            while comb(high, lower) <= remainder:
                high *= 2
        else:
            high = cap
        while low + 1 < high:
            middle = (low + high) // 2
            if comb(middle, lower) <= remainder:
                low = middle
            else:
                high = middle
        if low >= lower:
            word.append((low, lower))
            remainder -= comb(low, lower)
            cap = low
    if remainder:
        raise AssertionError((number, rank, remainder, word))
    return word


def upper(number: int, rank: int) -> int:
    return sum(comb(top, lower + 1) for top, lower in canonical(number, rank))


def word_value(word: list[tuple[int, int]]) -> int:
    return sum(comb(top, lower) for top, lower in word)


def full_orbit(
    raise_fn: Callable[[int, int], int],
    half: int,
    offset: int,
    through_rank: int = 6,
) -> dict[int, int]:
    """Uncompressed original adjacent orbit, including its leading blocks."""
    cap = half + offset - 2
    tau = 2 * half + offset - 2
    x_value = comb(cap, 3) + comb(offset - 1, 2) + 2 - 2 * half
    y_value = comb(cap + 1, 3) + comb(offset, 2) + 2 - 2 * half
    result: dict[int, int] = {}
    for rank in range(3, through_rank + 1):
        x_next = raise_fn(x_value, rank) - tau + 1
        y_next = raise_fn(y_value, rank) - tau
        result[rank] = y_next - x_value - raise_fn(x_value, rank)
        x_value, y_value = x_next, y_next
    return result


def family(exponent: int) -> dict[str, int]:
    if exponent < 2 or exponent % 4 != 2:
        raise ValueError(exponent)
    half = 224 * (1 << exponent)
    numerator = 2 * half - 2
    assert numerator % 5 == 0
    q_value = numerator // 5
    offset = q_value + 6
    n_value = comb(q_value, 2) + 10
    return {
        "s": exponent,
        "h": half,
        "q": q_value,
        "b": offset,
        "n": n_value,
        "tau": 6 * q_value + 6,
    }


def check_dyadic_legality() -> None:
    for exponent in range(16):
        divisible = (448 * (1 << exponent) - 2) % 5 == 0
        assert divisible == (exponent % 4 == 2)

    for exponent in (2, 6, 10, 14, 18):
        data = family(exponent)
        half, q_value, offset, n_value = (
            data["h"],
            data["q"],
            data["b"],
            data["n"],
        )
        assert q_value >= 358
        assert 0 <= 10 < q_value
        assert 0 <= 15 < q_value + 1
        assert 31 <= offset < half
        assert half >= 224
        assert n_value + offset - 1 == comb(q_value + 1, 2) + 15
        assert comb(offset - 1, 2) + 2 - n_value == 2 * half
        assert comb(offset, 2) + 1 - n_value == data["tau"]
        assert 2 * half + offset - 2 == data["tau"]


def chart_state(q_value: int) -> dict[str, int]:
    tau = 6 * q_value + 6
    r_tail = 40 - 6 * q_value
    s_tail = 99 - 6 * q_value
    alpha = comb(q_value - 1, 2) + r_tail
    beta = comb(q_value, 2) + s_tail
    p_raw = upper(alpha, 2) - tau + 1
    q_raw = upper(beta, 2) - tau
    p_two = upper(p_raw, 3) - tau + 1
    q_two = upper(q_raw, 3) - tau
    return {
        "tau": tau,
        "R": r_tail,
        "S": s_tail,
        "alpha": alpha,
        "beta": beta,
        "P": p_raw,
        "Q": q_raw,
        "P2": p_two,
        "Q2": q_two,
    }


def check_two_canonical_levels() -> None:
    for q_value in (2_948, 717_116, 4_302_621, 100_000_000):
        state = chart_state(q_value)
        alpha_word = [(q_value - 7, 2), (13, 1)]
        beta_word = [(q_value - 6, 2), (78, 1)]
        p_word = [(q_value - 8, 3), (q_value - 14, 2), (4, 1)]
        q_word = [(q_value - 7, 3), (q_value - 13, 2), (2_934, 1)]
        assert state["R"] < state["S"] < 0
        assert canonical(state["alpha"], 2) == alpha_word
        assert canonical(state["beta"], 2) == beta_word
        assert canonical(state["P"], 3) == p_word
        assert canonical(state["Q"], 3) == q_word
        assert state["alpha"] == word_value(alpha_word)
        assert state["beta"] == word_value(beta_word)
        assert state["P"] == word_value(p_word) > 0
        assert state["Q"] == word_value(q_word) > 0
        assert state["alpha"] < comb(q_value - 1, 2)
        assert state["beta"] < comb(q_value, 2)
        assert state["P"] < comb(q_value - 1, 3)
        assert state["Q"] < comb(q_value, 3)


def check_surplus_identities() -> None:
    for q_value in (2_948, 717_115, 717_116, 4_302_621, 100_000_000):
        state = chart_state(q_value)
        n_value = comb(q_value, 2) + 10
        offset = q_value + 6
        h_value = comb(offset, 2) + 1
        gamma_three = upper(n_value + offset - 1, 2) - upper(n_value, 2) - h_value
        x_zero = comb(q_value, 3) + state["R"]
        y_zero = comb(q_value + 1, 3) + state["S"]
        gamma_four = (
            upper(y_zero, 3)
            - upper(x_zero, 3)
            - x_zero
            - state["tau"]
        )
        x_one = comb(q_value - 1, 4) + state["P"]
        y_one = comb(q_value, 4) + state["Q"]
        gamma_five = (
            upper(y_one, 4)
            - upper(x_one, 4)
            - x_one
            - state["tau"]
        )
        assert gamma_three == 44 - 6 * q_value
        assert gamma_four == 2_906 - 6 * q_value
        assert gamma_five == comb(2_934, 2) - 6 * q_value - 16

    assert comb(2_934, 2) == 4_302_711
    assert 4_302_695 - 6 * 717_115 == 5
    assert 4_302_695 - 6 * 717_116 == -1


def check_stable_rank_six() -> None:
    threshold = 4_302_621
    for q_value in (threshold, 23_488_102, 100_000_000):
        state = chart_state(q_value)
        p_two_word = [
            (q_value - 8, 4),
            (q_value - 15, 3),
            (q_value - 22, 2),
            (q_value - 132, 1),
        ]
        q_two_word = [
            (q_value - 7, 4),
            (q_value - 14, 3),
            (q_value - 20, 2),
            (4_302_600, 1),
        ]
        assert canonical(state["P2"], 4) == p_two_word
        assert canonical(state["Q2"], 4) == q_two_word
        assert state["P2"] == word_value(p_two_word) > 0
        assert state["Q2"] == word_value(q_two_word) > 0
        gamma_six = (
            upper(state["Q2"], 4)
            - upper(state["P2"], 4)
            - state["P2"]
            - state["tau"]
        )
        expected = comb(4_302_600, 2) + 104 * q_value - 8_421
        assert gamma_six == expected > 0

    assert comb(4_302_600, 2) == 9_256_181_228_700
    below = chart_state(threshold - 1)
    proposed_below_word = [
        (threshold - 8, 4),
        (threshold - 15, 3),
        (threshold - 21, 2),
        (4_302_600, 1),
    ]
    assert canonical(below["Q2"], 4) != proposed_below_word


EXPECTED = {
    2: {3: -2_104, 4: 758, 5: 370_137, 6: 42_058_239},
    6: {3: -34_360, 4: -31_498, 5: 4_268_291, 6: 4_252_643_571},
    10: {3: -550_456, 4: -547_594, 5: 3_752_195, 6: 28_677_939_989},
    14: {
        3: -8_807_992,
        4: -8_805_130,
        5: -4_505_341,
        6: 3_088_969_555_650,
    },
    18: {
        3: -140_928_568,
        4: -140_925_706,
        5: -136_625_917,
        6: 9_258_623_982_887,
    },
}


def check_complete_dyadic_base() -> None:
    for exponent, expected in EXPECTED.items():
        data = family(exponent)
        independent = full_orbit(upper, data["h"], data["b"])
        inherited = full_orbit(INHERITED_UPPER, data["h"], data["b"])
        assert independent == inherited == expected

    first = family(14)
    assert first == {
        "s": 14,
        "h": 3_670_016,
        "q": 1_468_006,
        "b": 1_468_012,
        "n": 1_077_520_074_025,
        "tau": 8_808_042,
    }
    assert EXPECTED[2][5] > 0
    assert EXPECTED[6][5] > 0
    assert EXPECTED[10][5] > 0
    assert EXPECTED[14][5] < 0
    assert family(10)["q"] < 717_116 <= first["q"]
    assert first["q"] < 4_302_621 <= family(18)["q"]

    state = chart_state(first["q"])
    assert canonical(state["P2"], 4) == [
        (1_467_998, 4),
        (1_467_991, 3),
        (1_467_984, 2),
        (1_467_874, 1),
    ]
    assert canonical(state["Q2"], 4) == [
        (1_467_999, 4),
        (1_467_992, 3),
        (1_467_988, 2),
        (1_366_627, 1),
    ]


def main() -> int:
    check_dyadic_legality()
    check_two_canonical_levels()
    check_surplus_identities()
    check_stable_rank_six()
    check_complete_dyadic_base()
    print(
        json.dumps(
            {
                "status": "PASS",
                "rank_five_bridge": "REFUTED",
                "first_negative_dyadic_exponent": 14,
                "first_negative_q": 1_468_006,
                "first_negative_gamma5": -4_505_341,
                "first_negative_gamma6": 3_088_969_555_650,
                "stable_rank_six_from_q": 4_302_621,
                "whole_family_gamma6_positive": True,
                "two_macaulay_implementations": True,
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
