#!/usr/bin/env python3
"""Independent exact audit of the round-three conditional reduction.

This deliberately does not import the author-lane checker.  It uses exact
rational arithmetic for Q(sqrt(3)), a bit-mask matching DP, and direct Hall
cut enumeration.  Intended external limit: 2 GiB virtual memory, 120 seconds.
"""

from __future__ import annotations

from fractions import Fraction
from math import comb
import json


def sign_qsqrt3(p: Fraction, q: Fraction) -> int:
    """Return the exact sign of p + q*sqrt(3)."""
    if p == 0:
        return (q > 0) - (q < 0)
    if q == 0:
        return (p > 0) - (p < 0)
    if (p > 0) == (q > 0):
        return 1 if p > 0 else -1
    comparison = p * p - 3 * q * q
    # sqrt(3) is irrational, so equality is impossible for nonzero p,q in Q.
    assert comparison != 0
    if comparison > 0:
        return 1 if p > 0 else -1
    return 1 if q > 0 else -1


def integer_le_surd(k: int, a: Fraction, b: Fraction) -> bool:
    return sign_qsqrt3(a - k, b) >= 0


def exact_floor_surd(a: Fraction, b: Fraction) -> int:
    # Start at floor(a) and move by exact comparisons.  Audit instances are
    # tiny; no floating approximation enters the decision.
    k = a.numerator // a.denominator
    while not integer_le_surd(k, a, b):
        k -= 1
    while integer_le_surd(k + 1, a, b):
        k += 1
    return k


def neighbour_union(rows: tuple[int, ...], subset: int) -> int:
    union = 0
    for left, row in enumerate(rows):
        if subset & (1 << left):
            union |= row
    return union


def hall_deficiency(rows: tuple[int, ...]) -> tuple[int, int]:
    best = -1
    witness = 0
    for subset in range(1 << len(rows)):
        deficit = subset.bit_count() - neighbour_union(rows, subset).bit_count()
        if deficit > best:
            best, witness = deficit, subset
    return best, witness


def matching_number_dp(rows: tuple[int, ...], right_size: int) -> int:
    """Independent maximum matching DP over used-right masks."""
    states = {0}
    for row in rows:
        next_states = set(states)
        for used in states:
            available = row & ~used & ((1 << right_size) - 1)
            while available:
                bit = available & -available
                next_states.add(used | bit)
                available -= bit
        states = next_states
    return max(mask.bit_count() for mask in states)


def hall_holds(rows: tuple[int, ...]) -> bool:
    return all(
        neighbour_union(rows, subset).bit_count() >= subset.bit_count()
        for subset in range(1 << len(rows))
    )


def main() -> None:
    rounding_rows = 0
    for n in range(5, 32, 2):
        e = n * n // 4 + 1
        for b_size in range(min(n, 8) + 1):
            a = Fraction(e, 2) - comb(b_size, 2)
            b = -Fraction(n, 4)
            assert b != 0  # hence a+b*sqrt(3) is irrational
            floor_s = exact_floor_surd(a, b)
            # This compares every sampled integer directly with the surd,
            # rather than comparing the floor predicate with itself.
            for residue in range(floor_s - 3, floor_s + 4):
                assert integer_le_surd(residue, a, b) == (residue <= floor_s)
            assert integer_le_surd(floor_s, a, b)
            assert not integer_le_surd(floor_s + 1, a, b)
            rounding_rows += 1

    graph_count = 0
    size_profile: dict[str, int] = {}
    for left_size in range(5):
        for right_size in range(5):
            local_count = 0
            edge_slots = left_size * right_size
            for graph_mask in range(1 << edge_slots):
                row_limit = (1 << right_size) - 1
                rows = tuple(
                    (graph_mask >> (left * right_size)) & row_limit
                    for left in range(left_size)
                )
                delta, witness = hall_deficiency(rows)
                rank = matching_number_dp(rows, right_size)
                assert delta == left_size - rank

                universal = ((1 << delta) - 1) << right_size
                augmented = tuple(row | universal for row in rows)
                assert hall_holds(augmented)

                if delta:
                    fewer = ((1 << (delta - 1)) - 1) << right_size
                    fewer_rows = tuple(row | fewer for row in rows)
                    # The maximizing old cut witnesses necessity directly.
                    assert neighbour_union(fewer_rows, witness).bit_count() < witness.bit_count()

                graph_count += 1
                local_count += 1
            size_profile[f"{left_size}x{right_size}"] = local_count

    # Count alone is not sufficient for nonuniversal created carriers:
    # D={0,1}, no old carriers, delta=2; two new carriers both see only demand
    # 0, leaving cut {1} without a neighbour.
    old_rows = (0, 0)
    delta, _ = hall_deficiency(old_rows)
    actual_created_rows = (0b11, 0b00)
    assert delta == 2 and len({0, 1}) == delta
    assert not hall_holds(actual_created_rows)

    expected_count = sum(1 << (left * right) for left in range(5) for right in range(5))
    assert graph_count == expected_count == 74_963
    assert rounding_rows == 122

    print(json.dumps({
        "schema": "amra.erdos809.round3.independent-audit.v1",
        "method": {
            "rounding": "exact sign in Q(sqrt(3)); direct integer-to-surd comparison",
            "matching": "used-right-mask dynamic programming",
            "carrier": "direct enumeration of every Hall cut",
            "author_checker_imported": False,
            "lean_used": False
        },
        "rounding_rows": rounding_rows,
        "bipartite_graphs": graph_count,
        "graph_count_interpretation": "labelled bipartite graphs, ordered shore sizes 0..4, including empty shores",
        "size_profile": size_profile,
        "hall_identity_passed": True,
        "universal_delta_necessity_and_sufficiency_passed": True,
        "nonuniversal_delta_count_counterexample_passed": True,
        "public_problem_changed": False,
        "main_term_changed": False
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
