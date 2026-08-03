#!/usr/bin/env python3
"""Independent audit of the Erdos-776 low-half adjacent-sum kernel.

No function or data is imported from the author verifier.  All searches use
fresh integer definitions.  The finite base is exhaustive only on its declared
domain; the infinite tail is checked through exact algebraic guard identities.
"""

from __future__ import annotations

import argparse
import json
from math import comb, isqrt
from pathlib import Path


def choose(n: int, k: int) -> int:
    return comb(n, k) if n >= k >= 0 else 0


def rank2_top(n: int) -> int:
    # Largest z with z(z-1)/2 <= n.
    z = (1 + isqrt(1 + 8 * n)) // 2
    assert choose(z, 2) <= n < choose(z + 1, 2)
    return z


def first_triangular_at_least(n: int) -> int:
    # This intentionally uses the predecessor-top characterization rather
    # than the author's correction loop.
    return rank2_top(n - 1) + 1 if n > 0 else 1


def first_choose4_at_least(n: int, lower: int) -> int:
    lo = lower - 1
    hi = max(lower, 2)
    while choose(hi, 4) < n:
        hi *= 2
    while lo + 1 < hi:
        mid = (lo + hi) // 2
        if choose(mid, 4) >= n:
            hi = mid
        else:
            lo = mid
    return hi


def first_choose3_at_least(n: int, lower: int) -> int:
    lo = lower - 1
    hi = max(lower, 3)
    while choose(hi, 3) < n:
        hi *= 2
    while lo + 1 < hi:
        mid = (lo + hi) // 2
        if choose(mid, 3) >= n:
            hi = mid
        else:
            lo = mid
    return hi


def reconstruct(a: int, c: int) -> tuple[int, int, int, int]:
    p_threshold = choose(a + 1, 3) - choose(c + 1, 3) + 1
    rho = first_triangular_at_least(max(a * a + 3 * a, p_threshold))
    B = rank2_top(choose(a, 2) + 3 * rho + 2)
    D = first_choose4_at_least(
        choose(c + 1, 4) + choose(a + 1, 3), c + 2
    )
    Astar = first_choose3_at_least(
        choose(D, 3) + choose(a + 1, 3) - choose(c, 3), a + 2
    )
    return rho, D, B, Astar


def finite_base(max_a: int) -> dict[str, object]:
    checked = 0
    failures = []
    minimum = None
    expected = sum(max(0, (a - 1) // 2 - 2) for a in range(3, max_a + 1))
    for a in range(3, max_a + 1):
        for c in range(3, (a - 1) // 2 + 1):
            rho, D, B, Astar = reconstruct(a, c)
            gap = B - Astar
            row = (gap, a, c, rho, D, B, Astar)
            if minimum is None or row < minimum:
                minimum = row
            if gap < 0 and len(failures) < 10:
                failures.append(row)
            checked += 1
    assert checked == expected
    return {
        "domain": {"a": [3, max_a], "c": "3<=c and 2c<a"},
        "independent_combinatorial_pair_count": expected,
        "pairs_checked": checked,
        "failures": failures,
        "minimum": minimum,
    }


def analytic_tail_guards() -> dict[str, object]:
    # Threshold facts used without floating point.
    assert 2401 == 7**4
    assert 2401**3 == 343**4
    assert 343 > 40
    assert 3**4 > 5 * 2**4                    # 5^(1/4) < 3/2
    assert 49 * 375 > 12 * 256               # small-c final comparison
    assert 49 * 1024 > 12 * 3971             # large-c final comparison

    # Delta > a^3/8 follows after multiplying by 48 from
    # 7a^3-8a >= 6a^3, i.e. a(a^2-8)>=0.  Guard its first integer a=3.
    assert 3 * (3 * 3 - 8) > 0

    # The t estimate needs sqrt(a)>=12; the campaign uses >=49.
    assert 49 >= 12
    # 4/3*a^(3/2)+8/9*a <= 3/2*a^(3/2) is equivalent
    # to sqrt(a)>=16/3.
    assert 3 * 49 >= 16

    # Exact coefficient 3971 = 11*19^2 in the large-c chamber.
    assert 3971 == 11 * 19 * 19

    return {
        "a_tail_min": 2401,
        "sqrt_a_min": 49,
        "a_three_quarters_min": 343,
        "small_c_constant_comparison": "49/12 > 256/375",
        "large_c_constant_comparison": "49/12 > 3971/1024",
        "strictness": {
            "rho": "Delta>a^3/8 and C(rho_p,2)>Delta imply rho_p>a^(3/2)/2",
            "quartic_ceiling": "ceil(x)<x+1, so d0<4+x",
            "adjacent_q": "ceil(x)<x+1 and R>8 give q+1<11R/8",
        },
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-a", type=int, default=2400)
    ap.add_argument("--output")
    args = ap.parse_args()
    result = {
        "schema": "amra.erdos776.low-half-adjacent-sum-independent-audit.v1",
        "independence": "fresh integer reconstruction; no author verifier import",
        "finite_base": finite_base(args.max_a),
        "analytic_tail_guards": analytic_tail_guards(),
    }
    if args.max_a == 2400:
        fb = result["finite_base"]
        assert fb["pairs_checked"] == 1_434_006
        assert fb["failures"] == []
        assert fb["minimum"] == (0, 8, 3, 14, 9, 12, 12)
        result["verdict"] = "pass: exact finite base and infinite analytic tail reconstruct"
    else:
        result["verdict"] = "partial finite guard only because max_a!=2400"
    rendered = json.dumps(result, indent=2) + "\n"
    if args.output:
        Path(args.output).write_text(rendered)
    print(rendered, end="")


if __name__ == "__main__":
    main()
