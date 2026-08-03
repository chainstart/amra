#!/usr/bin/env python3
"""Exact falsification witnesses for two round-7 lift mechanisms.

This verifier uses only the Python standard library.  It reconstructs the
deletion and endpoint-connectivity polynomials directly in the eight original
edge variables, rather than trusting the transverse coefficient ledger.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations, product
import json


VERTICES = tuple(range(5))
EDGES = ((0, 1), (0, 2), (0, 4), (1, 2), (1, 3), (1, 4), (2, 3), (2, 4))
MARKED = (0, 3)


def is_forest(edges):
    parent = list(VERTICES)

    def find(vertex):
        while parent[vertex] != vertex:
            parent[vertex] = parent[parent[vertex]]
            vertex = parent[vertex]
        return vertex

    for left, right in edges:
        left_root, right_root = find(left), find(right)
        if left_root == right_root:
            return False
        parent[left_root] = right_root
    return True


def connects_marked(edges):
    adjacency = {vertex: [] for vertex in VERTICES}
    for left, right in edges:
        adjacency[left].append(right)
        adjacency[right].append(left)
    stack, seen = [MARKED[0]], {MARKED[0]}
    while stack:
        vertex = stack.pop()
        for neighbour in adjacency[vertex]:
            if neighbour not in seen:
                seen.add(neighbour)
                stack.append(neighbour)
    return MARKED[1] in seen


def reconstruct_complements():
    deletion, connected = [], []
    for size in range(len(EDGES) + 1):
        for chosen in combinations(EDGES, size):
            if not is_forest(chosen):
                continue
            complement = tuple(edge for edge in EDGES if edge not in chosen)
            deletion.append(complement)
            if connects_marked(chosen):
                connected.append(complement)
    return deletion, connected


def evaluate(complements, weights):
    total = Fraction(0)
    for complement in complements:
        term = Fraction(1)
        for edge in complement:
            term *= weights[edge]
        total += term
    return total


def edge_partial(complements, weights, differentiated_edge):
    total = Fraction(0)
    for complement in complements:
        if differentiated_edge not in complement:
            continue
        term = Fraction(1)
        for edge in complement:
            if edge != differentiated_edge:
                term *= weights[edge]
        total += term
    return total


def derivative_residuals(complements, differentiated_edges):
    differentiated_edges = set(differentiated_edges)
    residuals = {}
    for complement in complements:
        if not differentiated_edges.issubset(complement):
            continue
        residual = tuple(edge for edge in complement if edge not in differentiated_edges)
        residuals[residual] = residuals.get(residual, 0) + 1
    return residuals


def evaluate_residual_polynomial(residuals, weights):
    total = Fraction(0)
    for residual, coefficient in residuals.items():
        term = Fraction(coefficient)
        for edge in residual:
            term *= weights[edge]
        total += term
    return total


def simple_cycles():
    cycles = []
    for size in range(3, len(EDGES) + 1):
        for subset in combinations(EDGES, size):
            degrees = {vertex: 0 for vertex in VERTICES}
            for left, right in subset:
                degrees[left] += 1
                degrees[right] += 1
            if all(degree in (0, 2) for degree in degrees.values()) and sum(
                degree == 2 for degree in degrees.values()
            ) == size:
                cycles.append(subset)
    return cycles


def transverse_weights(u, v, q):
    return {
        (0, 1): 1 + u,
        (0, 2): 1 - u,
        (0, 4): Fraction(1),
        (1, 2): Fraction(1),
        (1, 3): 1 + v,
        (1, 4): 1 + q,
        (2, 3): 1 - v,
        (2, 4): 1 - q,
    }


def independently_even_value(complements, u, v, q):
    total = Fraction(0)
    for sign_u, sign_v, sign_q in product((-1, 1), repeat=3):
        total += evaluate(
            complements,
            transverse_weights(sign_u * u, sign_v * v, sign_q * q),
        )
    return total / 8


def fraction_text(value):
    return str(value.numerator) if value.denominator == 1 else str(value)


def main():
    deletion, connected = reconstruct_complements()
    assert (len(deletion), len(connected)) == (128, 58)

    # Differentiating in every deletion edge except one leaves exactly 1+w_e.
    # Combined with derivative-component nesting, this gives w_e>-1 for all
    # eight original edge activities throughout the distinguished component.
    for retained_edge in EDGES:
        differentiated = set(EDGES) - {retained_edge}
        assert derivative_residuals(deletion, differentiated) == {
            (): 1,
            (retained_edge,): 1,
        }

    # M702: the independent-pair symmetrization is the unique separately
    # symmetric multiaffine polarization of the fixed restriction.  Its
    # deletion polynomial remains positive along this whole anchor ray, but
    # the mixed graph correction overturns the positive xi margin.
    correction_point = (Fraction(-11, 10), Fraction(-4, 5), Fraction(-37, 25))
    u, v, q = correction_point
    full_p = evaluate(deletion, transverse_weights(u, v, q))
    full_xi = evaluate(connected, transverse_weights(u, v, q))
    even_p = independently_even_value(deletion, u, v, q)
    even_xi = independently_even_value(connected, u, v, q)
    p_correction, xi_correction = full_p - even_p, full_xi - even_xi

    # With s=lambda^2, the independently even P along the ray is cubic.
    power_coefficients = (
        Fraction(128),
        -48 * u * u - 38 * v * v - 48 * q * q,
        14 * u * u * v * v + 14 * u * u * q * q + 14 * v * v * q * q,
        -4 * u * u * v * v * q * q,
    )
    c0, c1, c2, c3 = power_coefficients
    bernstein_coefficients = (
        c0,
        c0 + c1 / 3,
        c0 + 2 * c1 / 3 + c2 / 3,
        c0 + c1 + c2 + c3,
    )
    assert bernstein_coefficients == (
        Fraction(128),
        Fraction(122788, 1875),
        Fraction(478091, 18750),
        Fraction(975607, 781250),
    )
    assert all(value > 0 for value in bernstein_coefficients)
    assert even_p == bernstein_coefficients[-1]
    assert even_xi == Fraction(523, 250) > 0
    assert xi_correction == Fraction(-119992, 15625)
    assert full_xi == Fraction(-174609, 31250) < 0

    # M703: positivity of P and of every first edge derivative does not by
    # itself exclude xi<0.  This says nothing about a stronger certificate
    # using higher mixed derivatives or exact component membership.
    derivative_point = (Fraction(59, 22), Fraction(-21, 11), Fraction(29, 11))
    weights = transverse_weights(*derivative_point)
    derivative_p = evaluate(deletion, weights)
    derivative_xi = evaluate(connected, weights)
    first_partials = {edge: edge_partial(deletion, weights, edge) for edge in EDGES}
    assert derivative_p == Fraction(22107148, 1771561) > 0
    assert derivative_xi == Fraction(-256198, 14641) < 0
    assert tuple(first_partials.values()) == (
        Fraction(257492, 161051),
        Fraction(570544, 161051),
        Fraction(812497, 1771561),
        Fraction(55363774, 1771561),
        Fraction(32507183, 322102),
        Fraction(510341, 322102),
        Fraction(755981, 322102),
        Fraction(1325911, 322102),
    )
    assert all(value > 0 for value in first_partials.values())

    # M712 route narrowing: even every simple-cycle derivative inequality,
    # together with P>0 and all edge floors, is too weak.  The simple-cycle
    # identity is partial_(E\C) P = product_(e in C)(1+w_e)-1.
    cycle_point = (
        Fraction(-1, 10),
        Fraction(0),
        Fraction(-2, 5),
        Fraction(1, 5),
        Fraction(-3, 5),
        Fraction(7, 5),
        Fraction(19, 10),
        Fraction(4, 5),
    )
    cycle_weights = dict(zip(EDGES, cycle_point))
    cycle_p = evaluate(deletion, cycle_weights)
    cycle_xi = evaluate(connected, cycle_weights)
    assert cycle_p == Fraction(17, 78125) > 0
    assert cycle_xi == Fraction(-559, 15625) < 0
    assert all(1 + cycle_weights[edge] > 0 for edge in EDGES)

    cycles = simple_cycles()
    assert len(cycles) == 12
    cycle_margins = {}
    for cycle in cycles:
        product_margin = Fraction(1)
        for edge in cycle:
            product_margin *= 1 + cycle_weights[edge]
        product_margin -= 1
        differentiated = set(EDGES) - set(cycle)
        derivative_value = evaluate_residual_polynomial(
            derivative_residuals(deletion, differentiated), cycle_weights
        )
        assert derivative_value == product_margin > 0
        cycle_margins[cycle] = product_margin
    assert min(cycle_margins.values()) == Fraction(11, 250)

    all_derivatives = {}
    for size in range(len(EDGES) + 1):
        for differentiated in combinations(EDGES, size):
            all_derivatives[differentiated] = evaluate_residual_polynomial(
                derivative_residuals(deletion, differentiated), cycle_weights
            )
    nonpositive_derivatives = {
        differentiated: value
        for differentiated, value in all_derivatives.items()
        if value <= 0
    }
    assert len(all_derivatives) == 256
    assert len(nonpositive_derivatives) == 24
    assert min(nonpositive_derivatives.items(), key=lambda item: item[1]) == (
        ((0, 2), (1, 3)),
        Fraction(-54491, 62500),
    )

    print(json.dumps({
        "schema": "amra.opg1757.round7.falsification-witnesses.v2",
        "M702": {
            "transverse_point": [fraction_text(value) for value in correction_point],
            "even_P_ray_bernstein": [fraction_text(value) for value in bernstein_coefficients],
            "even_P_endpoint": fraction_text(even_p),
            "full_P_endpoint": fraction_text(full_p),
            "even_xi_margin": fraction_text(even_xi),
            "xi_mixed_correction": fraction_text(xi_correction),
            "full_xi": fraction_text(full_xi),
            "classification": "unconditional polarization-correction domination is false",
        },
        "M703": {
            "transverse_point": [fraction_text(value) for value in derivative_point],
            "edge_weights": {str(edge): fraction_text(weights[edge]) for edge in EDGES},
            "P": fraction_text(derivative_p),
            "xi": fraction_text(derivative_xi),
            "first_edge_partials": {
                str(edge): fraction_text(first_partials[edge]) for edge in EDGES
            },
            "classification": "P plus all eight first-edge derivative signs do not exclude xi<0",
        },
        "M712_cycle_cone": {
            "edge_weights": {
                str(edge): fraction_text(cycle_weights[edge]) for edge in EDGES
            },
            "P": fraction_text(cycle_p),
            "xi": fraction_text(cycle_xi),
            "edge_floors_positive": 8,
            "simple_cycle_derivatives_positive": len(cycle_margins),
            "minimum_cycle_margin": fraction_text(min(cycle_margins.values())),
            "all_mixed_derivatives_checked": len(all_derivatives),
            "nonpositive_mixed_derivatives": len(nonpositive_derivatives),
            "minimum_mixed_derivative": {
                "edges": [str(edge) for edge in ((0, 2), (1, 3))],
                "value": "-54491/62500",
            },
            "classification": "P, edge floors, and all simple-cycle derivatives do not exclude xi<0",
        },
        "scope": {
            "M702": "does not exclude a correction estimate restricted by additional full-P component inequalities",
            "M703": "does not exclude higher mixed-derivative nesting or prove component membership",
            "M712_cycle_cone": "narrows M712 to genuinely non-circuit mixed derivatives; it does not refute the full derivative-cone mechanism",
            "public_problem_changed": False,
        },
        "full_edge_floor": {
            "identity": "partial_(E\\{e}) P = 1+w_e for every deletion edge e",
            "component_consequence": "w_e>-1 for all eight edges by derivative-component nesting",
            "q_fibre_consequence": "b+1>0; the b=-1 resultant stratum is disjoint from C_P",
        },
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
