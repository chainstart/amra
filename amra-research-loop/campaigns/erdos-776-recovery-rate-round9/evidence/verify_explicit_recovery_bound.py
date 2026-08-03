#!/usr/bin/env python3
"""Exact guards for p(j)=2+ceil(log2(j+4))."""

import json
from math import comb


def q_of(j: int) -> int:
    assert j >= 1 and j % 2 == 1
    return (224 * (1 << (j - 1)) + 4) // 3


def bound(j: int) -> int:
    # ceil(log2(j+4))=(j+3).bit_length().
    return 2 + (j + 3).bit_length()


def main() -> None:
    b = 1625
    rows = []
    assert b > 2**10
    for n in range(5, 21):
        assert b >= 20 * n
        exponent = 2 + 2 ** (n - 2)
        assert b >= 2**exponent
        margin4 = b * b - 2 * b - 80 * n + 208
        assert margin4 > 0
        rows.append({
            "rank": n,
            "B_bit_length": b.bit_length(),
            "lower_exponent": exponent,
            "taxed_square_margin_positive": True,
        })
        b = comb(b, 2) - (20 * n - 52)

    checks = []
    for j in list(range(1, 402, 2)) + [1231, 4943, 39585, 10**6 + 1]:
        p = bound(j)
        assert 2 ** (p - 2) >= j + 4
        assert q_of(j) < 2 ** (j + 6)
        exponent = 2 + 2 ** (p - 2)
        assert exponent >= j + 6
        checks.append({"j": j, "p_bound": p, "q_bit_length": q_of(j).bit_length()})

    assert bound(1) == 5 and bound(3) == 5 and bound(5) == 6
    print(json.dumps({
        "schema": "amra.erdos776.round9.explicit-recovery-bound.v1",
        "verdict": "PASS",
        "bound": "p(j)=2+ceil(log2(j+4))",
        "constant_rows": rows,
        "strip_checks": len(checks),
        "selected": [checks[0], checks[1], checks[2], checks[-4], checks[-3], checks[-2], checks[-1]],
        "scope_warning": "member-dependent fixed K4,r9 bound only; no uniform rank, rank-42 theorem, suffix, or public closure",
    }, indent=2))


if __name__ == "__main__":
    main()
