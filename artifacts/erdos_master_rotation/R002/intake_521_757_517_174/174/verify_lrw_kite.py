#!/usr/bin/env python3
"""Symbolic checks for the explicit LRW cyclic kite.

The script verifies the displayed affine parameters, cyclicity relation, and
the absence of parallel opposite-side pairings for transcendental a.  The
non-subtransitivity conclusion itself uses LRW Theorem 1 and is not reproved
by this finite algebra script.
"""

import sympy as sp


a, b, alpha, beta = sp.symbols("a b alpha beta", nonzero=True)
z = sp.Matrix((-1, 0))
y = sp.Matrix((1, 0))
x = sp.Matrix((a, b))
w = sp.Matrix((a, -b))

relation = w - (z + alpha * (x - z) + beta * (y - z))
solution = sp.solve(tuple(relation), (alpha, beta), dict=True)
assert solution == [{alpha: -1, beta: a + 1}]

# On b^2=1-a^2, every point has squared norm one.
norms = [sp.expand(p.dot(p)).subs(b**2, 1 - a**2) for p in (z, y, x, w)]
assert all(sp.simplify(value - 1) == 0 for value in norms)


def determinant(u, v):
    return sp.expand(u[0] * v[1] - u[1] * v[0])


# The three partitions of four vertices into two candidate opposite sides.
parallel_determinants = (
    determinant(y - z, w - x),
    determinant(x - z, w - y),
    determinant(w - z, x - y),
)
assert tuple(sp.factor(value) for value in parallel_determinants) == (
    -4 * b,
    -2 * a * b,
    2 * a * b,
)

print(
    {
        "status": "PASS",
        "lrw_parameters": {"alpha": "-1", "beta": "a+1"},
        "squared_norms_under_b2_eq_1_minus_a2": [str(value) for value in norms],
        "parallel_pair_determinants": [
            str(sp.factor(value)) for value in parallel_determinants
        ],
        "conclusion": (
            "for transcendental -1<a<1, a and b are nonzero; "
            "the four points are cyclic and are not a trapezoid"
        ),
        "scope": "symbolic geometry only; LRW Theorem 1 supplies non-subtransitivity",
    }
)

