#!/usr/bin/env python3
"""Blind audit of the full four-variable W4 rim component certificate.

P and Q are reconstructed from the graph, not imported from author evidence.
"""

from __future__ import annotations

from itertools import combinations
import json
from math import prod

import sympy as sp


a, b, c, d = sp.symbols("a b c d", real=True)
x, y, z, w, u = sp.symbols("x y z w u", real=True)

# W4 has centre 0, rim 1-2-3-4-1, and marked rim edge 12.
EDGES = (
    (0, 1, a), (0, 2, a),
    (0, 3, b), (0, 4, b),
    (2, 3, c), (1, 4, c),
    (3, 4, d),
)


def forest_and_connected(indices: tuple[int, ...]) -> tuple[bool, bool]:
    parent = list(range(5))

    def find(v: int) -> int:
        while parent[v] != v:
            parent[v] = parent[parent[v]]
            v = parent[v]
        return v

    for index in indices:
        left, right, _ = EDGES[index]
        rl, rr = find(left), find(right)
        if rl == rr:
            return False, False
        parent[rl] = rr
    return True, find(1) == find(2)


def reconstruct() -> tuple[sp.Expr, sp.Expr, int, int]:
    P = 0
    Q = 0
    forests = 0
    connected_forests = 0
    all_indices = set(range(len(EDGES)))
    for size in range(len(EDGES) + 1):
        for chosen in combinations(range(len(EDGES)), size):
            is_forest, endpoints_connected = forest_and_connected(chosen)
            if not is_forest:
                continue
            forests += 1
            complement = sorted(all_indices - set(chosen))
            monomial = prod((EDGES[index][2] for index in complement), start=sp.Integer(1))
            P += monomial
            if endpoints_connected:
                connected_forests += 1
                Q += monomial
    return sp.expand(P), sp.expand(Q), forests, connected_forests


def main() -> None:
    P, Q, forest_count, connected_count = reconstruct()
    shifted = {a: x - 1, b: y - 1, c: z - 1, d: w - 1}
    Ps = sp.expand(P.subs(shifted))
    Qs = sp.expand(Q.subs(shifted))
    T = x * y * z - 1
    L = x * z + y - 2
    K = x + y * z - 2

    assert forest_count == 82 and connected_count == 30
    assert sp.expand(Ps - (w * T**2 - L**2)) == 0
    Q0 = sp.expand(Qs.subs(w, 0))
    assert sp.expand(Qs - (w * K**2 + Q0)) == 0

    # Boundary numerator before any division.
    numerator = sp.expand(T**2 * Q0 + K**2 * L**2)
    A = sp.expand(
        x**2*y**2 + 2*x**2*y + x**2 + 2*x*y**2
        - 4*x*y - 2*x + y**2 - 2*y + 5
    )
    B = sp.expand(
        2*u**3 + A*u**2
        + 2*u*((x - 1)**2 + (y - 1)**2)
        + (x - 1)**2*(y - 1)**2
    )
    substituted = sp.cancel(numerator.subs(z, (u + 1)/(x*y)))
    target = sp.cancel((x - 1)**2*(y - 1)**2*B/(x**2*y**2))
    assert sp.cancel(substituted - target) == 0

    poly_A = sp.Poly(A, x)
    assert poly_A.degree() == 2
    assert sp.expand(poly_A.LC() - (y + 1)**2) == 0
    discriminant = sp.factor(sp.discriminant(A, x))
    assert sp.expand(discriminant + 16*(y**3 + y + 1)) == 0

    # Equality cases are checked as polynomial identities before sign use.
    assert sp.expand(K.subs(x, 1) - T.subs(x, 1)) == 0
    assert sp.expand(K.subs(y, 1) - (x + z - 2)) == 0

    anchor = {x: 2, y: 2, z: 2, w: 2}
    assert T.subs(anchor) == 7 and Ps.subs(anchor) > 0 and Qs.subs(anchor) > 0

    endpoint = {
        x: sp.Rational(-13, 20),
        y: sp.Rational(12, 25),
        z: sp.Rational(11, 2),
        w: sp.Rational(79, 10),
    }
    assert T.subs(endpoint) == sp.Rational(-679, 250)
    assert Ps.subs(endpoint) == sp.Rational(161582787, 5000000) > 0
    assert Qs.subs(endpoint) == sp.Rational(-346833, 500000) < 0

    print(json.dumps({
        "schema": "amra.opg1757.full-rim-independent-audit.v1",
        "reconstruction": {
            "deletion_forests": forest_count,
            "endpoint_connected_forests": connected_count,
            "P_at_ones": int(P.subs({a: 1, b: 1, c: 1, d: 1})),
            "Q_at_ones": int(Q.subs({a: 1, b: 1, c: 1, d: 1})),
        },
        "identities": {
            "P_shifted": "w*(x*y*z-1)^2-(x*z+y-2)^2",
            "Q_shifted": "w*(x+y*z-2)^2+Q0",
            "boundary_numerator": "(x-1)^2*(y-1)^2*B/(x^2*y^2)",
            "A_leading_coefficient": "(y+1)^2",
            "A_discriminant": str(discriminant),
        },
        "component": {
            "anchor_T": 7,
            "claimed_open_branch": "x,y,z>0; T>0; w>L^2/T^2",
            "coarse_endpoint_T": "-679/250",
        },
        "verdict": "symbolic reconstruction passes; topological and strict-equality proof recorded separately",
        "scope": "W4 rim four-variable stabilizer specialization only",
        "public_problem_closed": False,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
