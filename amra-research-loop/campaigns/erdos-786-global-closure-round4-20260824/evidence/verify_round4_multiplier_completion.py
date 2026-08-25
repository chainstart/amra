#!/usr/bin/env python3
"""Exact finite guards for the symbolic multiplier-completion theorem MC.1."""

from __future__ import annotations

import json
import math


def check(P: set[int], Q: set[int], start: int, stop: int) -> dict[str, int]:
    assert P and Q and P.isdisjoint(Q) and len(P) != len(Q)
    X = math.prod(P)
    Y = math.prod(Q)
    assert X != Y
    valid = 0
    endpoints: dict[int, int] = {}
    for t in range(start, stop + 1):
        left = P | {t * Y}
        right = Q | {t * X}
        if not left.isdisjoint(right) or len(left) != len(P) + 1 or len(right) != len(Q) + 1:
            continue
        assert math.prod(left) == math.prod(right)
        assert len(left) != len(right)
        valid += 1
        endpoints[t * X] = endpoints.get(t * X, 0) + 1
        endpoints[t * Y] = endpoints.get(t * Y, 0) + 1
    assert max(endpoints.values()) <= 2
    return {
        "X": X,
        "Y": Y,
        "M": max(X, Y),
        "valid_relations": valid,
        "maximum_endpoint_multiplicity": max(endpoints.values()),
    }


def main() -> None:
    rows = [
        check({2, 3}, {5}, 10, 200),
        check({2, 5, 7}, {3, 11}, 10, 200),
        check({3, 7, 13, 17}, {2, 5, 19}, 10, 200),
    ]
    print(json.dumps({
        "status": "PASS",
        "scope": "finite guards for the exact identities and endpoint multiplicity in the symbolic all-parameter proof",
        "rows": rows,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
