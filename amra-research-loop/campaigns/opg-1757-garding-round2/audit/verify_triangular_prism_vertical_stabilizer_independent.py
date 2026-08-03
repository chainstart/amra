#!/usr/bin/env python3
"""Blind audit of triangular-prism marked-vertical stabilizer domination."""

from itertools import combinations
import json
import sympy as sp


a, b, c, x, y, z = sp.symbols("a b c x y z")

# Triangles 012 and 345, vertical matching 03,14,25; delete marked 03.
EDGES = (
    (1, 4, a), (2, 5, a),
    (0, 1, b), (0, 2, b), (3, 4, b), (3, 5, b),
    (1, 2, c), (4, 5, c),
)


def classify(selected: tuple[int, ...]):
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
    forests = endpoint_connected = 0
    by_size = {str(size): 0 for size in range(9)}
    connected_by_size = {str(size): 0 for size in range(9)}

    for size in range(9):
        for selected in combinations(range(8), size):
            result = classify(selected)
            if result is None:
                continue
            monomial, joined = result
            forests += 1
            by_size[str(size)] += 1
            deletion += monomial
            if joined:
                endpoint_connected += 1
                connected_by_size[str(size)] += 1
                connected += monomial

    deletion = sp.expand(deletion)
    connected = sp.expand(connected)
    assert forests == 180 and endpoint_connected == 46
    assert deletion.subs({a: 1, b: 1, c: 1}) == 180
    assert connected.subs({a: 1, b: 1, c: 1}) == 46

    shifted_P = sp.expand(deletion.subs({a: x - 1, b: y - 1, c: z - 1}))
    shifted_xi = sp.expand(connected.subs({a: x - 1, b: y - 1, c: z - 1}))
    T = y**2*z - 1
    V = y**2 + z - 2
    A = y*(z + 1) - 2
    B = 2*y + z - 3
    assert sp.expand(shifted_P - ((x*T)**2 - V**2)) == 0
    assert sp.expand(shifted_xi - 2*(x*A**2 - B**2)) == 0
    barrier = sp.factor(V*A**2 - T*B**2)
    assert barrier == (y - 1)**4*(z - 1)**2

    anchor = {x: 2, y: 2, z: 2}
    assert shifted_P.subs(anchor) == 180
    assert shifted_xi.subs(anchor) == 46
    assert T.subs(anchor) == 7 and V.subs(anchor) == 4
    assert A.subs(anchor) == 4 and B.subs(anchor) == 3

    # Exact exceptional-set checks for A=0 together with the zero RHS walls.
    assert sp.factor(A.subs(y, 1)) == z - 1
    assert sp.expand(A.subs(z, 1) - 2*(y - 1)) == 0
    assert sp.factor(B.subs({y: 1, z: 1})) == 0
    assert T.subs({y: 1, z: 1}) == 0

    print(json.dumps({
        "schema": "amra.opg1757.triangular-prism-vertical-independent-audit.v1",
        "engine": "blind complement-of-forest reconstruction; no author verifier import",
        "graph": {
            "vertices": 6,
            "marked_edge": [0, 3],
            "unmarked_edges": 8,
            "stabilizer_orbits": {"other_vertical": 2, "incident_triangle": 4, "opposite_triangle": 2},
        },
        "forest_reconstruction": {
            "deletion_forests": forests,
            "endpoint_connected_forests": endpoint_connected,
            "forests_by_selected_edge_count": by_size,
            "connected_by_selected_edge_count": connected_by_size,
            "deletion_polynomial_abc": str(sp.factor(deletion)),
            "connected_polynomial_abc": str(sp.factor(connected)),
        },
        "identities": {
            "P": "(x*T)^2-V^2",
            "xi": "2*(x*A^2-B^2)",
            "barrier": "V*A^2-T*B^2=(y-1)^4*(z-1)^2",
            "T": str(T), "V": str(V), "A": str(A), "B": str(B),
            "all_verified": True,
        },
        "component_checks": {
            "anchor": {"x": 2, "y": 2, "z": 2, "P": 180, "xi": 46, "T": 7, "V": 4},
            "anchor_branch": "x*T>|V|",
            "sign_propagation": "on its P-positive component x*T>|V| persists; x,T stay positive, T>0 forces z>0 and y nonzero, so anchor sign gives y>0",
            "base_connectedness": "in (log y,log z), y,z>0 and T>0 is the open half-space 2 log y+log z>0",
            "V_strict_AM_GM": "V=y^2+z-2 >= 2*y*sqrt(z)-2 >0 because y^2*z>1",
            "component_equality": "the connected epigraph x>V/T over that base equals the distinguished component",
            "A_zero_exception": "barrier plus T>0 forces B=0 and y=1 or z=1; A=0 then forces y=z=1, contradicting T>0",
            "xi_strictness": "x>V/T, A!=0 and (V/T)A^2-B^2>=0 imply xA^2-B^2>0",
        },
        "statement_match": "marked-vertical-edge three-variable stabilizer slice only",
        "scope": "not the triangle-edge orbit, not eight independent variables, not G201/global/OPG-1757",
        "public_problem_closed": False,
        "lean_used": False,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
