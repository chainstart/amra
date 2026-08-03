#!/usr/bin/env python3
"""Small exact guards for the typed-cut no-go.

The script enumerates scalar opposite-star conservation profiles. It does not
enumerate graphs and does not prove anything beyond the displayed identities.
"""

import json
from itertools import combinations
from math import comb


def main():
    profiles = []
    duplicated_profiles = 0
    maximum_duplication_gap = 0
    for ell in range(1, 7):
        possible_edges = list(combinations(range(ell), 2))
        for mask in range(1 << len(possible_edges)):
            edges = [edge for index, edge in enumerate(possible_edges) if mask & (1 << index)]
            degrees = [0] * ell
            for x, y in edges:
                degrees[x] += 1
                degrees[y] += 1
            t = sum(degree == 0 for degree in degrees)
            mu = comb(ell, 2) - len(edges)
            for e_a in range(4):
                for e_b in range(4):
                    rhs = 2 * mu + e_a + e_b
                    a_l = rhs - ell * (t - 1)
                    # This equals ell*(ell-t)-2e(L)+E_A+E_B, the literal
                    # leaf-deficit count, so these profiles realize the leaf-graph
                    # part of the conservation identity.
                    direct_a_l = ell * (ell - t) - 2 * len(edges) + e_a + e_b
                    assert a_l == direct_a_l >= 0
                    literal_distinct_capacity = mu + e_a + e_b
                    gap = rhs - literal_distinct_capacity
                    assert gap == mu
                    if mu:
                        duplicated_profiles += 1
                        maximum_duplication_gap = max(maximum_duplication_gap, gap)
                        if len(profiles) < 12:
                            profiles.append({
                                "ell": ell,
                                "leaf_edges": edges,
                                "t": t,
                                "mu": mu,
                                "E_A": e_a,
                                "E_B": e_b,
                                "A_L": a_l,
                                "conserved_demand": rhs,
                                "literal_distinct_capacity": literal_distinct_capacity,
                                "duplication_gap": gap,
                            })

    # Coarse A/B flow has exactly four source-side choices for its two
    # independent demand nodes; it cannot name same/opposite geometry.
    coarse_cut_types = [
        "cut both source arcs: R_A + D_B",
        "pay A slack, cut B source: S_m + D_B",
        "cut A source, pay B reserve: R_A + |Q|",
        "pay both scalar capacities: S_m + |Q|",
    ]
    print(json.dumps({
        "pass": True,
        "duplicated_profiles": duplicated_profiles,
        "maximum_duplication_gap": maximum_duplication_gap,
        "sample_profiles": profiles,
        "coarse_cut_types": coarse_cut_types,
        "interpretation": "The coefficient 2 on mu is conservation multiplicity, not two disjoint missing-edge tokens. A literal additive resource network is short by mu; duplicating mu arcs spends the same Q edge twice.",
        "scope": "small exact leaf-graph/conservation guard only; no full BCM realization is claimed"
    }, indent=2))


if __name__ == "__main__":
    main()
