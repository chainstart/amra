#!/usr/bin/env python3
"""Independent exact audit of the W4 Gårding orbit probe."""

from collections import Counter
from itertools import combinations
import json
import sympy as sp


VERTICES = tuple(range(5))
SPOKES = ((0, 1), (0, 2), (0, 3), (0, 4))
RIM = ((1, 2), (2, 3), (3, 4), (1, 4))
EDGES = SPOKES + RIM
a, b, c, d, t = sp.symbols("a b c d t", real=True)
VARIABLES = (a, b, c, d)


def canonical(left, right):
    return tuple(sorted((left, right)))


def is_forest(edges):
    parent = list(VERTICES)

    def find(vertex):
        while parent[vertex] != vertex:
            parent[vertex] = parent[parent[vertex]]
            vertex = parent[vertex]
        return vertex

    for left, right in edges:
        root_left, root_right = find(left), find(right)
        if root_left == root_right:
            return False
        parent[root_left] = root_right
    return True


def connected(edges, source, target):
    adjacency = {vertex: [] for vertex in VERTICES}
    for left, right in edges:
        adjacency[left].append(right)
        adjacency[right].append(left)
    seen = {source}
    stack = [source]
    while stack:
        vertex = stack.pop()
        for nxt in adjacency[vertex]:
            if nxt not in seen:
                seen.add(nxt)
                stack.append(nxt)
    return target in seen


def variable_map(orbit):
    if orbit == "spoke":
        return {
            canonical(0, 2): a, canonical(0, 4): a,
            canonical(0, 3): b,
            canonical(1, 2): c, canonical(1, 4): c,
            canonical(2, 3): d, canonical(3, 4): d,
        }
    return {
        canonical(0, 1): a, canonical(0, 2): a,
        canonical(0, 3): b, canonical(0, 4): b,
        canonical(2, 3): c, canonical(1, 4): c,
        canonical(3, 4): d,
    }


def enumerate_polynomials(marked, orbit):
    remaining = tuple(item for item in EDGES if item != marked)
    weights = variable_map(orbit)
    c_delete = 0
    xi = 0
    forest_count = 0
    connected_forest_count = 0
    for mask in range(1 << len(remaining)):
        forest = tuple(remaining[index] for index in range(len(remaining)) if mask >> index & 1)
        if not is_forest(forest):
            continue
        forest_count += 1
        complement = tuple(item for item in remaining if item not in forest)
        monomial = sp.prod(weights[item] for item in complement)
        c_delete += monomial
        if connected(forest, *marked):
            xi += monomial
            connected_forest_count += 1
    return sp.expand(c_delete), sp.expand(xi), forest_count, connected_forest_count


def suppress_vertex(edge_multiset, vertex):
    incident = [item for item in edge_multiset.elements() if vertex in item]
    assert len(incident) == 2
    neighbours = [item[0] if item[1] == vertex else item[1] for item in incident]
    result = edge_multiset.copy()
    for item in incident:
        result[item] -= 1
        if result[item] == 0:
            del result[item]
    result[canonical(*neighbours)] += 1
    return result


def check_deletion_reductions():
    spoke_delete = Counter(item for item in EDGES if item != canonical(0, 1))
    spoke_suppressed = suppress_vertex(spoke_delete, 1)
    k4 = Counter(canonical(left, right) for left, right in combinations((0, 2, 3, 4), 2))
    assert spoke_suppressed == k4

    rim_delete = Counter(item for item in EDGES if item != canonical(1, 2))
    rim_suppressed = suppress_vertex(suppress_vertex(rim_delete, 1), 2)
    expected_parallel_triangle = Counter({
        canonical(0, 3): 2,
        canonical(0, 4): 2,
        canonical(3, 4): 1,
    })
    assert rim_suppressed == expected_parallel_triangle
    return {
        "spoke": "suppress degree-two vertex 1 to obtain simple K4",
        "rim": "suppress degree-two vertices 1 and 2 to obtain a triangle with two doubled edges",
    }


def channel(polynomial, variable):
    substitution = {item: 1 for item in VARIABLES}
    substitution[variable] = t
    return sp.factor(polynomial.subs(substitution))


def main():
    reductions = check_deletion_reductions()
    spoke_f, spoke_x, spoke_forests, spoke_connected = enumerate_polynomials((0, 1), "spoke")
    rim_f, rim_x, rim_forests, rim_connected = enumerate_polynomials((1, 2), "rim")
    assert spoke_f.subs(dict.fromkeys(VARIABLES, 1)) == 86
    assert spoke_x.subs(dict.fromkeys(VARIABLES, 1)) == 38
    assert rim_f.subs(dict.fromkeys(VARIABLES, 1)) == 82
    assert rim_x.subs(dict.fromkeys(VARIABLES, 1)) == 30

    expected = {
        "spoke": {
            a: (2*(15*t**2 + 22*t + 6), 2*(3*t**2 + 12*t + 4), (-11+sp.sqrt(31))/15),
            b: (2*(27*t + 16), 2*(11*t + 8), sp.Rational(-16, 27)),
            c: (2*(12*t**2 + 24*t + 7), 2*(14*t + 5), -1+sp.sqrt(15)/6),
            d: (2*(15*t**2 + 22*t + 6), 2*(6*t**2 + 10*t + 3), (-11+sp.sqrt(31))/15),
        },
        "rim": {
            a: (2*(14*t**2 + 20*t + 7), 2*(2*t**2 + 6*t + 7), (-10+sp.sqrt(2))/14),
            b: (31*t**2 + 42*t + 9, 2*(5*t**2 + 8*t + 2), (-21+9*sp.sqrt(2))/31),
            c: (2*(14*t**2 + 20*t + 7), 7*t**2 + 14*t + 9, (-10+sp.sqrt(2))/14),
            d: (49*t + 33, 2*(8*t + 7), sp.Rational(-33, 49)),
        },
    }
    polynomials = {"spoke": (spoke_f, spoke_x), "rim": (rim_f, rim_x)}
    comparisons = []
    for orbit in ("spoke", "rim"):
        f, x = polynomials[orbit]
        for variable, (expected_f, expected_x, boundary) in expected[orbit].items():
            actual_f, actual_x = channel(f, variable), channel(x, variable)
            assert sp.expand(actual_f - expected_f) == 0
            assert sp.expand(actual_x - expected_x) == 0
            f_roots = [root for root in sp.solve(actual_f, t) if root.is_real is not False]
            assert any(sp.simplify(root - boundary) == 0 for root in f_roots)
            if sp.degree(actual_x, t) == 2 and sp.discriminant(actual_x, t) < 0:
                assert sp.LC(sp.Poly(actual_x, t)) > 0
                comparison = "xi positive on all real t"
            else:
                x_roots = [root for root in sp.solve(actual_x, t) if root.is_real is not False]
                rightmost_x = max(x_roots, key=lambda root: float(sp.N(root)))
                assert sp.ask(sp.Q.positive(boundary - rightmost_x)) is True
                comparison = f"xi right root {rightmost_x} is left of C boundary"
            comparisons.append({
                "orbit": orbit,
                "variable": str(variable),
                "C_boundary": str(boundary),
                "comparison": comparison,
            })

    natural = {b: a, d: c}
    spoke_slice_f = sp.factor(spoke_f.subs(natural))
    spoke_slice_x = sp.factor(spoke_x.subs(natural))
    ps = sp.cancel(spoke_slice_f / c)
    qs = sp.cancel(spoke_slice_x / (2*c))
    spoke_identity = sp.expand(
        (a+1)*ps - (a**2*c+2*a*c+3*a+c+2)*qs - a**2*(4*a**2-2*a-c)
    )
    rim_slice_f = sp.factor(rim_f.subs(natural))
    rim_slice_x = sp.factor(rim_x.subs(natural))
    remainder = (
        a**4+6*a**3+2*a**2*c**2+7*a**2*c+8*a**2
        +4*a*c**2+8*a*c+2*c**2
    )
    rim_identity = sp.expand(rim_slice_f - (a+1)**2*rim_slice_x + a**2*remainder)
    assert spoke_identity == rim_identity == 0

    print(json.dumps({
        "schema": "amra.opg1757.w4-garding-orbit-independent-check.v1",
        "deletion_reductions": reductions,
        "enumeration": {
            "spoke": {"deletion_forests": spoke_forests, "connected_endpoint_forests": spoke_connected},
            "rim": {"deletion_forests": rim_forests, "connected_endpoint_forests": rim_connected},
        },
        "at_ones": {"spoke": {"C_delete": 86, "xi": 38}, "rim": {"C_delete": 82, "xi": 30}},
        "eight_channel_comparisons": comparisons,
        "boundary_identities": {"spoke": "pass", "rim": "pass"},
        "result": "pass",
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
