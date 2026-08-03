#!/usr/bin/env python3
r"""Exact low-dimensional probes for the two edge orbits of W4.

This is routing evidence, not a proof of full Fang--Ma domination.  For each
marked-edge orbit it enumerates C_{M\e} and xi_e exactly, specializes by the
marked-edge stabilizer, and checks exact one-coordinate boundary channels.

On a channel (a,b,c,d)=(t,1,1,1), etc., the distinguished component is
rigorously the interval to the right of the largest real C_delete root: the
interval contains t>0 and gives an explicit path inside {C_delete>0} to the
positive orthant.  No analogous claim is made for arbitrary points of the
four- or two-variable specializations.
"""

from __future__ import annotations

from collections import Counter
import json
from pathlib import Path

import sympy as sp


VERTICES = tuple(range(5))
CENTER = 0
SPOKES = ((0, 1), (0, 2), (0, 3), (0, 4))
RIM = ((1, 2), (2, 3), (3, 4), (1, 4))
EDGES = SPOKES + RIM
A, B, C, D, T = sp.symbols("a b c d t", real=True)
VARS = (A, B, C, D)


def is_forest(edges: tuple[tuple[int, int], ...]) -> bool:
    parent = list(VERTICES)

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for u, v in edges:
        ru, rv = find(u), find(v)
        if ru == rv:
            return False
        parent[ru] = rv
    return True


def connected(edges: tuple[tuple[int, int], ...], source: int, target: int) -> bool:
    adjacency = {v: [] for v in VERTICES}
    for u, v in edges:
        adjacency[u].append(v)
        adjacency[v].append(u)
    seen = {source}
    stack = [source]
    while stack:
        u = stack.pop()
        for v in adjacency[u]:
            if v not in seen:
                seen.add(v)
                stack.append(v)
    return target in seen


def orbit_variable(edge: tuple[int, int], orbit: str) -> sp.Symbol:
    if orbit == "spoke":
        # Mark 01.  Reflection in 01 interchanges 2 and 4.
        classes = {
            A: {(0, 2), (0, 4)},
            B: {(0, 3)},
            C: {(1, 2), (1, 4)},
            D: {(2, 3), (3, 4)},
        }
    elif orbit == "rim":
        # Mark 12.  Its stabilizing reflection interchanges 1<->2 and 3<->4.
        classes = {
            A: {(0, 1), (0, 2)},
            B: {(0, 3), (0, 4)},
            C: {(2, 3), (1, 4)},
            D: {(3, 4)},
        }
    else:
        raise ValueError(orbit)
    for variable, members in classes.items():
        if edge in members:
            return variable
    raise ValueError((orbit, edge))


def enumerate_orbit(marked: tuple[int, int], orbit: str) -> tuple[sp.Expr, sp.Expr]:
    unmarked = tuple(e for e in EDGES if e != marked)
    c_delete = 0
    xi = 0
    for mask in range(1 << len(unmarked)):
        independent = tuple(
            unmarked[i] for i in range(len(unmarked)) if mask & (1 << i)
        )
        if not is_forest(independent):
            continue
        complement = tuple(e for e in unmarked if e not in independent)
        monomial = sp.prod(orbit_variable(e, orbit) for e in complement)
        c_delete += monomial
        # I is independent after contracting marked iff I+marked is a forest,
        # i.e. iff the marked endpoints are not connected by I.  The exact
        # difference therefore counts the connected deletion forests.
        if connected(independent, *marked):
            xi += monomial
    return sp.expand(c_delete), sp.expand(xi)


def channel_data(c_delete: sp.Expr, xi: sp.Expr, variable: sp.Symbol,
                 rho: str, xi_boundary: str) -> dict[str, object]:
    substitution = {v: sp.Integer(1) for v in VARS}
    substitution[variable] = T
    f = sp.factor(c_delete.subs(substitution))
    x = sp.factor(xi.subs(substitution))
    return {
        "variable": str(variable),
        "C_delete": str(f),
        "xi": str(x),
        "distinguished_interval": f"t > {rho}",
        "xi_boundary": xi_boundary,
        "exact_conclusion": "xi > 0 throughout the distinguished interval",
        "membership_reason": (
            "The interval is the C_delete>0 component containing t>0; "
            "varying t inside it is an explicit path to the positive orthant."
        ),
    }


def main() -> None:
    spoke_f, spoke_x = enumerate_orbit((0, 1), "spoke")
    rim_f, rim_x = enumerate_orbit((1, 2), "rim")

    # Exact one-coordinate polynomials and root-order conclusions.
    spoke_channels = [
        channel_data(spoke_f, spoke_x, A, "(-11 + sqrt(31))/15",
                     "largest xi root = -2 + 2*sqrt(6)/3 < C_delete boundary"),
        channel_data(spoke_f, spoke_x, B, "-16/27",
                     "xi root = -8/11 < -16/27"),
        channel_data(spoke_f, spoke_x, C, "-1 + sqrt(15)/6",
                     "xi root = -5/14 < C_delete boundary"),
        channel_data(spoke_f, spoke_x, D, "(-11 + sqrt(31))/15",
                     "largest xi root = (-5 + sqrt(7))/6 < C_delete boundary"),
    ]
    rim_channels = [
        channel_data(rim_f, rim_x, A, "(-10 + sqrt(2))/14",
                     "xi has negative discriminant and positive leading coefficient"),
        channel_data(rim_f, rim_x, B, "(-21 + 9*sqrt(2))/31",
                     "largest xi root = (-4 + sqrt(6))/5 < C_delete boundary"),
        channel_data(rim_f, rim_x, C, "(-10 + sqrt(2))/14",
                     "xi has negative discriminant and positive leading coefficient"),
        channel_data(rim_f, rim_x, D, "-33/49",
                     "xi root = -7/8 < -33/49"),
    ]

    # Natural two-variable slice: merge all remaining spokes to a and all
    # remaining rim edges to c.  These exact division identities expose the
    # xi=0 boundary but do not identify the full two-dimensional component.
    natural = {B: A, D: C}
    sf2 = sp.factor(spoke_f.subs(natural))
    sx2 = sp.factor(spoke_x.subs(natural))
    rf2 = sp.factor(rim_f.subs(natural))
    rx2 = sp.factor(rim_x.subs(natural))
    ps = sp.cancel(sf2 / C)
    qs = sp.cancel(sx2 / (2 * C))
    pr = rf2
    qr = rx2
    spoke_identity = sp.expand(
        (A + 1) * ps - (A**2 * C + 2*A*C + 3*A + C + 2) * qs
        - A**2 * (4*A**2 - 2*A - C)
    )
    rim_remainder = (
        A**4 + 6*A**3 + 2*A**2*C**2 + 7*A**2*C + 8*A**2
        + 4*A*C**2 + 8*A*C + 2*C**2
    )
    rim_identity = sp.expand(pr - (A + 1)**2 * qr + A**2 * rim_remainder)
    assert spoke_identity == 0
    assert rim_identity == 0

    expected_channels = {
        "spoke": {
            "a": (2*(15*T**2 + 22*T + 6), 2*(3*T**2 + 12*T + 4)),
            "b": (2*(27*T + 16), 2*(11*T + 8)),
            "c": (2*(12*T**2 + 24*T + 7), 2*(14*T + 5)),
            "d": (2*(15*T**2 + 22*T + 6), 2*(6*T**2 + 10*T + 3)),
        },
        "rim": {
            "a": (2*(14*T**2 + 20*T + 7), 2*(2*T**2 + 6*T + 7)),
            "b": (31*T**2 + 42*T + 9, 2*(5*T**2 + 8*T + 2)),
            "c": (2*(14*T**2 + 20*T + 7), 7*T**2 + 14*T + 9),
            "d": (49*T + 33, 2*(8*T + 7)),
        },
    }
    for orbit, f, x in (("spoke", spoke_f, spoke_x), ("rim", rim_f, rim_x)):
        for variable in VARS:
            sub = {v: sp.Integer(1) for v in VARS}
            sub[variable] = T
            ef, ex = expected_channels[orbit][str(variable)]
            assert sp.expand(f.subs(sub) - ef) == 0
            assert sp.expand(x.subs(sub) - ex) == 0

    # Exact comparisons between every real xi boundary and the rightmost
    # C_delete boundary.  The two omitted rim channels have xi discriminant
    # < 0 and positive leading coefficient.
    boundary_gaps = (
        (-11 + sp.sqrt(31))/15 - (-2 + 2*sp.sqrt(6)/3),
        sp.Rational(-16, 27) - sp.Rational(-8, 11),
        -1 + sp.sqrt(15)/6 - sp.Rational(-5, 14),
        (-11 + sp.sqrt(31))/15 - (-5 + sp.sqrt(7))/6,
        (-21 + 9*sp.sqrt(2))/31 - (-4 + sp.sqrt(6))/5,
        sp.Rational(-33, 49) - sp.Rational(-7, 8),
    )
    assert all(sp.ask(sp.Q.positive(gap)) is True for gap in boundary_gaps)
    assert sp.discriminant(2*T**2 + 6*T + 7, T) < 0
    assert sp.discriminant(7*T**2 + 14*T + 9, T) < 0

    result = {
        "host": "W4 (wheel on five vertices, eight edges)",
        "scope": (
            "Exact stabilizer-orbit specializations and rigorous "
            "one-coordinate component channels only; no full domination claim."
        ),
        "spoke_orbit": {
            "marked_edge": [0, 1],
            "variable_classes": {
                "a": ["02", "04"], "b": ["03"],
                "c": ["12", "14"], "d": ["23", "34"],
            },
            "C_delete": str(spoke_f),
            "xi": str(spoke_x),
            "C_delete_at_ones": int(spoke_f.subs(dict.fromkeys(VARS, 1))),
            "xi_at_ones": int(spoke_x.subs(dict.fromkeys(VARS, 1))),
            "one_coordinate_channels": spoke_channels,
            "natural_two_variable": {
                "substitution": "b=a, d=c",
                "C_delete": str(sf2),
                "xi": str(sx2),
                "boundary_identity": (
                    "(a+1) P - (a^2*c+2*a*c+3*a+c+2) Q "
                    "= a^2*(4*a^2-2*a-c), where C_delete=c*P and xi=2*c*Q"
                ),
                "component_claim": "none beyond explicitly pathed channels",
            },
        },
        "rim_orbit": {
            "marked_edge": [1, 2],
            "variable_classes": {
                "a": ["01", "02"], "b": ["03", "04"],
                "c": ["23", "14"], "d": ["34"],
            },
            "C_delete": str(rim_f),
            "xi": str(rim_x),
            "C_delete_at_ones": int(rim_f.subs(dict.fromkeys(VARS, 1))),
            "xi_at_ones": int(rim_x.subs(dict.fromkeys(VARS, 1))),
            "one_coordinate_channels": rim_channels,
            "natural_two_variable": {
                "substitution": "b=a, d=c",
                "C_delete": str(rf2),
                "xi": str(rx2),
                "boundary_identity": (
                    "P-(a+1)^2 Q = -a^2 R, where Q=xi and "
                    "R=a^4+6*a^3+2*a^2*c^2+7*a^2*c+8*a^2+"
                    "4*a*c^2+8*a*c+2*c^2"
                ),
                "component_claim": "none beyond explicitly pathed channels",
            },
        },
        "disposition": (
            "Neither edge orbit is killed.  xi is exactly positive on every "
            "audited distinguished one-coordinate channel.  The two boundary "
            "identities are candidates for a later SOS/component argument."
        ),
    }
    output = Path(__file__).with_suffix(".json")
    output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
