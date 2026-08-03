#!/usr/bin/env python3
"""Blind reconstruction of the K3,3 marked-edge stabilizer certificate.

The graph, forest sums, factors, pseudo-remainder and component walls are
rebuilt here.  No author verifier or generated evidence is imported.
"""

from itertools import combinations
import json
import sympy as sp


a, b, x, y = sp.symbols("a b x y")

# Bipartition {0,1,2}|{3,4,5}; marked edge 03 is deleted.  Its stabilizer
# has the four edges meeting exactly one marked endpoint in one orbit and
# the four remaining edges in the other orbit.
EDGES = (
    (0, 4, a), (0, 5, a), (1, 3, a), (2, 3, a),
    (1, 4, b), (1, 5, b), (2, 4, b), (2, 5, b),
)


def forest_data(selected: tuple[int, ...]):
    parent = list(range(6))

    def root(vertex: int) -> int:
        while parent[vertex] != vertex:
            parent[vertex] = parent[parent[vertex]]
            vertex = parent[vertex]
        return vertex

    for index in selected:
        u, v, _ = EDGES[index]
        ru, rv = root(u), root(v)
        if ru == rv:
            return None
        parent[ru] = rv
    chosen = set(selected)
    monomial = sp.prod(label for index, (_, _, label) in enumerate(EDGES) if index not in chosen)
    return sp.expand(monomial), root(0) == root(3)


def main() -> None:
    deletion = sp.Integer(0)
    connected = sp.Integer(0)
    forest_count = connected_count = 0
    forest_by_size = {str(size): 0 for size in range(9)}
    connected_by_size = {str(size): 0 for size in range(9)}

    for size in range(9):
        for chosen in combinations(range(8), size):
            classified = forest_data(chosen)
            if classified is None:
                continue
            monomial, endpoints_connected = classified
            forest_count += 1
            forest_by_size[str(size)] += 1
            deletion += monomial
            if endpoints_connected:
                connected_count += 1
                connected_by_size[str(size)] += 1
                connected += monomial

    deletion = sp.expand(deletion)
    connected = sp.expand(connected)
    assert forest_count == 194
    assert connected_count == 60
    assert deletion.subs({a: 1, b: 1}) == 194
    assert connected.subs({a: 1, b: 1}) == 60

    shifted_P = sp.expand(deletion.subs({a: x - 1, b: y - 1}))
    shifted_xi = sp.expand(connected.subs({a: x - 1, b: y - 1}))
    expected_F = x**4 * (y**3 + y**2 + y + 1) - 4*x**2*(y + 1) - 2*y + 6
    expected_G = x**2*(y**2 + y + 2) - 2*x*y - 6*x - y + 5
    assert sp.expand(shifted_P - (y - 1)*expected_F) == 0
    assert sp.expand(shifted_xi - 4*(y - 1)*expected_G) == 0
    assert shifted_P.subs({x: 2, y: 2}) == 194
    assert shifted_xi.subs({x: 2, y: 2}) == 60

    pseudo_remainder = sp.factor(sp.prem(expected_F, expected_G, y))
    expected_remainder = -x**4*(x - 1)**4*(y - 1)
    assert sp.expand(pseudo_remainder - expected_remainder) == 0

    quotient, remainder = sp.div(
        sp.Poly(x**4*expected_F - expected_remainder, y),
        sp.Poly(expected_G, y),
    )
    assert remainder.is_zero
    S = sp.factor(quotient.as_expr())
    assert sp.expand(x**4*expected_F - S*expected_G - expected_remainder) == 0

    # Component-wall and exceptional-line checks, kept separate from the
    # symbolic divisibility computation.
    assert sp.expand(shifted_P.subs(y, 1)) == 0
    assert expected_G.subs({x: 2, y: 2}) == 15
    G_on_x0 = sp.factor(expected_G.subs(x, 0))
    F_on_x0 = sp.factor(expected_F.subs(x, 0))
    assert G_on_x0 == 5 - y
    assert F_on_x0.subs(y, 5) == -4

    # At any G-zero with x nonzero, the exact quotient identity forces the
    # displayed nonpositive value on the y>1 side of the wall.
    forced_F_on_G0 = sp.factor(expected_remainder / x**4)
    assert forced_F_on_G0 == -(x - 1)**4*(y - 1)

    print(json.dumps({
        "schema": "amra.opg1757.k33-stabilizer-independent-audit.v1",
        "engine": "blind complement-of-forest reconstruction; no author verifier import",
        "graph": {
            "vertices": 6,
            "marked_edge": [0, 3],
            "unmarked_edges": 8,
            "stabilizer_orbits": {"incident_to_one_marked_endpoint": 4, "other": 4},
        },
        "forest_reconstruction": {
            "deletion_forests": forest_count,
            "endpoint_connected_forests": connected_count,
            "forests_by_selected_edge_count": forest_by_size,
            "connected_by_selected_edge_count": connected_by_size,
            "deletion_polynomial_ab": str(sp.factor(deletion)),
            "connected_polynomial_ab": str(sp.factor(connected)),
        },
        "shifted_polynomials": {
            "P": str(sp.factor(shifted_P)),
            "xi": str(sp.factor(shifted_xi)),
            "F": str(expected_F),
            "G": str(expected_G),
            "anchor": {"x": 2, "y": 2, "P": 194, "xi": 60, "G": 15},
        },
        "pseudo_division": {
            "prem_y_F_G": str(pseudo_remainder),
            "exact_quotient_S": str(S),
            "identity": "x^4 F = S G - x^4 (x-1)^4 (y-1)",
        },
        "component_checks": {
            "y_equals_1_is_P_zero_wall": True,
            "anchor_side": "y>1",
            "P_positive_implies_F_positive_on_anchor_side": True,
            "G_zero_x_nonzero_forces_F": "-(x-1)^4*(y-1)<=0",
            "x_zero_exception": "G=5-y; its zero y=5 has F=-4",
            "G_anchor_sign": "positive (15)",
            "continuity_conclusion": "G has no zero on the connected distinguished component, hence keeps its positive anchor sign",
            "xi_conclusion": "4*(y-1)*G>0",
        },
        "statement_match": "complete two-dimensional stabilizer specialization only",
        "scope": "not eight independent unmarked-edge variables; not G201, the global moving-edge lemma, or OPG-1757",
        "public_problem_closed": False,
        "lean_used": False,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
