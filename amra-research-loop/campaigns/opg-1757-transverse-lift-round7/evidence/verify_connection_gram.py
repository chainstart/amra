#!/usr/bin/env python3
"""Exact Gram certificates for the three book-page connections (stdlib only)."""

from __future__ import annotations

from hashlib import sha256
from itertools import combinations, permutations
import json

from verify_c_zero_fibre import (
    EDGES,
    EDGE_INDEX,
    VERTICES,
    add as add_original,
    canonical as canonical_original,
    derivative,
    is_forest,
    multiply as multiply_original,
    original_variable,
    pair_polynomial,
    reconstruct_original,
)


B_EDGE = (0, 4)
PAGE_EDGES = {
    "0": ((0, 1), (0, 2)),
    "3": ((1, 3), (2, 3)),
    "4": ((1, 4), (2, 4)),
}
NAMES = ("q0", "q3", "q4", "c", "l0", "l3", "l4")
COUNT = len(NAMES)
ZERO = (0,) * COUNT


def add(left, right, scale=1):
    result = dict(left)
    for monomial, coefficient in right.items():
        result[monomial] = result.get(monomial, 0) + scale * coefficient
    return {monomial: coefficient for monomial, coefficient in result.items() if coefficient}


def multiply(left, right):
    result = {}
    for left_monomial, left_coefficient in left.items():
        for right_monomial, right_coefficient in right.items():
            monomial = tuple(a + b for a, b in zip(left_monomial, right_monomial))
            result[monomial] = (
                result.get(monomial, 0) + left_coefficient * right_coefficient
            )
    return {monomial: coefficient for monomial, coefficient in result.items() if coefficient}


def scale(poly, scalar):
    return {monomial: scalar * coefficient for monomial, coefficient in poly.items() if scalar}


def constant(value):
    return {} if not value else {ZERO: value}


def variable(name):
    monomial = [0] * COUNT
    monomial[NAMES.index(name)] = 1
    return {tuple(monomial): 1}


def power(poly, exponent):
    result = constant(1)
    for _ in range(exponent):
        result = multiply(result, poly)
    return result


def determinant(matrix):
    size = len(matrix)
    result = {}
    for permutation in permutations(range(size)):
        inversions = sum(
            permutation[left] > permutation[right]
            for left in range(size)
            for right in range(left + 1, size)
        )
        term = constant(-1 if inversions % 2 else 1)
        for row, column in enumerate(permutation):
            term = multiply(term, matrix[row][column])
        result = add(result, term)
    return result


def canonical(poly):
    return json.dumps(
        [[list(monomial), coefficient] for monomial, coefficient in sorted(poly.items())],
        separators=(",", ":"),
    )


def digest(poly):
    return sha256(canonical(poly).encode()).hexdigest()


def connects(chosen, marked):
    adjacency = {vertex: [] for vertex in VERTICES}
    for left, right in chosen:
        adjacency[left].append(right)
        adjacency[right].append(left)
    stack, seen = [marked[0]], {marked[0]}
    while stack:
        vertex = stack.pop()
        for neighbour in adjacency[vertex]:
            if neighbour not in seen:
                seen.add(neighbour)
                stack.append(neighbour)
    return marked[1] in seen


def reconstruct_connection(marked):
    """Complement polynomial of b-deleted forests connecting ``marked``."""
    active_edges = tuple(edge for edge in EDGES if edge != B_EDGE)
    result = {}
    forest_count = connected_count = 0
    for size in range(len(active_edges) + 1):
        for chosen in combinations(active_edges, size):
            if not is_forest(chosen):
                continue
            forest_count += 1
            if not connects(chosen, marked):
                continue
            connected_count += 1
            chosen_set = set(chosen)
            exponent = tuple(
                int(edge in active_edges and edge not in chosen_set)
                for edge in EDGES
            )
            result[exponent] = result.get(exponent, 0) + 1
    return result, forest_count, connected_count


def original_connection_formula(i, j, k):
    c = original_variable((1, 2))
    qi = pair_polynomial(*PAGE_EDGES[i])
    qj = pair_polynomial(*PAGE_EDGES[j])
    qk = pair_polynomial(*PAGE_EDGES[k])
    li, ri = (original_variable(edge) for edge in PAGE_EDGES[i])
    lj, rj = (original_variable(edge) for edge in PAGE_EDGES[j])
    pi = add_original(li, ri)
    pj = add_original(lj, rj)
    aligned = add_original(multiply_original(li, lj), multiply_original(ri, rj))
    return add_original(
        multiply_original(multiply_original(c, qk), add_original(add_original(pi, pj), aligned)),
        multiply_original(add_original(c, qk), multiply_original(pi, pj)),
    )


def route_a(q):
    q0, q3, q4, c = (q[name] for name in ("0", "3", "4", "c"))
    return add(
        multiply(multiply(q0, q3), q4),
        multiply(
            c,
            add(
                add(multiply(q0, q3), multiply(q0, q4)),
                add(multiply(q3, q4), multiply(multiply(q0, q3), q4)),
            ),
        ),
    )


def quadratic_form(matrix, vector):
    result = {}
    for row in range(len(vector)):
        for column in range(len(vector)):
            result = add(
                result,
                multiply(multiply(vector[row], matrix[row][column]), vector[column]),
            )
    return result


def connection_certificate(i, j, k, q, left, A):
    """Return the cleared connection numerator and its Gram data."""
    one = constant(1)
    den_i = add(one, left[i])
    den_j = add(one, left[j])
    pi_num = add(q[i], power(left[i], 2))
    pj_num = add(q[j], power(left[j], 2))
    aligned_num = add(
        multiply(multiply(left[i], left[j]), multiply(den_i, den_j)),
        multiply(add(q[i], left[i], -1), add(q[j], left[j], -1)),
    )

    # Substitute r_s=(q_s-l_s)/(1+l_s) into the graph-native connection
    # formula and clear the positive denominator (1+l_i)(1+l_j).
    cleared = add(
        multiply(
            multiply(q["c"], q[k]),
            add(
                add(multiply(pi_num, den_j), multiply(pj_num, den_i)),
                aligned_num,
            ),
        ),
        multiply(add(q["c"], q[k]), multiply(pi_num, pj_num)),
    )

    T = add(q["c"], q[k])
    L = multiply(q["c"], q[k])
    M = add(T, L)
    E_j = add(
        add(multiply(q["c"], q[j]), multiply(q["c"], q[k])),
        multiply(q[j], q[k]),
    )
    E_i = add(
        add(multiply(q["c"], q[i]), multiply(q["c"], q[k])),
        multiply(q[i], q[k]),
    )
    H = [[M, L, L], [L, E_j, L], [L, L, E_i]]
    z = [multiply(left[i], left[j]), left[i], left[j]]
    gram = add(A, quadratic_form(H, z))
    assert cleared == gram

    B_i = add(
        add(
            multiply(multiply(q["c"], q[j]), q[k]),
            multiply(q["c"], q[j]),
        ),
        add(multiply(q["c"], q[k]), multiply(q[j], q[k])),
    )
    minor1 = H[0][0]
    minor2 = determinant([row[:2] for row in H[:2]])
    minor3 = determinant(H)
    assert minor1 == M
    assert minor2 == multiply(T, B_i)
    assert minor3 == multiply(power(T, 2), A)
    return {
        "cleared": cleared,
        "gram": gram,
        "H": H,
        "T": T,
        "M": M,
        "B_i": B_i,
        "minors": (minor1, minor2, minor3),
    }


def main():
    deletion, connectivity, forest_count, connected_count = reconstruct_original()
    assert (forest_count, connected_count) == (128, 58)
    a_slope = derivative(deletion, (B_EDGE,))

    pairs = (("0", "3", "4"), ("0", "4", "3"), ("3", "4", "0"))
    original_records = {"A": a_slope}
    reconstruction = {}
    for i, j, k in pairs:
        marked = (int(i), int(j))
        connection, count, connection_count = reconstruct_connection(marked)
        assert count == 81
        assert connection == original_connection_formula(i, j, k)
        if (i, j) == ("0", "3"):
            # This is the D slope independently reconstructed in the b-Rayleigh ledger.
            assert connection == derivative(connectivity, (B_EDGE,))
        name = f"p{i}{j}"
        original_records[name] = connection
        reconstruction[name] = {
            "forests": count,
            "connecting_forests": connection_count,
            "terms": len(connection),
            "sha256": sha256(canonical_original(connection).encode()).hexdigest(),
        }

    q = {name: variable(f"q{name}") for name in ("0", "3", "4")}
    q["c"] = variable("c")
    left = {name: variable(f"l{name}") for name in ("0", "3", "4")}
    A = route_a(q)

    route_records = {"A": A}
    certificates = {}
    for i, j, k in pairs:
        data = connection_certificate(i, j, k, q, left, A)
        name = f"p{i}{j}"
        route_records[f"{name}_cleared"] = data["cleared"]
        route_records[f"H{k}_det"] = data["minors"][2]
        certificates[name] = {
            "remaining_page": k,
            "identity": (
                f"p{i}{j}*(1+l{i})*(1+l{j})="
                f"A+(l{i}*l{j},l{i},l{j})^T H{k} (l{i}*l{j},l{i},l{j})"
            ),
            "sylvester_minors": [
                f"M{k}=c+q{k}+c*q{k}",
                f"(c+q{k})*B{i}",
                f"(c+q{k})^2*A",
            ],
        }

    print(json.dumps({
        "schema": "amra.opg1757.round7.connection-gram.v1",
        "reconstruction": reconstruction,
        "route_chamber": {
            "hypothesis": "positive edge floors and K=diag(q0,q3,q4,c)+11^T positive definite",
            "A": "det(K)",
            "positive_inputs": "A, every 2x2 and 3x3 principal minor, and c+qk=Rc+Rk-2",
        },
        "certificates": certificates,
        "consequence": (
            "Hk is positive definite by its three leading Sylvester minors; "
            "therefore all three connection polynomials p03,p04,p34 are strictly positive"
        ),
        "records": {
            name: {"terms": len(poly), "sha256": digest(poly)}
            for name, poly in route_records.items()
        },
        "scope": (
            "exact direct replacement for the external sign argument for D=p03; "
            "the generic sign of Delta_b still requires a coupled certificate"
        ),
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
