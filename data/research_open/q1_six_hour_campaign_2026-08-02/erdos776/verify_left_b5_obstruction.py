#!/usr/bin/env python3
"""Exact guards for the fixed-left-offset obstruction in Erdős #776.

The symbolic proof is in ``LEFT_OFFSET_FIVE_OBSTRUCTION.md``.  This program
checks its finite certificate with two independently coded Macaulay engines,
the uncompressed global orbit, and literal stable words at a large dyadic
parameter.  The large-parameter checks are regression guards, not a finite
replacement for the induction in the manuscript.
"""

from __future__ import annotations

import importlib.util
import json
from math import comb
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[4]
INHERITED_ENGINE = (
    ROOT
    / "artifacts"
    / "erdos_master_rotation"
    / "R002"
    / "core_776_635"
    / "776"
    / "verify_rank5_rotation.py"
)
CERTIFICATE = HERE / "left_b5_rank5_counterexample_certificate.json"


def load_inherited_engine():
    spec = importlib.util.spec_from_file_location("inherited_776_b5", INHERITED_ENGINE)
    if spec is None or spec.loader is None:
        raise RuntimeError(INHERITED_ENGINE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


ENGINE = load_inherited_engine()


def canonical(number: int, rank: int) -> list[tuple[int, int]]:
    """Independent greedy combinadic implementation using binary search."""
    if number < 0 or rank < 1:
        raise ValueError((number, rank))
    remaining = number
    ceiling: int | None = None
    result: list[tuple[int, int]] = []
    for lower in range(rank, 0, -1):
        if remaining == 0:
            break
        left = lower - 1
        if ceiling is None:
            right = lower
            while comb(right, lower) <= remaining:
                left = right
                right *= 2
        else:
            right = ceiling
        while left + 1 < right:
            middle = (left + right) // 2
            if comb(middle, lower) <= remaining:
                left = middle
            else:
                right = middle
        if left >= lower:
            result.append((left, lower))
            remaining -= comb(left, lower)
            ceiling = left
    if remaining:
        raise AssertionError((number, rank, remaining, result))
    return result


def upper(number: int, rank: int) -> int:
    return sum(comb(a, lower + 1) for a, lower in canonical(number, rank))


def word_value(word: list[tuple[int, int]]) -> int:
    return sum(comb(a, lower) for a, lower in word)


def local_orbit(raise_fn, j: int = 17) -> dict[str, object]:
    length = 224 * (1 << (j - 1))
    half = length // 2
    b_value = 5
    c_value = half + 3
    tax = length + 2
    x_value = comb(c_value, 3) + comb(4, 2) + 2 - length
    y_value = comb(c_value + 1, 3) + comb(5, 2) + 2 - length
    result: dict[str, object] = {
        "j": j,
        "L": length,
        "h": half,
        "b": b_value,
        "k": b_value - half,
        "c": c_value,
        "M": tax - 221,
        "T": tax,
    }
    for rank in range(3, 7):
        result[f"x{rank}"] = x_value
        result[f"y{rank}"] = y_value
        result[f"x{rank}_word"] = canonical(x_value, rank)
        result[f"y{rank}_word"] = canonical(y_value, rank)
        x_next = raise_fn(x_value, rank) - tax
        y_next = raise_fn(y_value, rank) - tax - 1
        result[f"gamma{rank}"] = y_next - x_value - raise_fn(x_value, rank)
        x_value, y_value = x_next, y_next
    result["x7"] = x_value
    result["y7"] = y_value
    return result


def constants(through: int) -> tuple[dict[int, int], dict[int, int]]:
    a_values = {3: 9}
    b_values = {3: 15}
    for rank in range(3, through):
        a_values[rank + 1] = comb(a_values[rank], 2) + 11 - 6 * rank
        b_values[rank + 1] = comb(b_values[rank], 2) + 12 - 6 * rank
    return a_values, b_values


def stable_word(half: int, rank: int, constant: int, adjacent: bool):
    shift = 1 if adjacent else 0
    word = [(half + 2 + shift, rank)]
    word.extend(
        (half + 3 * lower - 3 * rank + 2 + shift, lower)
        for lower in range(rank - 1, 2, -1)
    )
    word.append((half + 9 - 3 * rank + shift, 2))
    word.append((constant, 1))
    return word


def check_stable_recurrence() -> None:
    a_values, b_values = constants(9)
    assert [a_values[p] for p in range(3, 9)] == [
        9,
        29,
        393,
        77_009,
        2_965_154_511,
        4_396_070_635_569_247_274,
    ]
    assert [b_values[p] for p in range(3, 9)] == [
        15,
        99,
        4_839,
        11_705_523,
        68_509_628_498_979,
        2_346_784_598_534_023_539_487_771_701,
    ]

    half = 112 * (1 << 200)
    tax = 2 * half + 2
    x_value = word_value(stable_word(half, 3, a_values[3], False))
    y_value = word_value(stable_word(half, 3, b_values[3], True))
    for rank in range(3, 8):
        x_word = stable_word(half, rank, a_values[rank], False)
        y_word = stable_word(half, rank, b_values[rank], True)
        assert canonical(x_value, rank) == x_word
        assert canonical(y_value, rank) == y_word
        gamma = upper(y_value, rank) - tax - 1 - x_value - upper(x_value, rank)
        expected = (
            comb(b_values[rank], 2)
            - comb(a_values[rank] + 1, 2)
            - 3
            - 2 * half
        )
        assert gamma == expected
        x_value = upper(x_value, rank) - tax
        y_value = upper(y_value, rank) - tax - 1


def check_first_rank_five_failure() -> None:
    observed = []
    for j in range(2, 18):
        data = local_orbit(upper, j)
        observed.append((j, int(data["gamma5"])))
    assert all(gamma >= 0 for _, gamma in observed[:-1])
    assert observed[-1] == (17, -3_051_947)
    # From j=7 onward the rank-five stable word is literal.
    k5 = 11_628_117
    for j, gamma in observed[5:]:
        length = 224 * (1 << (j - 1))
        assert gamma == k5 - length


def global_surpluses(raise_fn, ambient: int, through: int) -> dict[int, int]:
    f_value = ambient
    g_value = ambient + 1
    result: dict[int, int] = {}
    for rank in range(1, through + 1):
        g_next = raise_fn(g_value, rank) - (ambient + 222)
        result[rank] = g_next - f_value - raise_fn(f_value, rank)
        f_value = raise_fn(f_value, rank) - (ambient + 221)
        g_value = g_next
    return result


def check_certificate() -> None:
    certificate = json.loads(CERTIFICATE.read_text())
    independent = local_orbit(upper)
    inherited = local_orbit(ENGINE.upper_raise)
    for key, expected in certificate.items():
        if key.endswith("_word"):
            expected = [tuple(term) for term in expected]
        if key in independent:
            assert independent[key] == expected, (key, independent[key], expected)
            assert inherited[key] == expected, (key, inherited[key], expected)

    global_one = global_surpluses(upper, certificate["M"], 21)
    global_two = global_surpluses(ENGINE.upper_raise, certificate["M"], 21)
    for rank in (20, 21):
        expected = certificate[f"global_Gamma_{rank}"]
        assert global_one[rank] == global_two[rank] == expected


def check_growth_inequalities() -> None:
    a_values, b_values = constants(12)
    for rank in range(4, 12):
        a_value = a_values[rank]
        b_value = b_values[rank]
        k_value = comb(b_value, 2) - comb(a_value + 1, 2) - 3
        assert a_value * 2 <= b_value
        assert a_value**4 <= b_value**3
        assert b_value**2 // 4 <= k_value <= b_value**2 // 2
        if rank < 11:
            assert 2 * b_values[rank + 1] >= 4 * b_value**2 // 5
            assert 2 * b_values[rank + 1] <= b_value**2


def main() -> None:
    check_certificate()
    check_stable_recurrence()
    check_first_rank_five_failure()
    check_growth_inequalities()
    print(
        json.dumps(
            {
                "status": "PASS",
                "two_macaulay_implementations": True,
                "first_b5_rank5_failure_j": 17,
                "gamma5": -3_051_947,
                "gamma6": 36_463_781_155_415,
                "global_ranks_checked": [20, 21],
                "stable_recurrence_checked_through_rank": 8,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
