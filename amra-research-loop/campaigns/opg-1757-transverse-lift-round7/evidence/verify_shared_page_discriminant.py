#!/usr/bin/env python3
"""Exact shared-page activity discriminant certificate (stdlib only)."""

from __future__ import annotations

from hashlib import sha256
import json

from verify_c_zero_fibre import (
    EDGES,
    EDGE_INDEX,
    add,
    canonical,
    derivative,
    multiply,
    reconstruct_original,
    restrict_original_zero,
)


B_EDGE = (0, 4)
X01 = (0, 1)
X02 = (0, 2)
C_EDGE = (1, 2)
X13 = (1, 3)
X23 = (2, 3)
X14 = (1, 4)
X24 = (2, 4)


def scale(poly, scalar):
    return {monomial: scalar * coefficient for monomial, coefficient in poly.items() if scalar}


def edge_power(edge, degree):
    monomial = [0] * len(EDGES)
    monomial[EDGE_INDEX[edge]] = degree
    return {tuple(monomial): 1}


def coefficient(poly, edge, degree):
    slot = EDGE_INDEX[edge]
    result = {}
    for monomial, value in poly.items():
        if monomial[slot] != degree:
            continue
        reduced = list(monomial)
        reduced[slot] = 0
        result[tuple(reduced)] = value
    return result


def divide_monomial(poly, factors):
    result = {}
    for monomial, coefficient_value in poly.items():
        reduced = list(monomial)
        for edge, degree in factors.items():
            slot = EDGE_INDEX[edge]
            assert reduced[slot] >= degree
            reduced[slot] -= degree
        result[tuple(reduced)] = coefficient_value
    return result


def permute_edges(poly, edge_map):
    index_map = {EDGE_INDEX[edge]: EDGE_INDEX[edge_map.get(edge, edge)] for edge in EDGES}
    result = {}
    for monomial, coefficient_value in poly.items():
        transformed = [0] * len(EDGES)
        for old_slot, degree in enumerate(monomial):
            transformed[index_map[old_slot]] = degree
        result[tuple(transformed)] = coefficient_value
    return result


def digest(poly):
    return sha256(canonical(poly).encode()).hexdigest()


def main():
    deletion, connectivity, forest_count, connected_count = reconstruct_original()
    assert (forest_count, connected_count) == (128, 58)
    a_slope = derivative(deletion, (B_EDGE,))
    c_zero = restrict_original_zero(deletion, B_EDGE)
    d_slope = derivative(connectivity, (B_EDGE,))
    e_zero = restrict_original_zero(connectivity, B_EDGE)
    delta = add(multiply(a_slope, e_zero), multiply(d_slope, c_zero), -1)

    a2 = coefficient(delta, X01, 2)
    a1 = coefficient(delta, X01, 1)
    a0 = coefficient(delta, X01, 0)
    assert delta == add(
        add(a0, multiply(a1, edge_power(X01, 1))),
        multiply(a2, edge_power(X01, 2)),
    )
    assert (len(a2), len(a1), len(a0)) == (149, 25, 4)
    assert all(value > 0 for poly in (a2, a1, a0) for value in poly.values())

    discriminant = add(multiply(a1, a1), multiply(a2, a0), -4)
    divided_discriminant = divide_monomial(
        discriminant,
        {C_EDGE: 2, X02: 2, X13: 2, X14: 2},
    )
    assert all(value % 4 == 0 for value in divided_discriminant.values())
    H = {monomial: -value // 4 for monomial, value in divided_discriminant.items()}
    assert discriminant == scale(
        multiply(
            multiply(
                multiply(
                    multiply(H, edge_power(C_EDGE, 2)),
                    edge_power(X02, 2),
                ),
                edge_power(X13, 2),
            ),
            edge_power(X14, 2),
        ),
        -4,
    )
    assert len(H) == 215
    assert min(H.values()) == 1 and max(H.values()) == 12
    assert all(value > 0 for value in H.values())

    # Hub exchange gives the identical statement for x02.
    hub_swap = {
        X01: X02,
        X02: X01,
        X13: X23,
        X23: X13,
        X14: X24,
        X24: X14,
    }
    b2 = coefficient(delta, X02, 2)
    b1 = coefficient(delta, X02, 1)
    b0 = coefficient(delta, X02, 0)
    discriminant_x02 = add(multiply(b1, b1), multiply(b2, b0), -4)
    assert discriminant_x02 == permute_edges(discriminant, hub_swap)

    records = {
        "Delta_b": delta,
        "x01_quadratic": a2,
        "x01_linear": a1,
        "x01_constant": a0,
        "x01_discriminant": discriminant,
        "positive_residual_H": H,
        "x02_discriminant": discriminant_x02,
    }
    print(json.dumps({
        "schema": "amra.opg1757.round7.shared-page-discriminant.v1",
        "reconstruction": {
            "deletion_forests": forest_count,
            "endpoint_connected_forests": connected_count,
            "Delta_b_original_terms": len(delta),
        },
        "x01_quadratic": {
            "formula": "Delta_b=A2*x01^2+A1*x01+A0",
            "term_counts": {"A2": len(a2), "A1": len(a1), "A0": len(a0)},
            "all_coefficient_polynomials_positive": True,
            "discriminant": "A1^2-4*A2*A0=-4*c^2*x02^2*x13^2*x14^2*H",
            "H_terms": len(H),
            "H_coefficient_range": [min(H.values()), max(H.values())],
        },
        "consequence": "Delta_b>=0 for arbitrary real x01 when c,x02,x13,x23,x14,x24>=0; hub exchange gives the same theorem for x02",
        "nonnegative_route_sign_chambers_added": ["LPP", "RPP"],
        "combined_nonnegative_route_coverage": "13 of 27 chambers together with NONNEGATIVE_ROUTE_CHAMBERS.md",
        "records": {
            name: {"terms": len(poly), "sha256": digest(poly)}
            for name, poly in records.items()
        },
        "scope": "exact coordinate-discriminant theorem; other multiple-negative chambers and negative effective routes remain open",
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
