#!/usr/bin/env python3
"""Finite arithmetic guards for weighted #809 synchronization."""

from __future__ import annotations

from math import ceil
import random


def audit_support_system(
    supports: list[set[int]],
    weights: list[int],
    d_zero: int,
    m_a: int,
) -> dict[str, int]:
    """Check the weighted incidence/Cauchy chain in an abstract system.

    Each matching index must occur in at least d_zero missing-anchor
    supports.  The chosen Q size is the least square-scale integer that
    satisfies both the anchor-rectangle and A-rectangle premises.
    """

    if not supports or not weights:
        raise ValueError("nonempty supports and weights required")
    if d_zero <= 0 or m_a <= 0:
        raise ValueError("positive d_zero and M_A required")
    f = len(weights)
    if any(weight <= 0 for weight in weights):
        raise ValueError("weights must be positive")
    occurrence = [0] * f
    for support in supports:
        for index in support:
            occurrence[index] += 1
    if min(occurrence) < d_zero:
        raise ValueError("each index needs at least d_zero supports")

    max_support = max(len(support) for support in supports)
    square_h = sum(weight * weight for weight in weights)
    q_root = max(max_support, ceil(square_h / m_a))
    q_size = q_root * q_root

    weighted_supports = [
        sum(weights[index] for index in support)
        for support in supports
    ]
    total_h = sum(weights)
    missing_count = len(supports)
    best_weight = max(weighted_supports)

    assert sum(weighted_supports) >= d_zero * total_h
    assert best_weight * missing_count >= d_zero * total_h
    assert max_support * max_support <= q_size
    assert square_h <= m_a * q_root
    assert (
        d_zero * d_zero * total_h * total_h
        <= missing_count * missing_count * m_a * q_size
    )

    return {
        "matching_size": f,
        "missing_anchors": missing_count,
        "d_zero": d_zero,
        "sum_h": total_h,
        "sum_h2": square_h,
        "M_A": m_a,
        "Q": q_size,
        "best_weighted_support": best_weight,
    }


def deterministic_audit() -> dict[str, int]:
    supports = [
        {0, 1, 2},
        {0, 1},
        {0, 2},
        {1, 2},
        {0, 1, 2},
    ]
    return audit_support_system(
        supports=supports,
        weights=[2, 5, 7],
        d_zero=4,
        m_a=9,
    )


def random_audits(seed: int = 809_35, trials: int = 10_000) -> int:
    rng = random.Random(seed)
    for _ in range(trials):
        f = rng.randint(1, 30)
        missing_count = rng.randint(1, 40)
        d_zero = rng.randint(1, missing_count)
        supports = [set() for _ in range(missing_count)]
        for index in range(f):
            for anchor in rng.sample(range(missing_count), d_zero):
                supports[anchor].add(index)
            for anchor in range(missing_count):
                if rng.random() < 0.15:
                    supports[anchor].add(index)
        weights = [rng.randint(1, 80) for _ in range(f)]
        m_a = rng.randint(1, 300)
        audit_support_system(supports, weights, d_zero, m_a)
    return trials


def main() -> None:
    deterministic = deterministic_audit()
    random_count = random_audits()
    print(
        {
            "schema": "amra.erdos809.weighted-synchronization.v1",
            "deterministic_sum_h": deterministic["sum_h"],
            "deterministic_Q": deterministic["Q"],
            "random_systems": random_count,
            "status": "PASS",
            "scope": "finite arithmetic guards only; Erdos #809 remains open",
        }
    )


if __name__ == "__main__":
    main()
