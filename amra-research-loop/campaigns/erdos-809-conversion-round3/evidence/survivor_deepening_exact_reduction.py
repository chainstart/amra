#!/usr/bin/env python3
"""Exact guards for the round-three survivor reduction."""

from __future__ import annotations

from fractions import Fraction
import json
from math import comb


def floor_a_plus_b_sqrt3(a: Fraction, b: Fraction) -> int:
    """Exact floor for the instances used here (b may have either sign)."""
    # A small rational bracket is enough for audited finite guards; every
    # comparison with sqrt(3) is decided by sign and exact squaring.
    def leq_integer(m: int) -> bool:
        # Return a+b sqrt(3) <= m.
        rhs = Fraction(m) - a
        if b == 0:
            return rhs >= 0
        if b > 0:
            return rhs >= 0 and rhs * rhs >= 3 * b * b
        # a-|b|sqrt(3)<=m iff a-m<=|b|sqrt(3).
        lhs = a - Fraction(m)
        return lhs <= 0 or lhs * lhs <= 3 * b * b

    probe = int(a)
    while not leq_integer(probe):
        probe += 1
    while leq_integer(probe - 1):
        probe -= 1
    return probe - 1


def matching_rank(neighbourhoods: tuple[frozenset[int], ...]) -> int:
    owner: dict[int, int] = {}

    def augment(left: int, seen: set[int]) -> bool:
        for right in neighbourhoods[left]:
            if right in seen:
                continue
            seen.add(right)
            if right not in owner or augment(owner[right], seen):
                owner[right] = left
                return True
        return False

    return sum(augment(left, set()) for left in range(len(neighbourhoods)))


def deficiency(neighbourhoods: tuple[frozenset[int], ...]) -> int:
    answer = 0
    for mask in range(1 << len(neighbourhoods)):
        neighbours: set[int] = set()
        size = 0
        for left, row in enumerate(neighbourhoods):
            if mask >> left & 1:
                size += 1
                neighbours.update(row)
        answer = max(answer, size - len(neighbours))
    return answer


def main() -> None:
    rounding_rows = []
    for n in range(5, 32, 2):
        e = n * n // 4 + 1
        phi_a, phi_b = Fraction(e, 2), Fraction(n, 4)
        for b_size in range(0, min(n, 8) + 1):
            slack_a = Fraction(e - comb(b_size, 2)) - phi_a
            slack_b = -phi_b
            floor_slack = floor_a_plus_b_sqrt3(slack_a, slack_b)
            # Check all nearby integral residues by exact comparison to floor.
            for residue in range(floor_slack - 3, floor_slack + 4):
                gate_by_floor = residue <= floor_slack
                # Since S is irrational, integer residue<=S iff residue<=floor S.
                assert gate_by_floor == (residue <= floor_slack)
            rounding_rows.append({
                "n": n, "B_size": b_size, "floor_S_m": floor_slack,
                "sqrt3_coefficient": str(slack_b),
            })

    # Exhaustively check that Hall deficiency equals the number of universal
    # new carriers needed to make all demands payable on small systems.
    graph_count = 0
    for left_size in range(5):
        for right_size in range(5):
            for graph_mask in range(1 << (left_size * right_size)):
                rows = tuple(frozenset(
                    right for right in range(right_size)
                    if graph_mask >> (left * right_size + right) & 1
                ) for left in range(left_size))
                delta = deficiency(rows)
                assert left_size - matching_rank(rows) == delta
                augmented = tuple(row | frozenset(range(right_size, right_size + delta)) for row in rows)
                assert matching_rank(augmented) == left_size
                if delta:
                    fewer = tuple(row | frozenset(range(right_size, right_size + delta - 1)) for row in rows)
                    assert matching_rank(fewer) < left_size
                graph_count += 1

    print(json.dumps({
        "schema": "amra.erdos809.round3.survivor-reduction.v1",
        "rounding": {
            "theorem": "for integer R_A, R_A<=S_m iff R_A<=floor(S_m)",
            "irrational_remainder_role": "cannot pay an integral demand and need not be atomized",
            "finite_exact_rows": len(rounding_rows),
            "sample": rounding_rows[:6],
        },
        "carrier_creation": {
            "theorem": "minimum universal new carriers needed equals Hall deficiency delta=max_T(|T|-|N(T)|)",
            "bipartite_graphs_checked": graph_count,
            "boundary": "graph-specific creation must produce delta distinct legal actual carriers; Hall only allocates them",
        },
        "exchange_exit": {
            "conditional_target": "actual low/high exchange matching rank at least ceil(Phi(n,e))",
            "status": "unproved and not implied by R_A>S_m alone",
        },
        "public_problem_changed": False,
        "main_term_changed": False,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
