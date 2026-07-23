#!/usr/bin/env python3
"""Compute exact h(n!) for small n in Erdős Problem #18.

For a practical integer m, h(m) is the least k such that every integer in
[0,m) is a sum of at most k distinct divisors of m.  Python integers are used
as bitsets: bit s in layer j records that s is a sum of exactly j divisors.
The calculation is finite evidence only and does not address asymptotic bounds.
"""

from __future__ import annotations

import argparse
import json
from math import factorial, isqrt
from pathlib import Path


def divisors(number: int) -> list[int]:
    lower: list[int] = []
    upper: list[int] = []
    for divisor in range(1, isqrt(number) + 1):
        if number % divisor != 0:
            continue
        lower.append(divisor)
        if divisor * divisor != number:
            upper.append(number // divisor)
    return lower + upper[::-1]


def exact_h(number: int, max_terms: int) -> dict[str, object]:
    available = divisors(number)
    mask = (1 << number) - 1
    layers = [0] * (max_terms + 1)
    layers[0] = 1
    for divisor in available:
        for terms in range(max_terms, 0, -1):
            layers[terms] |= (layers[terms - 1] << divisor) & mask

    covered = 0
    least_missing_by_budget: list[int | None] = []
    answer: int | None = None
    for terms, layer in enumerate(layers):
        covered |= layer
        missing = (~covered) & mask
        least_missing = None
        if missing:
            least_missing = (missing & -missing).bit_length() - 1
        least_missing_by_budget.append(least_missing)
        if missing == 0:
            answer = terms
            break
    return {
        "number": number,
        "divisor_count": len(available),
        "h": answer,
        "least_missing_by_budget": least_missing_by_budget,
        "complete": answer is not None,
    }


def verify(first_n: int, last_n: int, max_terms: int) -> dict[str, object]:
    rows: list[dict[str, object]] = []
    for n in range(first_n, last_n + 1):
        row = exact_h(factorial(n), max_terms)
        row["n"] = n
        rows.append(row)
    complete = all(bool(row["complete"]) for row in rows)
    recurrence_verified = complete and all(
        int(right["h"]) <= int(left["h"]) + 1
        for left, right in zip(rows, rows[1:])
    )
    return {
        "schema_version": "amra.erdos18.small_factorials.v1",
        "problem_id": "18",
        "range": {"first_n": first_n, "last_n": last_n},
        "rows": rows,
        "recurrence_h_next_at_most_h_plus_one_verified": recurrence_verified,
        "passed": complete and recurrence_verified,
        "scope_note": (
            "Exact finite subset-sum computation only; it provides no asymptotic "
            "upper bound for h(n!)."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--first-n", type=int, default=3)
    parser.add_argument("--last-n", type=int, default=10)
    parser.add_argument("--max-terms", type=int, default=16)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    payload = verify(args.first_n, args.last_n, args.max_terms)
    rendered = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0 if payload["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
