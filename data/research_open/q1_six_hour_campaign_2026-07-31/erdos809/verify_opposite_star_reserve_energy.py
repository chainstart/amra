#!/usr/bin/env python3
"""Exhaustive small-graph guard for opposite-star reserve energy."""

from __future__ import annotations

from itertools import combinations


def all_graphs(vertex_count: int):
    pairs = list(combinations(range(vertex_count), 2))
    for mask in range(1 << len(pairs)):
        adjacency = [set() for _ in range(vertex_count)]
        for bit, (x, y) in enumerate(pairs):
            if mask & (1 << bit):
                adjacency[x].add(y)
                adjacency[y].add(x)
        yield adjacency


def is_zero_pair(adjacency: list[set[int]], b: int, c: int) -> bool:
    if c in adjacency[b]:
        return False
    for x in adjacency[b]:
        for y in adjacency[c]:
            if x != y and y in adjacency[x]:
                return False
    return True


def incident_missing_count(
    adjacency: list[set[int]], b_block: set[int], leaves: set[int]
) -> int:
    count = 0
    for x, y in combinations(sorted(b_block), 2):
        if y not in adjacency[x] and (x in leaves or y in leaves):
            count += 1
    return count


def exhaustive_guard(limit: int = 6) -> dict[str, int]:
    graphs = 0
    stars = 0
    subsets = 0
    for n in range(2, limit + 1):
        for adjacency in all_graphs(n):
            graphs += 1
            degrees = [len(neighbours) for neighbours in adjacency]
            delta = min(degrees)
            maximum = max(degrees)
            for v in range(n):
                if degrees[v] != maximum:
                    continue
                a_block = set(adjacency[v]) | {v}
                b_block = set(range(n)) - a_block
                m = len(a_block)
                for b in b_block:
                    leaves = [
                        c
                        for c in b_block
                        if c != b
                        and is_zero_pair(adjacency, b, c)
                        and not (adjacency[b] & adjacency[c])
                    ]
                    if not leaves:
                        continue
                    stars += 1
                    for size in range(1, len(leaves) + 1):
                        for chosen_tuple in combinations(leaves, size):
                            chosen = set(chosen_tuple)
                            ell = len(chosen)
                            q_size = incident_missing_count(
                                adjacency, b_block, chosen
                            )
                            exact_rhs = 0
                            coarse_h = 0
                            coarse_rho = 0
                            for c in chosen:
                                h_c = min(
                                    len(adjacency[b] & a_block),
                                    len(adjacency[c] & a_block),
                                )
                                # Active pairs have h>=1.  Skip an
                                # abstract pair that cannot carry a
                                # colour in this maximum-witness chart.
                                if h_c == 0:
                                    break
                                rho = n - degrees[b] - degrees[c]
                                lam = m + 1 - delta
                                exact_rhs += (
                                    2 * (h_c + rho - lam)
                                    - min(ell - 1, rho - 2)
                                )
                                coarse_h += h_c - 1
                                coarse_rho += rho
                            else:
                                assert 2 * q_size >= exact_rhs
                                coarse_rhs = (
                                    2 * coarse_h
                                    + coarse_rho
                                    - 2 * (m - delta - 1) * ell
                                )
                                assert 2 * q_size >= coarse_rhs
                                subsets += 1
    return {
        "graphs": graphs,
        "opposite_stars": stars,
        "active_leaf_subsets": subsets,
    }


def main() -> None:
    report = exhaustive_guard()
    print(
        {
            "schema": "amra.erdos809.opposite-star-reserve.v1",
            **report,
            "status": "PASS",
            "scope": "small-graph guard only; Erdos #809 remains open",
        }
    )


if __name__ == "__main__":
    main()
