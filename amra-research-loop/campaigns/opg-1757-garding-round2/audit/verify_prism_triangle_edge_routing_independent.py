#!/usr/bin/env python3
"""Independent reconstruction of the prism triangle-edge routing evidence."""

from itertools import permutations
import json
import sympy as sp


vertices = tuple(range(6))
marked = frozenset((0, 1))
graph_edges = tuple(map(frozenset, (
    (0, 1), (1, 2), (2, 0),
    (3, 4), (4, 5), (5, 3),
    (0, 3), (1, 4), (2, 5),
)))
edge_set = frozenset(graph_edges)
unmarked = tuple(sorted(
    (tuple(sorted(e)) for e in edge_set if e != marked),
))


def image_edge(perm, e):
    a, b = e
    return frozenset((perm[a], perm[b]))


automorphisms = []
stabilizer = []
for perm in permutations(vertices):
    if frozenset(image_edge(perm, tuple(e)) for e in edge_set) != edge_set:
        continue
    automorphisms.append(perm)
    if image_edge(perm, tuple(marked)) == marked:
        stabilizer.append(perm)

assert len(automorphisms) == 12
assert len(stabilizer) == 2

unseen = set(unmarked)
orbits = []
while unseen:
    seed = min(unseen)
    orbit = {
        tuple(sorted(image_edge(perm, seed))) for perm in stabilizer
    }
    orbits.append(tuple(sorted(orbit)))
    unseen -= orbit
orbits.sort(key=lambda orbit: (len(orbit), orbit))
assert sorted(map(len, orbits)) == [1, 1, 2, 2, 2]

orbit_index = {
    edge: index for index, orbit in enumerate(orbits) for edge in orbit
}


def components(selected_edges):
    adjacency = {v: set() for v in vertices}
    for a, b in selected_edges:
        adjacency[a].add(b)
        adjacency[b].add(a)
    component = {}
    number = 0
    for start in vertices:
        if start in component:
            continue
        stack = [start]
        component[start] = number
        while stack:
            current = stack.pop()
            for nxt in adjacency[current]:
                if nxt not in component:
                    component[nxt] = number
                    stack.append(nxt)
        number += 1
    return component, number


# Coefficient dictionaries are reconstructed without using the candidate
# verifier's symbolic forest loop.
p_coefficients = {}
q_coefficients = {}
forest_count = connected_count = 0
for mask in range(1 << len(unmarked)):
    selected = tuple(
        unmarked[i] for i in range(len(unmarked)) if mask & (1 << i)
    )
    component, component_count = components(selected)
    if len(selected) != len(vertices) - component_count:
        continue
    forest_count += 1
    exponent = [0] * len(orbits)
    for i, graph_edge in enumerate(unmarked):
        if not mask & (1 << i):
            exponent[orbit_index[graph_edge]] += 1
    exponent = tuple(exponent)
    p_coefficients[exponent] = p_coefficients.get(exponent, 0) + 1
    if component[0] == component[1]:
        connected_count += 1
        q_coefficients[exponent] = q_coefficients.get(exponent, 0) + 1

assert (forest_count, connected_count) == (190, 66)
assert (len(p_coefficients), len(q_coefficients)) == (79, 35)

u = sp.symbols("u0:5")


def polynomial(coefficients):
    return sp.Add(*(
        coefficient * sp.prod(u[i] ** exponent[i] for i in range(5))
        for exponent, coefficient in coefficients.items()
    ))


P5 = sp.expand(polynomial(p_coefficients))
Q5 = sp.expand(polynomial(q_coefficients))
assert P5.subs(dict.fromkeys(u, 1)) == 190
assert Q5.subs(dict.fromkeys(u, 1)) == 66

# Identify the orbit types intrinsically.
triangle_edges = {
    tuple(sorted(e)) for e in ((0, 1), (1, 2), (2, 0), (3, 4), (4, 5), (5, 3))
}
vertical_edges = {tuple(sorted(e)) for e in ((0, 3), (1, 4), (2, 5))}
size_two_triangles = [i for i, orbit in enumerate(orbits)
                      if len(orbit) == 2 and set(orbit) <= triangle_edges]
singletons = [i for i, orbit in enumerate(orbits) if len(orbit) == 1]
size_two_vertical = [i for i, orbit in enumerate(orbits)
                     if len(orbit) == 2 and set(orbit) <= vertical_edges]
assert tuple(map(len, (size_two_triangles, singletons, size_two_vertical))) == (2, 2, 1)

x, y, z = sp.symbols("x y z")
substitution = {}
for i in size_two_triangles:
    substitution[u[i]] = x - 1
for i in singletons:
    substitution[u[i]] = y - 1
for i in size_two_vertical:
    substitution[u[i]] = z - 1
P = sp.expand(P5.subs(substitution))
Q = sp.expand(Q5.subs(substitution))

P_expected = (
    x**4*y**2*z**2 - x**2*y*z**2 - 2*x**2*y*z - x**2*y
    - 2*x**2*z + 4*x*z + 4*x - y**2 + 4*y - 6
)
Q_expected = (
    x**4*y + x**2*y**2*z**2 + x**2*y**2 + 2*x**2*y*z
    - 4*x**2*y + 2*x**2*z - 8*x**2 - 4*x*y*z - 4*x*y
    - 8*x*z + 24*x - 2*y**2 - y*z**2 + 10*y + 8*z - 18
)
assert sp.expand(P - P_expected) == 0
assert sp.expand(Q - Q_expected) == 0

resultant = sp.expand(sp.resultant(P, Q, x))
known = y**2 * (y - 1)**4 * (z - 1)**2 * (y*z + y - 2)**2
quotient, remainder = sp.div(resultant, known, y, z)
assert remainder == 0
residual = sp.expand(quotient)
resultant_poly = sp.Poly(resultant, y, z)
residual_poly = sp.Poly(residual, y, z)
assert (resultant_poly.total_degree(), len(resultant_poly.terms())) == (28, 166)
assert (residual_poly.total_degree(), len(residual_poly.terms())) == (16, 52)

residual_factorization = sp.factor_list(residual)
nonconstant_residual_factors = [
    (factor, exponent) for factor, exponent in residual_factorization[1]
    if sp.Poly(factor, y, z).total_degree() > 0
]
residual_is_polynomial_square_up_to_constant = all(
    exponent % 2 == 0 for _, exponent in nonconstant_residual_factors
)

point = {x: sp.Rational(3, 2), y: sp.Rational(1, 2), z: 1}
assert P.subs(point) == sp.Rational(1, 64)
assert Q.subs(point) == -sp.Rational(3, 32)
assert sp.rem(P.subs(z, 1), x - 1, x) == 0
assert sp.rem(Q.subs(z, 1), x - 1, x) == 0
assert sp.factor(P.subs({z: 1, y: sp.Rational(1, 2)})) == (
    (x - 1) * (x**3 + x**2 - 15*x + 17) / 4
)
assert P.subs({x: 2, y: sp.Rational(1, 2), z: 1}) < 0

print(json.dumps({
    "schema": "amra.opg1757.prism-triangle-edge-routing-independent-audit.v1",
    "automorphism_group_order": len(automorphisms),
    "marked_edge_stabilizer_order": len(stabilizer),
    "orbits": [[list(edge) for edge in orbit] for orbit in orbits],
    "orbit_sizes": sorted(map(len, orbits)),
    "forest_count": forest_count,
    "endpoint_connected_count": connected_count,
    "five_variable_term_counts": {"P": len(p_coefficients), "xi": len(q_coefficients)},
    "three_variable_polynomials_match": True,
    "resultant": {"total_degree": 28, "term_count": 166},
    "known_factor_total_degree": sp.Poly(known, y, z).total_degree(),
    "residual": {
        "total_degree": 16,
        "term_count": 52,
        "factor_degrees_and_exponents": [
            [sp.Poly(factor, y, z).total_degree(), exponent]
            for factor, exponent in nonconstant_residual_factors
        ],
        "is_polynomial_square_up_to_constant": residual_is_polynomial_square_up_to_constant,
    },
    "negative_point": {"P": "1/64", "xi": "-3/32"},
    "z1_wall_and_direct_x_obstruction_verified": True,
    "component_membership_of_negative_point": "not_established",
    "public_or_component_counterexample": False,
}, indent=2, sort_keys=True))
