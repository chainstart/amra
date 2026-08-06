#!/usr/bin/env python3
"""Discovery-only Schur scan of the 45-channel numerator for each negative route."""

from __future__ import annotations

from itertools import combinations
from pathlib import Path
import sys


EVIDENCE = (
    Path(__file__).parents[1]
    / "campaigns"
    / "opg-1757-transverse-lift-round7"
    / "evidence"
)
sys.path.insert(0, str(EVIDENCE))

from verify_c_zero_fibre import (  # noqa: E402
    add as add_original,
    derivative,
    multiply as multiply_original,
    reconstruct_original,
    restrict_original_zero,
)
from verify_negative_c_direct_chambers import (  # noqa: E402
    add,
    bernstein_transform,
    constant,
    multiply,
    power,
    variable,
)
from verify_route_matrix_chamber import (  # noqa: E402
    B_EDGE,
    NAMES,
    ROUTE_NAMES,
    add as add_route,
    constant as route_constant,
    multiply as multiply_route,
    power as power_route,
    substitute_original,
    variable as route_variable,
)


TAU = 3
H_SLOTS = (4, 5, 6)


def route_orientation_numerator():
    deletion, connectivity, _, _ = reconstruct_original()
    A = derivative(deletion, (B_EDGE,))
    C = restrict_original_zero(deletion, B_EDGE)
    D = derivative(connectivity, (B_EDGE,))
    E = restrict_original_zero(connectivity, B_EDGE)
    delta = add_original(multiply_original(A, E), multiply_original(D, C), -1)
    R0, R3, R4, Rc = (route_variable(name) for name in ROUTE_NAMES)
    h0, h3, h4 = (route_variable(name) for name in ("h0", "h3", "h4"))
    one = route_constant(1)
    factors = {
        (0, 1): add_route(h0, one, -1),
        (0, 2): add_route(
            multiply_route(R0, route_variable("h0", -1)), one, -1
        ),
        B_EDGE: {},
        (1, 2): add_route(Rc, one, -1),
        (1, 3): add_route(h3, one, -1),
        (2, 3): add_route(
            multiply_route(R3, route_variable("h3", -1)), one, -1
        ),
        (1, 4): add_route(h4, one, -1),
        (2, 4): add_route(
            multiply_route(R4, route_variable("h4", -1)), one, -1
        ),
    }
    route_delta = substitute_original(delta, factors)
    return multiply_route(
        route_delta,
        multiply_route(power_route(h0, 2), multiply_route(h3, h4)),
    )


def substitute_negative_route(poly, negative_index):
    positive_indices = tuple(index for index in range(4) if index != negative_index)
    positive_q = {
        index: variable(slot) for slot, index in enumerate(positive_indices)
    }
    P = constant(1)
    for index in positive_indices:
        P = multiply(P, positive_q[index])
    B = P
    for pair in combinations(positive_indices, 2):
        B = add(B, multiply(positive_q[pair[0]], positive_q[pair[1]]))
    negative_floor_numerator = add(B, multiply(variable(TAU), P), -1)
    floors = {}
    for index in range(4):
        if index == negative_index:
            floors[index] = negative_floor_numerator
        else:
            floors[index] = add(constant(1), positive_q[index])
    orientations = {
        NAMES.index("h0"): variable(H_SLOTS[0]),
        NAMES.index("h3"): variable(H_SLOTS[1]),
        NAMES.index("h4"): variable(H_SLOTS[2]),
    }
    negative_slot = negative_index
    negative_degree = max(monomial[negative_slot] for monomial in poly)
    result = {}
    for monomial, value in poly.items():
        term = constant(value)
        for index in range(4):
            term = multiply(term, power(floors[index], monomial[index]))
        term = multiply(term, power(B, negative_degree - monomial[negative_slot]))
        for source_slot, replacement in orientations.items():
            term = multiply(term, power(replacement, monomial[source_slot]))
        result = add(result, term)
    return result


def row(poly):
    values = tuple(poly.values())
    return {
        "terms": len(poly),
        "positive": sum(value > 0 for value in values),
        "negative": sum(value < 0 for value in values),
        "minimum": str(min(values)),
        "maximum": str(max(values)),
        "degrees": [max(monomial[slot] for monomial in poly) for slot in range(8)],
    }


def main():
    numerator = route_orientation_numerator()
    for negative_index, name in enumerate(ROUTE_NAMES):
        schur = substitute_negative_route(numerator, negative_index)
        transformed = bernstein_transform(schur, [TAU])
        print({
            "negative_route": name,
            "schur": row(schur),
            "tau_bernstein": row(transformed),
        }, flush=True)


if __name__ == "__main__":
    main()
