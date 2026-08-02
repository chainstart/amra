#!/usr/bin/env python3
"""Independent blind-audit arithmetic for the final Erdős #776 chamber.

This file deliberately imports no author verifier or Macaulay engine.
"""

from __future__ import annotations

from fractions import Fraction
from functools import cache
from math import comb

import sympy as sp


def canonical(number: int, rank: int) -> tuple[tuple[int, int], ...]:
    if number < 0 or rank < 1:
        raise ValueError((number, rank))
    remainder = number
    cap: int | None = None
    word: list[tuple[int, int]] = []
    for lower in range(rank, 0, -1):
        if remainder == 0:
            break
        low = lower - 1
        high = cap if cap is not None else max(2 * lower, 2)
        if cap is None:
            while comb(high, lower) <= remainder:
                high *= 2
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
    return tuple(word)


@cache
def upper(number: int, rank: int) -> int:
    return sum(comb(top, lower + 1) for top, lower in canonical(number, rank))


def value(word: tuple[tuple[int, int], ...]) -> int:
    return sum(comb(top, lower) for top, lower in word)


def family(exponent: int) -> tuple[int, int, int, int, int]:
    if exponent < 2 or exponent % 4 != 2:
        raise ValueError(exponent)
    h = 224 * 2**exponent
    assert (2 * h - 2) % 5 == 0
    q = (2 * h - 2) // 5
    b = q + 6
    n = comb(q, 2) + 10
    tau = 6 * q + 6
    assert comb(b - 1, 2) + 2 - n == 2 * h
    assert tau == comb(b, 2) + 1 - n == 2 * h + b - 2
    assert 0 <= 10 < q and 0 <= 15 < q + 1 and 31 <= b < h
    assert canonical(n, 2) == ((q, 2), (10, 1))
    assert canonical(n + b - 1, 2) == ((q + 1, 2), (15, 1))
    return h, q, b, n, tau


def orbit(h: int, b: int) -> dict[int, int]:
    cap = h + b - 2
    tau = 2 * h + b - 2
    x = comb(cap, 3) + comb(b - 1, 2) + 2 - 2 * h
    y = comb(cap + 1, 3) + comb(b, 2) + 2 - 2 * h
    result: dict[int, int] = {}
    for rank in range(3, 7):
        ux, uy = upper(x, rank), upper(y, rank)
        result[rank] = uy - ux - x - tau
        x, y = ux - tau + 1, uy - tau
    return result


def chart(q: int) -> dict[str, int]:
    tau = 6 * q + 6
    alpha = comb(q - 7, 2) + 13
    beta = comb(q - 6, 2) + 78
    p = upper(alpha, 2) - tau + 1
    qq = upper(beta, 2) - tau
    p2 = upper(p, 3) - tau + 1
    q2 = upper(qq, 3) - tau
    return {"tau": tau, "alpha": alpha, "beta": beta, "P": p, "Q": qq,
            "P2": p2, "Q2": q2}


def check_family() -> None:
    for exponent in range(16):
        assert ((448 * 2**exponent - 2) % 5 == 0) == (exponent % 4 == 2)

    expected = {
        2: (-2104, 758, 370137, 42058239),
        6: (-34360, -31498, 4268291, 4252643571),
        10: (-550456, -547594, 3752195, 28677939989),
        14: (-8807992, -8805130, -4505341, 3088969555650),
        18: (-140928568, -140925706, -136625917, 9258623982887),
    }
    for exponent, row in expected.items():
        h, q, b, _, _ = family(exponent)
        got = orbit(h, b)
        assert tuple(got[rank] for rank in range(3, 7)) == row
        assert got[3] == 44 - 6 * q
        assert got[4] == 2906 - 6 * q
        if q >= 2948:
            assert got[5] == 4302695 - 6 * q

    assert 4302695 - 6 * 717115 == 5
    assert 4302695 - 6 * 717116 == -1
    assert family(10)[1] < 717116 <= family(14)[1]

    for exponent in (14, 18, 22):
        _, q, _, _, _ = family(exponent)
        state = chart(q)
        assert 40 - 6 * q < 99 - 6 * q < 0
        assert state["P"] > 0 and state["Q"] > 0
        assert canonical(state["alpha"], 2) == ((q - 7, 2), (13, 1))
        assert canonical(state["beta"], 2) == ((q - 6, 2), (78, 1))
        assert canonical(state["P"], 3) == ((q - 8, 3), (q - 14, 2), (4, 1))
        assert canonical(state["Q"], 3) == ((q - 7, 3), (q - 13, 2), (2934, 1))

    _, q14, _, _, _ = family(14)
    state14 = chart(q14)
    assert canonical(state14["P2"], 4) == (
        (q14 - 8, 4), (q14 - 15, 3), (q14 - 22, 2), (q14 - 132, 1)
    )
    assert canonical(state14["Q2"], 4) == (
        (q14 - 7, 4), (q14 - 14, 3), (q14 - 18, 2), (1366627, 1)
    )

    for q in (4302621, family(18)[1], 100000000):
        state = chart(q)
        assert canonical(state["P2"], 4) == (
            (q - 8, 4), (q - 15, 3), (q - 22, 2), (q - 132, 1)
        )
        assert canonical(state["Q2"], 4) == (
            (q - 7, 4), (q - 14, 3), (q - 20, 2), (4302600, 1)
        )
        gamma6 = upper(state["Q2"], 4) - upper(state["P2"], 4) - state["P2"] - state["tau"]
        assert gamma6 == comb(4302600, 2) + 104 * q - 8421 > 0


def loss(rank: int, cap: int, deficit: int) -> int:
    return comb(cap, rank + 1) - upper(comb(cap, rank) - deficit, rank)


def check_deficit_and_tail_arithmetic() -> None:
    for rank in (2, 3):
        for cap in range(rank + 1, 12):
            c = comb(cap, rank)
            vals = [loss(rank, cap, d) for d in range(c + 1)]
            for d in range(c + 1):
                assert vals[d] >= upper(d, rank)
                assert loss(rank, cap + 1, d) - vals[d] <= d
            for e in range(c + 1):
                for d in range(e, c + 1):
                    assert vals[d] - vals[e] >= upper(d - e, rank)

    # Independent exact checks of both analytic anchors and of the slack in
    # the displayed derivative lower bounds.
    sa, ta = Fraction(812, 25), Fraction(1023, 25)
    assert (sa + 3) ** 2 < 1259 and ta**3 < 2 * sa**3 - 6
    assert ((ta - 4) ** 4 / 24 + sa**3 / 3 - 2
            - Fraction(422 * 421, 2)) == Fraction(51111641, 9375000)
    variable = sp.symbols("variable", positive=True)
    lower_a = (
        3 * variable**2 / (2 * (variable + 3))
        * (1 + sp.Rational(243, 640) * variable)
        - (variable**2 + 6 * variable + 16) / 3
        + sp.Rational(1, 2)
    )
    claimed_a = (
        sp.Rational(437, 5250) * variable**2
        - 2 * variable
        - sp.Rational(29, 6)
    )
    slack_a = 3 * variable**2 * (11421 * variable + 18688) / (
        224000 * (variable + 3)
    )
    assert sp.factor(lower_a - claimed_a - slack_a) == 0

    sb, tb = Fraction(3789, 100), Fraction(3759, 125)
    assert (sb + 3) ** 2 < 1672 and tb**3 < sb**3 / 2 - 3
    assert ((tb - 4) ** 4 / 12 - Fraction(278 * 277, 2) - 1
            ) == Fraction(2674108561, 2929687500)
    assert Fraction(437, 5250) * 32**2 - 64 - Fraction(29, 6) > 0
    coefficient = Fraction(450179, 2099520)
    assert (coefficient - Fraction(1, 6)) * 37**2 - 37 - Fraction(1, 3) > 0
    lower_b = (
        variable**2 / (2 * (variable + 3))
        * sp.Rational(3, 4) * variable * sp.Rational(23, 27) ** 3
        - ((variable**2 + 6 * variable + 5) / 6 - sp.Rational(1, 2))
    )
    claimed_b = (
        (sp.Rational(450179, 2099520) - sp.Rational(1, 6)) * variable**2
        - variable
        - sp.Rational(1, 3)
    )
    slack_b = 12167 * variable**2 * (variable - 37) / (
        699840 * (variable + 3)
    )
    assert sp.factor(lower_b - claimed_b - slack_b) == 0

    best_a: tuple[int, int, int, int] | None = None
    for w in range(32, 422):
        total = 3 * w - 7
        for x in range(total + 1):
            promoted = upper(x, 2) + upper(total - x, 2) - 1
            candidate = (upper(promoted, 3) + promoted - comb(w, 2) - 1,
                         w, x, promoted)
            best_a = candidate if best_a is None else min(best_a, candidate)
    assert best_a == (178, 32, 40, 215)

    best_b: tuple[int, int, int, int] | None = None
    for r in range(32, 278):
        total = upper(3 * r + 2, 2) - 1
        for d in range(total + 1):
            candidate = (upper(d, 3) + upper(total - d, 3) - comb(r, 2) - 1,
                         r, d, total)
            best_b = candidate if best_b is None else min(best_b, candidate)
    assert best_b == (258, 32, 188, 384)


def check_small_double_negative_base() -> None:
    antecedents = 0
    single: list[tuple[int, int, int, int, int, int]] = []
    double: list[tuple[int, int, int, int, int, int]] = []
    for q in range(2, 216):
        for k in range(4, q + 2):
            for r in range(q - k + 2):
                twice_h = (k - 1) * q + comb(k - 1, 2) + 2 - r
                if twice_h % 2:
                    continue
                h, b = twice_h // 2, q + k
                if h < 224 or b >= h:
                    continue
                tau = k * q + comb(k, 2) + 1 - r
                u = r + k - 1
                rr = comb(r + 1, 2) - k * q - comb(k, 2)
                ss = rr + comb(u, 2) - comb(r, 2) - 1
                x0, y0 = comb(q, 3) + rr, comb(q + 1, 3) + ss
                gamma3 = (k - 1) * r - k * (q + 1)
                gamma4 = upper(y0, 3) - upper(x0, 3) - x0 - tau
                if gamma3 >= 0 or x0 < 0 or gamma4 >= 0:
                    continue
                antecedents += 1
                if not (rr < ss < 0):
                    continue
                alpha, beta = comb(q - 1, 2) + rr, comb(q, 2) + ss
                if canonical(x0, 3)[0] != (q - 1, 3) or canonical(y0, 3)[0] != (q, 3):
                    continue
                p, qq = upper(alpha, 2) - tau + 1, upper(beta, 2) - tau
                if p >= 0:
                    continue
                x1, y1 = upper(x0, 3) - tau + 1, upper(y0, 3) - tau
                gamma5 = upper(y1, 4) - upper(x1, 4) - x1 - tau
                record = (gamma5, q, k, r, b, h)
                (single if qq >= 0 else double).append(record)
    assert antecedents == 133
    assert single == [(4923, 35, 13, 0, 48, 244)]
    assert double == [
        (4222, 34, 13, 0, 47, 238),
        (4599, 36, 14, 0, 50, 274),
        (9010, 41, 16, 0, 57, 361),
    ]


def main() -> None:
    check_family()
    check_deficit_and_tail_arithmetic()
    check_small_double_negative_base()
    print("ERDOS776 FINAL-CHAMBER BLIND ARITHMETIC: PASS")
    print("first_negative_s 14")
    print("first_negative_gamma5 -4505341")
    print("first_negative_gamma6 3088969555650")
    print("stable_rank6_q 4302621")


if __name__ == "__main__":
    main()
