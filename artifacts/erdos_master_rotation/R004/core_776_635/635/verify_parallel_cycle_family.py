#!/usr/bin/env python3
"""Verify the R004 parametric family of parallel all-prime swap edges."""

from __future__ import annotations

import json
from math import isqrt


def is_prime(value: int) -> bool:
    if value < 2:
        return False
    if value % 2 == 0:
        return value == 2
    for divisor in range(3, isqrt(value) + 1, 2):
        if value % divisor == 0:
            return False
    return True


def audit(
    B: int, c: int, p: int, q: int, k: int | None = None
) -> dict[str, object]:
    assert B >= 2 and B & (B - 1) == 0
    assert c >= 4 and c & (c - 1) == 0
    if k is None:
        k = c - 1
    assert k >= 1 and (c - 1) % k == 0
    h = (c - 1) // k
    t = k * B
    translated_p, translated_q = p + t, q + t
    assert (h * p - B) * (h * q - B) == c * B * B - h
    assert all(
        is_prime(value)
        for value in (p, q, translated_p, translated_q)
    )

    first_label = c * B * p * q
    second_label = B * translated_p * translated_q
    assert second_label - first_label == t
    first_endpoints = sorted((first_label - p, first_label - q))
    second_endpoints = sorted(
        (second_label - translated_p, second_label - translated_q)
    )
    assert first_endpoints == second_endpoints

    conflict = first_label % t == 0
    assert conflict == ((p * q) % k == 0)
    return {
        "B": B,
        "c": c,
        "k": k,
        "h": h,
        "translation_t": t,
        "first_scale": c * B,
        "second_scale": B,
        "first_primes": [p, q],
        "translated_primes": [translated_p, translated_q],
        "labels": [first_label, second_label],
        "endpoints": first_endpoints,
        "label_conflict": conflict,
    }


def main() -> None:
    controls = [
        audit(2, 4, 5, 7),
        audit(4, 4, 5, 67),
        audit(8, 4, 13, 59),
        audit(4, 16, 7, 89),
        audit(32, 4, 71, 137),
        audit(4, 4_096, 3, 317, k=455),
        audit(8_192, 64, 2_053, 100_469, k=9),
    ]
    assert all(not row["label_conflict"] for row in controls)
    result = {
        "schema": "amra.erdos635.r004-parallel-cycle-family.v1",
        "status": "PASS",
        "parametric_identity": {
            "hypotheses": (
                "B and c are powers of two with c>=4, "
                "k divides c-1, h=(c-1)/k, t=kB, and "
                "(hp-B)(hq-B)=cB^2-h"
            ),
            "conclusion": (
                "Edges (scale cB, primes p,q) and "
                "(scale B, primes p+t,q+t) have the same endpoints."
            ),
            "label_conflict_criterion": "k divides p*q",
        },
        "all_prime_conflict_free_controls": controls,
        "scope": (
            "This parametrizes genuine all-prime single cycles.  It does "
            "not construct a bicyclic component and does not settle Hall."
        ),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
