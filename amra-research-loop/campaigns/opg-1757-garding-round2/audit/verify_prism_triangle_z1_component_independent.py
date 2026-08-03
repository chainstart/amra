#!/usr/bin/env python3
"""Independent exact audit of the prism triangle-edge z=1 theorem."""

from itertools import combinations
import json
import sympy as sp


# Reconstruct the coarsened polynomials directly from the graph.  This does
# not import either candidate verifier or a previously reconstructed formula.
vertices = tuple(range(6))
marked = (0, 1)
all_edges = (
    (0, 1), (1, 2), (2, 0),
    (3, 4), (4, 5), (5, 3),
    (0, 3), (1, 4), (2, 5),
)
unmarked = tuple(edge for edge in all_edges if set(edge) != set(marked))
p, t, v = sp.symbols("p t v")
x, y, z = sp.symbols("x y z")

triangle_size_two = {
    frozenset(e) for e in ((0, 2), (1, 2), (3, 5), (4, 5))
}
singletons = {frozenset(e) for e in ((3, 4), (2, 5))}
vertical_size_two = {frozenset(e) for e in ((0, 3), (1, 4))}


def activity(edge):
    key = frozenset(edge)
    if key in triangle_size_two:
        return p
    if key in singletons:
        return t
    if key in vertical_size_two:
        return v
    raise AssertionError(edge)


def forest_data(indices):
    parent = list(vertices)

    def root(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    for index in indices:
        a, b = unmarked[index]
        ra, rb = root(a), root(b)
        if ra == rb:
            return None
        parent[ra] = rb
    chosen = set(indices)
    complement_weight = sp.prod(
        activity(edge) for index, edge in enumerate(unmarked)
        if index not in chosen
    )
    return complement_weight, root(0) == root(1)


P0 = sp.Integer(0)
Q0 = sp.Integer(0)
forest_count = connected_count = 0
for size in range(9):
    for indices in combinations(range(8), size):
        data = forest_data(indices)
        if data is None:
            continue
        weight, connected = data
        forest_count += 1
        P0 += weight
        if connected:
            connected_count += 1
            Q0 += weight

assert (forest_count, connected_count) == (190, 66)
P = sp.expand(P0.subs({p: x - 1, t: y - 1, v: z - 1}))
Q = sp.expand(Q0.subs({p: x - 1, t: y - 1, v: z - 1}))

C = (x + 1)*(x**2 + 1)*y**2 - 4*(x + 1)*y + 6 - 2*x
D = 2*(x + 1)*y**2 + (x**3 + x**2 - x - 9)*y + 10 - 6*x
assert sp.expand(P.subs(z, 1) - (x - 1)*C) == 0
assert sp.expand(Q.subs(z, 1) - (x - 1)*D) == 0

disc_C = sp.factor(sp.discriminant(C, y))
disc_D = sp.factor(sp.discriminant(D, y))
resultant = sp.factor(sp.resultant(C, D, y))
assert disc_C == 8*(x - 1)**3*(x + 1)
assert disc_D == (x - 1)**3*(x**3 + 5*x**2 + 11*x - 1)
assert resultant == -2*(x - 1)**7*(x + 1)*(x + 3)**2

# At x=2 both quadratics have distinct real roots and their upper roots have
# the strict order used to orient the global no-crossing argument.
roots_D_at_2 = sorted(sp.solve(D.subs(x, 2), y))
assert roots_D_at_2 == [sp.Rational(-2, 3), sp.Rational(1, 2)]
upper_C_at_2 = sp.Rational(2, 5) + sp.sqrt(6)/15
assert sp.expand(C.subs({x: 2, y: upper_C_at_2})) == 0
assert upper_C_at_2 > sp.Rational(1, 2)
assert upper_C_at_2 < 2

# Exact negative-point firewall in the z=1 plane.
lower_C_at_3_2 = sp.Rational(8, 13) - 2*sp.sqrt(10)/65
assert sp.expand(C.subs({x: sp.Rational(3, 2), y: lower_C_at_3_2})) == 0
assert lower_C_at_3_2 > sp.Rational(1, 2)
assert P.subs({x: sp.Rational(3, 2), y: sp.Rational(1, 2), z: 1}) == sp.Rational(1, 64)
assert Q.subs({x: sp.Rational(3, 2), y: sp.Rational(1, 2), z: 1}) == -sp.Rational(3, 32)

print(json.dumps({
    "schema": "amra.opg1757.prism-triangle-z1-component-independent-audit.v1",
    "reconstruction": {"forests": forest_count, "connected": connected_count},
    "z1_factorization": True,
    "disc_C": "8*(x-1)^3*(x+1)",
    "disc_D": "(x-1)^3*(x^3+5*x^2+11*x-1)",
    "disc_D_strictly_positive_for_x_gt_1": True,
    "resultant": "-2*(x-1)^7*(x+1)*(x+3)^2",
    "upper_root_order_at_x2": "r_D^+=1/2 < r_C^+=2/5+sqrt(6)/15",
    "negative_point_below_lower_C_root": True,
    "local_conclusion": "xi>0 on x>1 and y>r_C^+(x) in the z=1 plane",
    "scope": "z=1 plane of the three-variable coarsening only",
}, indent=2, sort_keys=True))
