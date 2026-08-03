#!/usr/bin/env python3
"""Exact first kill test for the full W4 marked-spoke specialization.

The negative point was found by a finite search, but every conclusion emitted
here is an exact identity or a consequence of the already established
C-Garding status of the deletion polynomial.  No scan-completeness claim is
made.  Intended external limit: 2 GiB virtual memory, 120 seconds.
"""

from __future__ import annotations

from itertools import combinations
import json
import sympy as sp


VERTICES = tuple(range(5))
MARKED = (0, 1)
EDGES = (
    (0, 1), (0, 2), (0, 3), (0, 4),
    (1, 2), (2, 3), (3, 4), (1, 4),
)
a, b, c, d, t = sp.symbols("a b c d t")
VARIABLE = {
    (0, 2): a, (0, 4): a,
    (0, 3): b,
    (1, 2): c, (1, 4): c,
    (2, 3): d, (3, 4): d,
}


def is_forest(edges: tuple[tuple[int, int], ...]) -> bool:
    parent = list(VERTICES)

    def find(vertex: int) -> int:
        while parent[vertex] != vertex:
            parent[vertex] = parent[parent[vertex]]
            vertex = parent[vertex]
        return vertex

    for u, v in edges:
        ru, rv = find(u), find(v)
        if ru == rv:
            return False
        parent[ru] = rv
    return True


def connected(edges: tuple[tuple[int, int], ...], source: int, target: int) -> bool:
    adjacency = {vertex: [] for vertex in VERTICES}
    for u, v in edges:
        adjacency[u].append(v)
        adjacency[v].append(u)
    stack = [source]
    seen = {source}
    while stack:
        u = stack.pop()
        for v in adjacency[u]:
            if v not in seen:
                seen.add(v)
                stack.append(v)
    return target in seen


def reconstruct() -> tuple[sp.Expr, sp.Expr, int, int]:
    unmarked = tuple(edge for edge in EDGES if edge != MARKED)
    deletion = sp.Integer(0)
    xi = sp.Integer(0)
    forest_count = 0
    connected_count = 0
    for size in range(len(unmarked) + 1):
        for chosen in combinations(unmarked, size):
            if not is_forest(chosen):
                continue
            forest_count += 1
            chosen_set = set(chosen)
            monomial = sp.prod(VARIABLE[edge] for edge in unmarked if edge not in chosen_set)
            deletion += monomial
            if connected(chosen, *MARKED):
                connected_count += 1
                xi += monomial
    return sp.expand(deletion), sp.expand(xi), forest_count, connected_count


def main() -> None:
    P, xi, forest_count, connected_count = reconstruct()
    ones = {a: 1, b: 1, c: 1, d: 1}
    assert forest_count == 86 and connected_count == 38
    assert P.subs(ones) == 86 and xi.subs(ones) == 38

    # Compact full four-variable form, quadratic in the broken-symmetry a.
    p_coefficients = tuple(sp.factor(value) for value in sp.Poly(P, a).all_coeffs())
    xi_coefficients = tuple(sp.factor(value) for value in sp.Poly(xi, a).all_coeffs())
    expected_p_coefficients = (
        (b + 1) * (c*d + c + d) * (c*d + c + d + 2),
        2 * (
            b*c**2*d**2 + 2*b*c**2*d + b*c**2
            + 2*b*c*d**2 + 4*b*c*d + 2*b*c + b*d**2 + 2*b*d
            + c**2*d**2 + c**2*d + 2*c*d**2 + 2*c*d + d**2
        ),
        c*d*(c + 2)*(b*d + 2*b + d),
    )
    expected_xi_coefficients = (
        2*(c*d + c + d),
        2*(
            b*c*d**2 + 2*b*c*d + 2*b*c + b*d**2 + 2*b*d
            + c*d**2 + 2*c*d + d**2
        ),
        2*c*d*(b*d + 2*b + d),
    )
    assert all(sp.expand(actual - expected) == 0 for actual, expected in zip(
        p_coefficients, expected_p_coefficients
    ))
    assert all(sp.expand(actual - expected) == 0 for actual, expected in zip(
        xi_coefficients, expected_xi_coefficients
    ))

    negative_point = {a: -8, b: sp.Rational(1, 8), c: 8, d: 7}
    assert P.subs(negative_point) == 294896
    assert xi.subs(negative_point) == -16

    # The fixed (b,c,d) fibre already displays the intervening P<0 island.
    base = {b: sp.Rational(1, 8), c: 8, d: 7}
    p_fibre = sp.factor(P.subs(base))
    xi_fibre = sp.factor(xi.subs(base))
    assert sp.expand(p_fibre - (46647*a**2 + 82830*a + 36400) / 8) == 0
    assert sp.expand(xi_fibre - (568*a**2 + 5007*a + 3640) / 4) == 0
    assert p_fibre.subs(a, sp.Rational(-4, 5)) == sp.Rational(-31, 25)

    # Stronger global component exclusion.  The spoke deletion is already
    # known C-Garding, so its distinguished positivity component is convex.
    # If the negative point belonged to it, its segment to the positive anchor
    # would remain in P>0.  At t=1/5 that segment has exact negative P.
    target = tuple(negative_point[v] for v in (a, b, c, d))
    segment = tuple(1 + t*(value - 1) for value in target)
    segment_polynomial = sp.factor(P.subs(dict(zip((a, b, c, d), segment))))
    barrier_parameter = sp.Rational(1, 5)
    barrier_point = tuple(sp.factor(value.subs(t, barrier_parameter)) for value in segment)
    assert barrier_point == (
        sp.Rational(-4, 5), sp.Rational(33, 40),
        sp.Rational(12, 5), sp.Rational(11, 5),
    )
    assert segment_polynomial.subs(t, barrier_parameter) == sp.Rational(-1009646, 78125)

    print(json.dumps({
        "schema": "amra.opg1757.round2.g202-spoke-first-kill-test.v1",
        "host": "W4",
        "marked_orbit": "spoke 01",
        "stabilizer_classes": {
            "a": ["02", "04"], "b": ["03"],
            "c": ["12", "14"], "d": ["23", "34"]
        },
        "reconstruction": {
            "deletion_forests": forest_count,
            "endpoint_connected_forests": connected_count,
            "P_at_anchor": 86,
            "xi_at_anchor": 38,
            "P_as_quadratic_in_a": [str(value) for value in p_coefficients],
            "xi_as_quadratic_in_a": [str(value) for value in xi_coefficients]
        },
        "exact_negative_point": {
            "coordinates": ["-8", "1/8", "8", "7"],
            "P": "294896",
            "xi": "-16"
        },
        "fixed_fibre": {
            "base": {"b": "1/8", "c": "8", "d": "7"},
            "P_of_a": str(p_fibre),
            "xi_of_a": str(xi_fibre),
            "barrier_a": "-4/5",
            "P_at_barrier_a": "-31/25"
        },
        "global_component_exclusion": {
            "dependency": "the established C-Garding status of P makes its distinguished positivity component convex",
            "anchor": ["1", "1", "1", "1"],
            "segment_parameter": "1/5",
            "segment_point": [str(value) for value in barrier_point],
            "P_at_segment_point": "-1009646/78125",
            "conclusion": "the P>0, xi<0 point is outside the full distinguished component"
        },
        "kill_test_outcome": "survives_this_exact_negative_specialization; full spoke domination remains open",
        "finite_scan_role": "candidate discovery only; no completeness or promotion claim",
        "lean_used": False,
        "phase_changed": False,
        "public_problem_changed": False
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
