#!/usr/bin/env python3
"""Blind direct-orbit audit of the K4,r9 no-fixed-rank theorem.

This checker is standard-library-only and does not import the author verifier.
It reconstructs one actual dyadic member from the original h/q/b formulas,
iterates greedy Macaulay shadows, and compares the resulting full states with
the proposed stable words at every rank in a finite prefix.  The accompanying
audit note supplies the all-rank algebraic induction and quantifier argument.
"""

from __future__ import annotations

from hashlib import sha256
from json import dumps
from math import comb


def C(top: int, lower: int) -> int:
    return comb(top, lower) if top >= lower >= 0 else 0


def canonical(value: int, rank: int) -> tuple[tuple[int, int], ...]:
    """Greedy canonical rank-rank Macaulay expansion."""
    assert value >= 0 and rank >= 1
    remainder = value
    ceiling: int | None = None
    word: list[tuple[int, int]] = []
    for lower in range(rank, 0, -1):
        if remainder == 0:
            break
        lo = lower - 1
        if ceiling is None:
            hi = max(2, lower + 1)
            while C(hi, lower) <= remainder:
                hi *= 2
        else:
            hi = ceiling
        while lo + 1 < hi:
            mid = (lo + hi) // 2
            if C(mid, lower) <= remainder:
                lo = mid
            else:
                hi = mid
        if lo >= lower:
            word.append((lo, lower))
            remainder -= C(lo, lower)
            ceiling = lo
    assert remainder == 0
    return tuple(word)


def word_value(word: tuple[tuple[int, int], ...]) -> int:
    return sum(C(top, lower) for top, lower in word)


def upper(word: tuple[tuple[int, int], ...]) -> int:
    return sum(C(top, lower + 1) for top, lower in word)


def strict_canonical(word: tuple[tuple[int, int], ...]) -> bool:
    return (
        all(top >= lower for top, lower in word)
        and all(word[i][0] > word[i + 1][0] for i in range(len(word) - 1))
    )


def q_of(j: int) -> int:
    assert j >= 1 and j % 2 == 1
    h = 112 * 2 ** (j - 1)
    numerator = 2 * h + 4
    assert numerator % 3 == 0
    q = numerator // 3
    assert q % 2 == 0
    return q


def first_odd_j_above(bound: int) -> int:
    j = max(1, bound.bit_length() - 8)
    if j % 2 == 0:
        j += 1
    while q_of(j) <= bound:
        j += 2
    return j


def constants(last_rank: int) -> tuple[dict[int, int], dict[int, int]]:
    A, B = {4: 25}, {4: 58}
    for n in range(4, last_rank):
        A[n + 1] = C(A[n], 2) - (20 * n - 49)
        B[n + 1] = C(B[n], 2) - (20 * n - 52)
    return A, B


def stable_word(
    q: int, rank: int, constant: int, side: str
) -> tuple[tuple[int, int], ...]:
    H = 5 * q // 2
    if side == "x":
        word = [(H, rank), (q - 1, rank - 1)]
        word.extend(
            (q - (1 + 5 * i), rank - 1 - i)
            for i in range(1, rank - 3)
        )
        word.extend(((q - (5 * rank - 15), 2), (constant, 1)))
    else:
        word = [(H + 1, rank), (q, rank - 1)]
        word.extend(
            (q - 5 * i, rank - 1 - i)
            for i in range(1, rank - 3)
        )
        word.extend(((q - (5 * rank - 16), 2), (constant, 1)))
    return tuple(word)


def main() -> None:
    max_rank = 12
    A, B = constants(max_rank + 1)

    # A single finite maximum realizes the theorem's order and sign choices
    # simultaneously for this audited prefix.  The note proves this construction
    # for arbitrary fixed max_rank.
    bounds = [13]
    for n in range(4, max_rank + 1):
        bounds.extend((A[n] + 5 * n - 15, B[n] + 5 * n - 16))
        gamma_constant = C(B[n], 2) - C(A[n] + 1, 2) + 2
        bounds.append(max(0, gamma_constant // 4))
    chosen_bound = max(bounds)
    j = first_odd_j_above(chosen_bound)
    q = q_of(j)
    h = 112 * 2 ** (j - 1)
    b = q + 4
    tau = C(b, 2) + 1 - (C(q, 2) + 9)
    H = 5 * q // 2

    # Actual-family identities and the raw direct rank-three orbit states.
    assert 2 * h == 3 * q - 4
    assert C(b - 1, 2) + 2 - (C(q, 2) + 9) == 2 * h
    assert tau == 4 * q - 2
    assert h + b - 2 == H
    x = C(h + b - 2, 3) + C(b - 1, 2) + 2 - 2 * h
    y = C(h + b - 1, 3) + C(b, 2) + 2 - 2 * h
    expected_x3 = ((H, 3), (q, 2), (9, 1))
    expected_y3 = ((H + 1, 3), (q + 1, 2), (12, 1))
    assert canonical(x, 3) == expected_x3
    assert canonical(y, 3) == expected_y3

    gammas: dict[int, int] = {}
    checked_words: list[int] = []
    for rank in range(3, max_rank + 1):
        xword = canonical(x, rank)
        yword = canonical(y, rank)
        assert strict_canonical(xword) and strict_canonical(yword)
        if rank >= 4:
            expected_x = stable_word(q, rank, A[rank], "x")
            expected_y = stable_word(q, rank, B[rank], "y")
            assert xword == expected_x
            assert yword == expected_y
            checked_words.append(rank)

        ux, uy = upper(xword), upper(yword)
        gamma = uy - ux - x - tau
        if rank == 3:
            assert gamma == 23 - 4 * q
        else:
            constant = C(B[rank], 2) - C(A[rank] + 1, 2) + 2
            assert gamma == constant - 4 * q
            recurrence_constant = B[rank + 1] - A[rank + 1] - A[rank] - 1
            assert constant == recurrence_constant
        assert gamma < 0
        gammas[rank] = gamma

        next_x, next_y = ux - tau + 1, uy - tau
        assert next_x >= 0 and next_y >= 0
        if rank < max_rank:
            assert canonical(next_x, rank + 1) == stable_word(
                q, rank + 1, A[rank + 1], "x"
            )
            assert canonical(next_y, rank + 1) == stable_word(
                q, rank + 1, B[rank + 1], "y"
            )
        x, y = next_x, next_y

    # Constant positivity and the claimed monotone lower-bound induction.
    A_long, B_long = constants(20)
    assert A_long[5] == 269 and B_long[5] == 1625
    assert A_long[6] == 35995 and B_long[6] == 1319452
    assert A_long[7] == 647801944 and B_long[7] == 870476130358
    for n in range(5, 20):
        assert A_long[n] >= 20 * n and B_long[n] >= 20 * n
        assert A_long[n + 1] > A_long[n] + 20
        assert B_long[n + 1] > B_long[n] + 20

    # Exact recurrence on the actual odd subsequence.
    assert q_of(j + 2) == 4 * q - 4 > q

    result = {
        "schema": "amra.erdos776.adaptive-round4.k4r9-no-fixed-rank-independent-audit.v1",
        "verdict": "pass",
        "engine": "independent standard-library greedy Macaulay direct orbit; no author verifier import",
        "finite_prefix_guard": {
            "max_rank": max_rank,
            "actual_odd_j": j,
            "q_bit_length": q.bit_length(),
            "chosen_bound_bit_length": chosen_bound.bit_length(),
            "stable_word_ranks": checked_words,
            "all_gamma_3_through_R_negative": True,
            "all_next_states_nonnegative": True,
            "gamma_signs_digest": sha256(
                repr(sorted(gammas.items())).encode("utf-8")
            ).hexdigest(),
        },
        "universal_checks": {
            "actual_q_recurrence": "q_(j+2)=4q_j-4>q_j",
            "x_bottom_pascal_gap": "-20n+49",
            "y_bottom_pascal_gap": "-20n+52",
            "gamma_n": "C(B_n,2)-C(A_n+1,2)+2-4q",
            "constant_positivity_induction": "A_n,B_n>=20n for n>=5",
        },
        "quantifiers": "forall fixed R>=4 exists one actual odd j_R with the same member negative at every gamma_3,...,gamma_R",
        "scope": {
            "proves": "no uniform finite recovery rank on the fixed actual K4,r9 odd-j orbit",
            "does_not_prove": [
                "one finite member is negative at every rank",
                "an infinite-rank Macaulay state",
                "the public Erdos-776 antichain statement",
            ],
        },
        "lean_used": False,
    }
    print(dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
