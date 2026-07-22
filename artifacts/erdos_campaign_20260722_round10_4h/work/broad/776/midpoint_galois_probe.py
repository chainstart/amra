#!/usr/bin/env python3
"""Exact midpoint certificates for the #776 colex-capacity cascade.

For N=r+5, the forward tail capacity a_p and the reverse requirement b_p are

    a_3 = C(N,3)-r,       a_(p+1) = U_p(a_p)-r,
    b_(N-2) = 0,          b_p = KK_(p+1)(b_(p+1)+r).

The Macaulay adjunction U_p(x)>=y iff x>=KK_(p+1)(y) makes a_p>=b_p
equivalent at every adjacent rank.  This script compares the two integers at
p=floor(N/2) and records the first differing canonical digit.  It supplies
finite exact evidence only; it does not prove the all-r statement.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from math import comb


def canonical(number: int, rank: int) -> list[tuple[int, int]]:
    result: list[tuple[int, int]] = []
    remaining = number
    cap: int | None = None
    for lower_rank in range(rank, 0, -1):
        if remaining == 0:
            break
        low = lower_rank - 1
        high = cap if cap is not None else max(lower_rank + 1, 2 * lower_rank)
        if cap is None:
            while comb(high, lower_rank) <= remaining:
                high *= 2
        while low + 1 < high:
            middle = (low + high) // 2
            if comb(middle, lower_rank) <= remaining:
                low = middle
            else:
                high = middle
        upper = low
        if cap is not None:
            upper = min(upper, cap - 1)
            while upper >= lower_rank and comb(upper, lower_rank) > remaining:
                upper -= 1
        if upper < lower_rank:
            continue
        result.append((upper, lower_rank))
        remaining -= comb(upper, lower_rank)
        cap = upper
    if remaining:
        raise AssertionError((number, rank, result, remaining))
    return result


def lower_shadow(number: int, rank: int) -> int:
    return sum(comb(upper, lower - 1)
               for upper, lower in canonical(number, rank))


def upper_raise(number: int, rank: int) -> int:
    return sum(comb(upper, lower + 1)
               for upper, lower in canonical(number, rank))


def midpoint_certificate(r: int) -> dict[str, object]:
    n = r + 5
    middle = n // 2

    a = comb(n, 3) - r
    for rank in range(3, middle):
        a = upper_raise(a, rank) - r
        if a < 0:
            raise AssertionError(("negative_forward", r, rank + 1, a))

    b = 0
    for rank in range(n - 3, middle - 1, -1):
        b = lower_shadow(b + r, rank + 1)

    a_digits = canonical(a, middle)
    b_digits = canonical(b, middle)
    common = 0
    while (common < len(a_digits) and common < len(b_digits)
           and a_digits[common] == b_digits[common]):
        common += 1

    a_first = a_digits[common] if common < len(a_digits) else None
    b_first = b_digits[common] if common < len(b_digits) else None
    if not a > b:
        raise AssertionError(("midpoint_failure", r, middle, a, b))
    if a_first is not None and b_first is not None:
        # Canonical expansions are compared lexicographically by upper tops.
        assert a_first[1] == b_first[1]
        assert a_first[0] > b_first[0]

    digest_payload = json.dumps({
        "a": a_digits,
        "b": b_digits,
    }, separators=(",", ":"), sort_keys=True).encode()
    return {
        "r": r,
        "N": n,
        "middle_rank": middle,
        "a_middle": a,
        "b_middle": b,
        "positive_gap": a - b,
        "common_canonical_prefix_length": common,
        "a_first_different_digit": a_first,
        "b_first_different_digit": b_first,
        "canonical_pair_sha256": hashlib.sha256(digest_payload).hexdigest(),
    }


def brute_galois_self_test() -> None:
    """Independent small-box audit of the adjunction used in ATTEMPT.md."""
    for rank in range(1, 7):
        for x in range(30):
            raised = upper_raise(x, rank)
            for y in range(30):
                assert ((raised >= y)
                        == (x >= lower_shadow(y, rank + 1)))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-r", type=int, default=300)
    parser.add_argument(
        "--samples",
        default="20,50,100,101,200,300",
        help="comma-separated rows retained verbatim in the JSON output",
    )
    args = parser.parse_args()
    if args.max_r < 2:
        raise SystemExit("--max-r must be at least 2")

    requested = {int(value) for value in args.samples.split(",") if value}
    brute_galois_self_test()
    rows = []
    prefix_histogram: dict[int, int] = {}
    minimum_gap: int | None = None
    for r in range(2, args.max_r + 1):
        row = midpoint_certificate(r)
        prefix = int(row["common_canonical_prefix_length"])
        gap = int(row["positive_gap"])
        prefix_histogram[prefix] = prefix_histogram.get(prefix, 0) + 1
        minimum_gap = gap if minimum_gap is None else min(minimum_gap, gap)
        if r in requested or r == args.max_r:
            rows.append(row)

    print(json.dumps({
        "schema": "amra.erdos776.midpoint-galois.v1",
        "galois_bruteforce": "PASS ranks=1..6, x,y=0..29",
        "verified_range": [2, args.max_r],
        "all_midpoint_comparisons": "PASS",
        "minimum_positive_gap": minimum_gap,
        "common_prefix_histogram": {
            str(key): value for key, value in sorted(prefix_histogram.items())
        },
        "selected_rows": rows,
        "scope_warning": "Finite exact verification; no all-r proof claim.",
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
