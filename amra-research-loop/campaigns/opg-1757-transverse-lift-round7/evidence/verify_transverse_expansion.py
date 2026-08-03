#!/usr/bin/env python3
"""Exact eight-variable and transverse expansion ledger (stdlib only)."""

from __future__ import annotations

from hashlib import sha256
from itertools import combinations, permutations
import json


VERTICES = tuple(range(5))
EDGES = ((0, 1), (0, 2), (0, 4), (1, 2), (1, 3), (1, 4), (2, 3), (2, 4))
MARKED = (0, 3)
# Polynomial slots: a,b,c,d,e,u,v,q.
ZERO = (0,) * 8


def add(left, right):
    result = dict(left)
    for monomial, coefficient in right.items():
        result[monomial] = result.get(monomial, 0) + coefficient
    return {m: value for m, value in result.items() if value}


def multiply(left, right):
    result = {}
    for lm, lv in left.items():
        for rm, rv in right.items():
            monomial = tuple(x + y for x, y in zip(lm, rm))
            result[monomial] = result.get(monomial, 0) + lv * rv
    return {m: value for m, value in result.items() if value}


def term(slot, coefficient=1):
    exponent = [0] * 8
    exponent[slot] = 1
    return {tuple(exponent): coefficient}


EDGE_FACTOR = {
    (0, 1): add(term(0), term(5)),
    (0, 2): add(term(0), term(5, -1)),
    (0, 4): term(1),
    (1, 2): term(2),
    (1, 3): add(term(3), term(6)),
    (2, 3): add(term(3), term(6, -1)),
    (1, 4): add(term(4), term(7)),
    (2, 4): add(term(4), term(7, -1)),
}


def is_forest(edges):
    parent = list(VERTICES)

    def find(vertex):
        while parent[vertex] != vertex:
            parent[vertex] = parent[parent[vertex]]
            vertex = parent[vertex]
        return vertex

    for left, right in edges:
        left_root, right_root = find(left), find(right)
        if left_root == right_root:
            return False
        parent[left_root] = right_root
    return True


def connected(edges):
    adjacency = {vertex: [] for vertex in VERTICES}
    for left, right in edges:
        adjacency[left].append(right)
        adjacency[right].append(left)
    stack, seen = [MARKED[0]], {MARKED[0]}
    while stack:
        vertex = stack.pop()
        for neighbour in adjacency[vertex]:
            if neighbour not in seen:
                seen.add(neighbour)
                stack.append(neighbour)
    return MARKED[1] in seen


def reconstruct():
    P, xi = {}, {}
    forest_count = connected_count = 0
    for size in range(len(EDGES) + 1):
        for chosen in combinations(EDGES, size):
            if not is_forest(chosen):
                continue
            forest_count += 1
            chosen_set = set(chosen)
            monomial = {ZERO: 1}
            for edge in EDGES:
                if edge not in chosen_set:
                    monomial = multiply(monomial, EDGE_FACTOR[edge])
            P = add(P, monomial)
            if connected(chosen):
                connected_count += 1
                xi = add(xi, monomial)
    return P, xi, forest_count, connected_count


def transverse_support(poly):
    return {monomial[5:] for monomial in poly}


def at_base_anchor(poly):
    result = {}
    for monomial, coefficient in poly.items():
        key = monomial[5:]
        result[key] = result.get(key, 0) + coefficient
    return {m: value for m, value in result.items() if value}


def fixed_coefficient_at_anchor(poly):
    return sum(value for monomial, value in poly.items() if monomial[5:] == (0, 0, 0))


def canonical(poly):
    return json.dumps(
        [[list(monomial), coefficient] for monomial, coefficient in sorted(poly.items())],
        separators=(",", ":"),
    )


# Small univariate-in-k engine for the exact symmetric-ray resultant.
def uadd(left, right):
    result = dict(left)
    for degree, coefficient in right.items():
        result[degree] = result.get(degree, 0) + coefficient
    return {degree: value for degree, value in result.items() if value}


def umultiply(left, right):
    result = {}
    for ld, lv in left.items():
        for rd, rv in right.items():
            result[ld + rd] = result.get(ld + rd, 0) + lv * rv
    return {degree: value for degree, value in result.items() if value}


def uscale(poly, scalar):
    return {degree: scalar * value for degree, value in poly.items() if scalar * value}


def upower(poly, exponent):
    result = {0: 1}
    for _ in range(exponent):
        result = umultiply(result, poly)
    return result


def udeterminant(matrix):
    size = len(matrix)
    result = {}
    for permutation in permutations(range(size)):
        inversions = sum(
            permutation[i] > permutation[j]
            for i in range(size) for j in range(i + 1, size)
        )
        product = {0: -1 if inversions % 2 else 1}
        for row, column in enumerate(permutation):
            product = umultiply(product, matrix[row][column])
        result = uadd(result, product)
    return result


def main():
    P, xi, forest_count, connected_count = reconstruct()
    assert (forest_count, connected_count) == (128, 58)
    assert len(P) == 155 and len(xi) == 38
    assert len(transverse_support(P)) == 10
    assert len(transverse_support(xi)) == 8
    assert all(sum(monomial) % 2 == 0 for monomial in transverse_support(P))
    assert all(sum(monomial) % 2 == 0 for monomial in transverse_support(xi))
    assert (fixed_coefficient_at_anchor(P), fixed_coefficient_at_anchor(xi)) == (128, 58)

    expected_P_anchor = {
        (0, 0, 0): 128,
        (2, 0, 0): -48,
        (0, 2, 0): -38,
        (0, 0, 2): -48,
        (1, 0, 1): -6,
        (2, 2, 0): 14,
        (2, 0, 2): 14,
        (0, 2, 2): 14,
        (1, 2, 1): 2,
        (2, 2, 2): -4,
    }
    expected_xi_anchor = {
        (0, 0, 0): 58,
        (2, 0, 0): -10,
        (0, 0, 2): -20,
        (1, 1, 0): 8,
        (1, 0, 1): -4,
        (0, 1, 1): 2,
        (1, 1, 2): -4,
        (2, 1, 1): -2,
    }
    assert at_base_anchor(P) == expected_P_anchor
    assert at_base_anchor(xi) == expected_xi_anchor

    # On the symmetric direction (U,V,Q)=(1,1,k), put s=t^2.  The exact
    # resultant locates every common P/xi ray wall, including the squared
    # near-contact factor seen by the finite discovery scan.
    zero = {}
    bp0, bp1 = {0: -64}, {0: 43, 1: 3, 2: 24}
    bp2, bp3 = {0: -7, 1: -1, 2: -14}, {2: 2}
    bx0, bx1, bx2 = {0: -29}, {0: 1, 1: 1, 2: 10}, {1: 1, 2: 2}
    resultant = udeterminant([
        [bp3, bp2, bp1, bp0, zero],
        [zero, bp3, bp2, bp1, bp0],
        [bx2, bx1, bx0, zero, zero],
        [zero, bx2, bx1, bx0, zero],
        [zero, zero, bx2, bx1, bx0],
    ])
    k = {1: 1}
    expected_resultant = uscale(umultiply(
        k,
        umultiply(
            upower(uadd(uadd(uscale(upower(k, 2), 6), k), {0: -14}), 2),
            uadd(uadd(uadd(uscale(upower(k, 3), 224), uscale(upower(k, 2), 148)), uscale(k, -73)), {0: -42}),
        ),
    ), -4)
    assert resultant == expected_resultant

    print(json.dumps({
        "schema": "amra.opg1757.round7.transverse-expansion.v1",
        "reconstruction": {
            "forest_count": forest_count,
            "endpoint_connected_count": connected_count,
            "expanded_P_terms": len(P),
            "expanded_xi_terms": len(xi),
            "P_sha256": sha256(canonical(P).encode()).hexdigest(),
            "xi_sha256": sha256(canonical(xi).encode()).hexdigest(),
        },
        "involution": "(u,v,q)->(-u,-v,-q); every surviving transverse monomial has even total degree",
        "anchor": {
            "P_coefficients": {str(key): value for key, value in sorted(expected_P_anchor.items())},
            "xi_coefficients": {str(key): value for key, value in sorted(expected_xi_anchor.items())},
            "P_transverse_hessian": [[-96, 0, -6], [0, -76, 0], [-6, 0, -96]],
            "xi_transverse_hessian": [[-20, 8, -4], [8, 0, 2], [-4, 2, -40]],
        },
        "symmetric_ray_resultant": "-4*k*(6*k^2+k-14)^2*(224*k^3+148*k^2-73*k-42)",
        "scope": "exact expansion and local anchor data only; no component-complete transverse theorem",
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
