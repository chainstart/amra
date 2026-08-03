#!/usr/bin/env python3
"""Independent exact probes for the growing-c #776 audit.

This implementation does not import the author probes.  Finite output is a
guard for the natural proof, not evidence for its unbounded quantifiers.
"""

from fractions import Fraction
from math import comb, isqrt
import json


def upper(number: int, rank: int) -> int:
    assert number >= 0 and rank >= 1
    remainder = number
    ceiling = None
    result = 0
    for lower in range(rank, 0, -1):
        if remainder == 0:
            break
        lo = lower - 1
        hi = ceiling if ceiling is not None else max(lower + 1, 2)
        if ceiling is None:
            while comb(hi, lower) <= remainder:
                hi *= 2
        while lo + 1 < hi:
            mid = (lo + hi) // 2
            if comb(mid, lower) <= remainder:
                lo = mid
            else:
                hi = mid
        if lo >= lower:
            remainder -= comb(lo, lower)
            result += comb(lo, lower + 1)
            ceiling = lo
    assert remainder == 0
    return result


def state(q: int, c: int, r: int, u: int) -> dict[str, int] | None:
    n = comb(q, 2) + r
    b = c * q + comb(c, 2) + u - r + 1
    if b < 1:
        return None
    twice_h = comb(b - 1, 2) + 2 - n
    if twice_h % 2:
        return None
    h = twice_h // 2
    z = comb(q, 3) + comb(r, 2)
    w = comb(q + c, 3) + comb(u, 2)
    cap = comb(b, 2) + 1
    x = n + z - cap + 1
    y = n + w - cap
    delta = w - z - 1
    if min(x, y) < 0:
        return None
    gamma3 = w - z - cap
    gamma4 = upper(y, 3) - upper(x, 3) - z - 1
    assert b == c * q + comb(c, 2) + u - r + 1
    assert y - x == delta
    assert x + (cap - n) == z + 1
    assert gamma4 == upper(y, 3) - upper(x, 3) - x - (cap - n)
    return {
        "q": q, "c": c, "r": r, "u": u, "b": b, "h": h,
        "x": x, "y": y, "z": z, "delta": delta,
        "gamma3": gamma3, "gamma4": gamma4,
    }


def find_nearby(q: int, c: int) -> dict[str, int]:
    for r in range(12):
        for u in range(12):
            row = state(q, c, r, u)
            if row is not None and row["gamma3"] < 0 and row["x"] >= 0:
                return row
    raise AssertionError((q, c))


def main() -> None:
    checked = 0
    nonpositive = 0
    maximum_c_over_sqrt_q = Fraction(0)
    for q in range(24, 101):
        for c in range(2, 14):
            for r in range(q):
                for u in range(q + c):
                    row = state(q, c, r, u)
                    if row is None or row["gamma3"] >= 0:
                        continue
                    checked += 1
                    if row["gamma4"] <= 0:
                        nonpositive += 1
                    # This is only a finite diagnostic for the proved O(sqrt(q)) bound.
                    maximum_c_over_sqrt_q = max(
                        maximum_c_over_sqrt_q,
                        Fraction(c, max(1, isqrt(q))),
                    )

    slow_rows = [find_nearby(q, max(2, isqrt(isqrt(q)))) for q in (256, 1024, 4096, 16384)]
    root_rows = [find_nearby(q, max(2, isqrt(q) // 4)) for q in (256, 1024, 4096, 16384)]

    def summarize(row: dict[str, int]) -> dict[str, object]:
        q, c, delta = row["q"], row["c"], row["delta"]
        return {
            "q": q,
            "c": c,
            "r": row["r"],
            "u": row["u"],
            "delta_over_half_c_q2": [2 * delta, c * q * q],
            "gamma4_sign": 1 if row["gamma4"] > 0 else (0 if row["gamma4"] == 0 else -1),
        }

    # Exact error samples for U3(N)=C*N^(4/3)+O(N) are deliberately omitted:
    # irrational floating evaluation cannot strengthen the symbolic proof.
    output = {
        "schema": "amra.erdos776.independent-growing-c-audit.v1",
        "implementation_independent_of_author_probe": True,
        "finite_guard": {
            "q_range": [24, 100],
            "c_range": [2, 13],
            "admissible_negative_gamma3_rows": checked,
            "nonpositive_gamma4_rows": nonpositive,
            "maximum_c_over_floor_sqrt_q": [maximum_c_over_sqrt_q.numerator, maximum_c_over_sqrt_q.denominator],
        },
        "slow_growing_c_samples": [summarize(row) for row in slow_rows],
        "positive_sqrt_scale_samples": [summarize(row) for row in root_rows],
        "unbounded_inference_from_computation": False,
        "public_problem_closed": False,
    }
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
