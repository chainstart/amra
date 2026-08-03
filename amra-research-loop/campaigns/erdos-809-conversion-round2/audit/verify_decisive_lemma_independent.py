#!/usr/bin/env python3
"""Blind arithmetic and finite Hall audit of the round-two decisive lemma.

This checker imports no campaign evidence and uses exact rational arithmetic.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations
import json
from math import comb


def phi_qsqrt3(n: int) -> tuple[Fraction, Fraction, int]:
    """Return Phi=a+b*sqrt(3) at e=floor(n^2/4)+1 for odd n."""
    if n % 2 != 1:
        raise ValueError("odd n required")
    e = n * n // 4 + 1
    radicand = Fraction(e) - Fraction(n * n, 4)
    assert radicand == Fraction(3, 4)
    return Fraction(e, 2), Fraction(n, 4), e


def maximum_matching(neighbourhoods: tuple[frozenset[int], ...]) -> int:
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


def hall_deficiency(neighbourhoods: tuple[frozenset[int], ...]) -> int:
    size = len(neighbourhoods)
    answer = 0
    for mask in range(1 << size):
        neighbours: set[int] = set()
        selected = 0
        for left in range(size):
            if mask >> left & 1:
                selected += 1
                neighbours.update(neighbourhoods[left])
        answer = max(answer, selected - len(neighbours))
    return answer


def exhaustive_hall_guard(max_left: int = 4, max_right: int = 4) -> int:
    tested = 0
    for left_size in range(max_left + 1):
        for right_size in range(max_right + 1):
            edge_count = left_size * right_size
            for graph_mask in range(1 << edge_count):
                rows = []
                for left in range(left_size):
                    rows.append(frozenset(
                        right for right in range(right_size)
                        if graph_mask >> (left * right_size + right) & 1
                    ))
                neighbourhoods = tuple(rows)
                unpaid = left_size - maximum_matching(neighbourhoods)
                assert unpaid == hall_deficiency(neighbourhoods)
                tested += 1
    return tested


def main() -> None:
    odd_rows = []
    for n in range(3, 32, 2):
        rational, sqrt3_coefficient, e = phi_qsqrt3(n)
        assert sqrt3_coefficient != 0
        # For every integer b=|B|, S_m has sqrt(3)-coefficient -n/4.
        for b_size in range(n + 1):
            slack_rational = Fraction(e - comb(b_size, 2)) - rational
            slack_sqrt3 = -sqrt3_coefficient
            assert slack_sqrt3 != 0
            _ = slack_rational
        odd_rows.append({
            "n": n, "e": e,
            "Phi": f"{rational}+({sqrt3_coefficient})*sqrt(3)",
            "S_m_sqrt3_coefficient": str(-sqrt3_coefficient),
        })

    # Independently reconstruct the n=14 scalar counterprofile.
    n, e = 14, 50
    radicand = Fraction(e) - Fraction(n * n, 4)
    assert radicand == 1
    phi14 = Fraction(e, 2) + Fraction(n, 2)
    slack14 = Fraction(e - comb(3, 2)) - phi14
    assert phi14 == 32 and slack14 == 15
    internal_low, i_mix, n_int = 8, 8, 0
    residue = internal_low + i_mix - n_int
    assert residue == 16 > slack14
    assert internal_low < phi14 and i_mix < phi14

    # The direct exit is an integer-threshold implication: I_mix distinct
    # colours with injective compatible anchors reach Phi iff I_mix>=ceil Phi.
    # Test the nonintegral odd-n thresholds exactly in Q(sqrt(3)) by safe
    # integer bracketing using integer squares.
    threshold_rows = []
    for n in range(3, 32, 2):
        a, b, e = phi_qsqrt3(n)
        candidate = 0
        while True:
            # candidate >= a+b*sqrt(3); here b>0. Compare squares exactly.
            delta = Fraction(candidate) - a
            if delta >= 0 and delta * delta >= 3 * b * b:
                break
            candidate += 1
        previous_delta = Fraction(candidate - 1) - a
        assert previous_delta < 0 or previous_delta * previous_delta < 3 * b * b
        threshold_rows.append({"n": n, "ceil_Phi": candidate})

    graph_count = exhaustive_hall_guard()
    tight = (frozenset((0, 1)),) * 3
    paid = (frozenset((0, 1)), frozenset((0, 1)), frozenset((0, 1, 2)))
    assert maximum_matching(tight) == 2 and hall_deficiency(tight) == 1
    assert maximum_matching(paid) == 3 and hall_deficiency(paid) == 0

    print(json.dumps({
        "schema": "amra.erdos809.conversion-round2.independent-audit.v1",
        "M809C-05": {
            "verdict": "refutation_passes_in_exact_unweighted_form",
            "derivation": (
                "odd n gives e=(n^2+3)/4 and e-n^2/4=3/4, hence "
                "Phi=e/2+n*sqrt(3)/4; S_m has nonzero sqrt(3) coefficient -n/4"
            ),
            "finite_guard": odd_rows,
            "scope": "does not refute weighted mass or an integer rounded ledger",
        },
        "M809C-08": {
            "verdict": "direct_subcase_passes_conditionally_on_inherited_anchor_interface",
            "logic": (
                "I_mix counts distinct colours; their unique high internal anchors are "
                "injective by colour and lie in the common compatible high-edge family. "
                "Thus I_mix>=ceil(Phi) supplies at least Phi compatible colours."
            ),
            "ceil_guards": threshold_rows,
            "counterprofile": {
                "Phi": 32, "S_m": 15, "internal_low": 8,
                "I_mix": 8, "N_int": 0, "R_A": residue,
            },
            "boundary": "the counterprofile is scalar-logical, not graph-realizable evidence",
        },
        "M809C-11": {
            "verdict": "conditional_Hall_boundary_passes",
            "theorem": "unpaid=|D|-nu=max_T(|T|-|N(T)|)",
            "exhaustive_bipartite_graphs": graph_count,
            "tight": {"matching": 2, "deficiency": 1},
            "paid": {"matching": 3, "deficiency": 0},
            "boundary": "requires an explicit finite carrier set and proved legal arcs; Hall creates neither",
        },
        "public_problem_changed": False,
        "main_term_changed": False,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
