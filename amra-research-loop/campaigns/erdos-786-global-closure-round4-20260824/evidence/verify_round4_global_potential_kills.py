#!/usr/bin/env python3
"""Finite guards for the symbolic graph-product constructions in Round 4."""

from __future__ import annotations

import json
import math


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    r = math.isqrt(n)
    f = 3
    while f <= r:
        if n % f == 0:
            return False
        f += 2
    return True


def primes_in_interval(lo: int, hi: int, count: int) -> list[int]:
    ans = []
    n = lo | 1
    while n < hi and len(ans) < count:
        if is_prime(n):
            ans.append(n)
        n += 2
    assert len(ans) == count
    return ans


def ceil_log2(n: int) -> int:
    return (n - 1).bit_length()


def padded_relation(vertices: int, edges: list[tuple[int, int]], labels: list[int], K: int):
    shore_u = [x for x in range(vertices) if x % 2 == 0]
    shore_v = [x for x in range(vertices) if x % 2 == 1]
    assert len(shore_u) == len(shore_v) + 1
    q = [1] * vertices
    for (x, y), b in zip(edges, labels, strict=True):
        q[x] *= b
        q[y] *= b
    c = [ceil_log2(x) for x in q]
    exponents = [K - z for z in c]
    delta = sum(exponents[x] for x in shore_u) - sum(exponents[x] for x in shore_v)
    assert delta >= 0
    for j in range(delta):
        x = shore_u[j % len(shore_u)]
        exponents[x] -= 1
    assert min(exponents) >= 0
    a = [(1 << exponents[x]) * q[x] for x in range(vertices)]
    assert len(set(a)) == vertices
    assert math.prod(a[x] for x in shore_u) == math.prod(a[x] for x in shore_v)
    assert max(a) <= 1 << K
    return a, max(K - x.bit_length() + 1 for x in a)


def path_edges(vertices: int) -> list[tuple[int, int]]:
    return [(i, i + 1) for i in range(vertices - 1)]


def main() -> None:
    K = 160
    vertices = 31
    edges = path_edges(vertices)
    narrow = primes_in_interval(1024, 2048, len(edges))
    path_values, path_band = padded_relation(vertices, edges, narrow, K)

    d = 4
    occurrence_primes = primes_in_interval(4096, 8192, d * len(edges))
    product_labels = [
        math.prod(occurrence_primes[d * i : d * (i + 1)]) for i in range(len(edges))
    ]
    occurrence_values, occurrence_band = padded_relation(vertices, edges, product_labels, K)
    beta = d * len(edges) - vertices + 1
    assert beta == (d - 1) * (vertices - 1)

    # A path with three length-two arms attached to even vertices.  Number the
    # new odd/even pair consecutively so the parity bipartition is preserved.
    base_vertices = 15
    branch_edges = path_edges(base_vertices)
    next_vertex = base_vertices
    for anchor in (2, 6, 10):
        odd = next_vertex if next_vertex % 2 == 1 else next_vertex + 1
        even = odd + 1
        next_vertex = even + 1
        branch_edges.extend([(anchor, odd), (odd, even)])
    branch_vertices = next_vertex
    branch_primes = primes_in_interval(1024, 2048, len(branch_edges))
    branch_values, branch_band = padded_relation(
        branch_vertices, branch_edges, branch_primes, K
    )

    result = {
        "status": "PASS",
        "scope": "finite guards for separately proved graph-product families; no finite extrapolation",
        "narrow_scale_path": {
            "vertices": vertices,
            "transitions": len(edges),
            "dyadic_label_scales": len({p.bit_length() for p in narrow}),
            "top_band_power_of_two_width": path_band,
            "distinct_terms": len(set(path_values)),
        },
        "private_branch_tree": {
            "vertices": branch_vertices,
            "edges": len(branch_edges),
            "branch_arms": 3,
            "top_band_power_of_two_width": branch_band,
            "distinct_terms": len(set(branch_values)),
        },
        "high_occurrence_path": {
            "vertices": vertices,
            "private_primes_per_edge": d,
            "cycle_rank_ignoring_two_adic_edges": beta,
            "formula": (d - 1) * (vertices - 1),
            "top_band_power_of_two_width": occurrence_band,
            "distinct_terms": len(set(occurrence_values)),
        },
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
