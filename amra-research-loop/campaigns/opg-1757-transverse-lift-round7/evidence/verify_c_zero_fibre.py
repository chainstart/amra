#!/usr/bin/env python3
"""Exact c=0 q-fibre containment ledger (Python standard library only).

The verifier reconstructs both graph polynomials from forests in the eight
original edge variables.  It then performs a fresh transverse substitution
and checks the coefficient, derivative, and boundary-determinant identities
used by C_ZERO_FIBRE_THEOREM.md.
"""

from __future__ import annotations

from hashlib import sha256
from itertools import combinations
import json


VERTICES = tuple(range(5))
EDGES = ((0, 1), (0, 2), (0, 4), (1, 2), (1, 3), (1, 4), (2, 3), (2, 4))
MARKED = (0, 3)
EDGE_INDEX = {edge: index for index, edge in enumerate(EDGES)}
ZERO8 = (0,) * 8
ZERO7 = (0,) * 7


def add(left, right, scale=1):
    result = dict(left)
    for monomial, coefficient in right.items():
        result[monomial] = result.get(monomial, 0) + scale * coefficient
    return {monomial: value for monomial, value in result.items() if value}


def multiply(left, right):
    result = {}
    for left_monomial, left_value in left.items():
        for right_monomial, right_value in right.items():
            monomial = tuple(
                left_degree + right_degree
                for left_degree, right_degree in zip(left_monomial, right_monomial)
            )
            result[monomial] = result.get(monomial, 0) + left_value * right_value
    return {monomial: value for monomial, value in result.items() if value}


def scale(poly, scalar):
    return {monomial: scalar * value for monomial, value in poly.items() if scalar * value}


def variable(slot, coefficient=1):
    exponent = [0] * 8
    exponent[slot] = 1
    return {tuple(exponent): coefficient}


def original_variable(edge):
    return variable(EDGE_INDEX[edge])


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


def connects_marked(edges):
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


def reconstruct_original():
    deletion, connectivity = {}, {}
    forest_count = connected_count = 0
    for size in range(len(EDGES) + 1):
        for chosen in combinations(EDGES, size):
            if not is_forest(chosen):
                continue
            forest_count += 1
            chosen = set(chosen)
            exponent = tuple(int(edge not in chosen) for edge in EDGES)
            deletion[exponent] = deletion.get(exponent, 0) + 1
            if connects_marked(chosen):
                connected_count += 1
                connectivity[exponent] = connectivity.get(exponent, 0) + 1
    return deletion, connectivity, forest_count, connected_count


def derivative(poly, differentiated_edges):
    differentiated = {EDGE_INDEX[edge] for edge in differentiated_edges}
    result = {}
    for monomial, coefficient in poly.items():
        if any(monomial[index] == 0 for index in differentiated):
            continue
        exponent = tuple(
            degree - int(index in differentiated)
            for index, degree in enumerate(monomial)
        )
        result[exponent] = result.get(exponent, 0) + coefficient
    return result


def restrict_original_zero(poly, edge):
    index = EDGE_INDEX[edge]
    return {
        monomial: coefficient
        for monomial, coefficient in poly.items()
        if monomial[index] == 0
    }


def transverse_factor(edge):
    # Transverse slots are a,b,c,d,e,u,v,q.
    factors = {
        (0, 1): add(variable(0), variable(5)),
        (0, 2): add(variable(0), variable(5, -1)),
        (0, 4): variable(1),
        (1, 2): variable(2),
        (1, 3): add(variable(3), variable(6)),
        (1, 4): add(variable(4), variable(7)),
        (2, 3): add(variable(3), variable(6, -1)),
        (2, 4): add(variable(4), variable(7, -1)),
    }
    return factors[edge]


def transverse_substitute(poly):
    result = {}
    for exponent, coefficient in poly.items():
        term = {ZERO8: coefficient}
        for edge, degree in zip(EDGES, exponent):
            assert degree in (0, 1)
            if degree:
                term = multiply(term, transverse_factor(edge))
        result = add(result, term)
    return result


def q_coefficients(poly):
    result = [{}, {}, {}]
    for monomial, coefficient in poly.items():
        q_degree = monomial[7]
        base = monomial[:7]
        result[q_degree][base] = result[q_degree].get(base, 0) + coefficient
    return [{m: c for m, c in part.items() if c} for part in result]


def restrict_base_zero(poly, slot):
    return {m: c for m, c in poly.items() if m[slot] == 0}


def base_monomial(**degrees):
    names = "abcdeuv"
    exponent = [0] * 7
    for name, degree in degrees.items():
        exponent[names.index(name)] = degree
    return tuple(exponent)


def pair_polynomial(left_edge, right_edge):
    left, right = original_variable(left_edge), original_variable(right_edge)
    return add(add(multiply(left, right), left), right)


def canonical(poly):
    return json.dumps(
        [[list(monomial), coefficient] for monomial, coefficient in sorted(poly.items())],
        separators=(",", ":"),
    )


def main():
    deletion, connectivity, forest_count, connected_count = reconstruct_original()
    assert (forest_count, connected_count) == (128, 58)

    c_edge = (1, 2)
    pair_a = pair_polynomial((0, 1), (0, 2))
    pair_d = pair_polynomial((1, 3), (2, 3))
    pair_e = pair_polynomial((1, 4), (2, 4))

    # On c=0, three fifth derivatives are precisely the three parallel-pair
    # quantities (1+x)(1+y)-1.  Derivative-component nesting makes them
    # positive on C_P.
    derivative_sets = {
        "A_pair": ((0, 4), (1, 3), (1, 4), (2, 3), (2, 4)),
        "D_pair": ((0, 1), (0, 2), (0, 4), (1, 4), (2, 4)),
        "E_pair": ((0, 1), (0, 2), (0, 4), (1, 3), (2, 3)),
    }
    expected_pairs = {"A_pair": pair_a, "D_pair": pair_d, "E_pair": pair_e}
    for name, differentiated in derivative_sets.items():
        wall_derivative = restrict_original_zero(derivative(deletion, differentiated), c_edge)
        assert wall_derivative == expected_pairs[name]

    deletion_transverse = transverse_substitute(deletion)
    connectivity_transverse = transverse_substitute(connectivity)
    p0, p1, p2 = q_coefficients(deletion_transverse)
    x0, x1, x2 = q_coefficients(connectivity_transverse)
    p0, p1, p2 = (restrict_base_zero(poly, 2) for poly in (p0, p1, p2))
    x0, x1, x2 = (restrict_base_zero(poly, 2) for poly in (x0, x1, x2))
    assert not p1 and not x1

    one_plus_b = {ZERO7: 1, base_monomial(b=1): 1}
    expected_x2 = scale(
        multiply(one_plus_b, {base_monomial(a=1, d=1): 1}),
        -4,
    )
    assert x2 == expected_x2

    d0 = add(multiply(p2, x0), multiply(x2, p0), -1)
    a_square_minus_u_square = {
        base_monomial(a=2): 1,
        base_monomial(u=2): -1,
    }
    d_pair_transverse = {
        base_monomial(d=2): 1,
        base_monomial(d=1): 2,
        base_monomial(v=2): -1,
    }
    expected_d0 = scale(
        multiply(
            multiply(
                {base_monomial(d=1, e=1): 1},
                multiply(a_square_minus_u_square, a_square_minus_u_square),
            ),
            multiply(one_plus_b, d_pair_transverse),
        ),
        -4,
    )
    assert d0 == expected_d0

    print(json.dumps({
        "schema": "amra.opg1757.round7.c-zero-fibre.v1",
        "reconstruction": {
            "deletion_forests": forest_count,
            "endpoint_connected_forests": connected_count,
            "P_original_sha256": sha256(canonical(deletion).encode()).hexdigest(),
            "xi_original_sha256": sha256(canonical(connectivity).encode()).hexdigest(),
        },
        "component_derivative_identities": {
            "A_pair": "partial_(04,13,14,23,24) P | c=0 = x01*x02+x01+x02",
            "D_pair": "partial_(01,02,04,14,24) P | c=0 = x13*x23+x13+x23",
            "E_pair": "partial_(01,02,04,13,23) P | c=0 = x14*x24+x14+x24",
        },
        "q_fibre": {
            "P1": "0",
            "xi1": "0",
            "xi2": "-4*a*d*(b+1)",
            "D0": "-4*d*e*(a^2-u^2)^2*(b+1)*(d^2+2*d-v^2)",
        },
        "sign_reduction": {
            "component": "edge floors plus the three pair derivatives imply a,d,e>0",
            "boundary": "P2<0 and D0<=0 imply xi>=0 at both P roots",
            "interior": "xi2<0 makes xi strictly concave, hence xi>0 inside the P interval",
        },
        "scope": "exact c=0 projected-component fibre theorem only; remaining walls and the full transverse theorem stay open",
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
