#!/usr/bin/env python3
"""Exact route-matrix chamber and orientation ledger (stdlib only)."""

from __future__ import annotations

from hashlib import sha256
from itertools import combinations, permutations
import json

from verify_c_zero_fibre import (
    EDGES,
    add as add_original,
    derivative,
    multiply as multiply_original,
    reconstruct_original,
    restrict_original_zero,
)


B_EDGE = (0, 4)
ROUTE_NAMES = ("R0", "R3", "R4", "Rc")
NAMES = ROUTE_NAMES + ("h0", "h3", "h4")
COUNT = len(NAMES)
ZERO = (0,) * COUNT


def add(left, right, scale=1):
    result = dict(left)
    for monomial, coefficient in right.items():
        result[monomial] = result.get(monomial, 0) + scale * coefficient
    return {monomial: coefficient for monomial, coefficient in result.items() if coefficient}


def multiply(left, right):
    result = {}
    for left_monomial, left_coefficient in left.items():
        for right_monomial, right_coefficient in right.items():
            monomial = tuple(a + b for a, b in zip(left_monomial, right_monomial))
            result[monomial] = (
                result.get(monomial, 0) + left_coefficient * right_coefficient
            )
    return {monomial: coefficient for monomial, coefficient in result.items() if coefficient}


def scale(poly, scalar):
    return {monomial: scalar * coefficient for monomial, coefficient in poly.items() if scalar}


def constant(value):
    return {} if not value else {ZERO: value}


def variable(name, exponent=1):
    monomial = [0] * COUNT
    monomial[NAMES.index(name)] = exponent
    return {tuple(monomial): 1}


def power(poly, exponent):
    result = constant(1)
    for _ in range(exponent):
        result = multiply(result, poly)
    return result


def derivative_route(poly, slots):
    result = dict(poly)
    for slot in slots:
        differentiated = {}
        for monomial, coefficient in result.items():
            degree = monomial[slot]
            if degree <= 0:
                continue
            reduced = list(monomial)
            reduced[slot] -= 1
            differentiated[tuple(reduced)] = coefficient * degree
        result = differentiated
    return result


def substitute_original(poly, factors):
    result = {}
    for original_monomial, coefficient in poly.items():
        term = constant(coefficient)
        for edge, degree in zip(EDGES, original_monomial):
            if degree:
                term = multiply(term, power(factors[edge], degree))
        result = add(result, term)
    return result


def coefficient(poly, name, degree):
    slot = NAMES.index(name)
    result = {}
    for monomial, value in poly.items():
        if monomial[slot] != degree:
            continue
        reduced = list(monomial)
        reduced[slot] = 0
        result[tuple(reduced)] = value
    return result


def slice_with_degree(poly, name, degree):
    slot = NAMES.index(name)
    return {
        monomial: value
        for monomial, value in poly.items()
        if monomial[slot] == degree
    }


def quadratic_discriminant(poly, name):
    assert max(monomial[NAMES.index(name)] for monomial in poly) == 2
    a = coefficient(poly, name, 2)
    b = coefficient(poly, name, 1)
    c = coefficient(poly, name, 0)
    return add(multiply(b, b), scale(multiply(a, c), -4))


def determinant(matrix):
    size = len(matrix)
    result = {}
    for permutation in permutations(range(size)):
        inversions = sum(
            permutation[left] > permutation[right]
            for left in range(size)
            for right in range(left + 1, size)
        )
        term = constant(-1 if inversions % 2 else 1)
        for row, column in enumerate(permutation):
            term = multiply(term, matrix[row][column])
        result = add(result, term)
    return result


def principal_matrix(route_variables, subset):
    return [
        [route_variables[row] if row == column else constant(1) for column in subset]
        for row in subset
    ]


def canonical(poly):
    return json.dumps(
        [[list(monomial), coefficient] for monomial, coefficient in sorted(poly.items())],
        separators=(",", ":"),
    )


def digest(poly):
    return sha256(canonical(poly).encode()).hexdigest()


def term_count(poly):
    return len(poly)


def degrees(poly):
    return {
        name: max((monomial[index] for monomial in poly), default=-1)
        for index, name in enumerate(NAMES)
    }


def support_count(poly, names):
    slots = tuple(NAMES.index(name) for name in names)
    return len({tuple(monomial[slot] for slot in slots) for monomial in poly})


def main():
    deletion, connectivity, forest_count, connected_count = reconstruct_original()
    assert (forest_count, connected_count) == (128, 58)

    a_slope = derivative(deletion, (B_EDGE,))
    c_zero = restrict_original_zero(deletion, B_EDGE)
    d_slope = derivative(connectivity, (B_EDGE,))
    e_zero = restrict_original_zero(connectivity, B_EDGE)
    delta = add_original(
        multiply_original(a_slope, e_zero),
        multiply_original(d_slope, c_zero),
        -1,
    )

    route_variables = [variable(name) for name in ROUTE_NAMES]
    R0, R3, R4, Rc = route_variables
    h0, h3, h4 = (variable(name) for name in ("h0", "h3", "h4"))
    one = constant(1)

    factors = {
        (0, 1): add(h0, one, -1),
        (0, 2): add(multiply(R0, variable("h0", -1)), one, -1),
        B_EDGE: {},
        (1, 2): add(Rc, one, -1),
        (1, 3): add(h3, one, -1),
        (2, 3): add(multiply(R3, variable("h3", -1)), one, -1),
        (1, 4): add(h4, one, -1),
        (2, 4): add(multiply(R4, variable("h4", -1)), one, -1),
    }

    # The b-deletion polynomial loses all internal orientations and is the
    # determinant of the diagonal-plus-ones route matrix.
    route_a = substitute_original(a_slope, factors)
    route_matrix = [
        [route_variables[row] if row == column else one for column in range(4)]
        for row in range(4)
    ]
    determinant_a = determinant(route_matrix)
    assert route_a == determinant_a
    assert term_count(route_a) == 12

    # Every nonempty principal minor is the complementary route derivative
    # of det(K).  Hence the 1x1, 2x2, 3x3 and 4x4 minors reproduce precisely
    # the floor, cycle, first-derivative and A inequalities.
    principal_counts = {}
    for size in range(1, 5):
        principal_counts[str(size)] = 0
        for subset in combinations(range(4), size):
            minor = determinant(principal_matrix(route_variables, subset))
            complement = tuple(index for index in range(4) if index not in subset)
            assert minor == derivative_route(route_a, complement)
            principal_counts[str(size)] += 1
    assert principal_counts == {"1": 4, "2": 6, "3": 4, "4": 1}

    # Clear the positive orientation denominator from Delta_b.  The result has
    # only 45 orientation monomials (577 fully expanded route/orientation
    # monomials) and multidegree (4,2,2) in h0,h3,h4.
    route_delta = substitute_original(delta, factors)
    orientation_numerator = multiply(
        route_delta,
        multiply(power(h0, 2), multiply(h3, h4)),
    )
    assert all(all(exponent >= 0 for exponent in monomial) for monomial in orientation_numerator)
    assert term_count(orientation_numerator) == 577
    assert support_count(orientation_numerator, ("h0", "h3", "h4")) == 45
    assert tuple(degrees(orientation_numerator)[name] for name in ("h0", "h3", "h4")) == (
        4,
        2,
        2,
    )

    S4c = add(add(R4, Rc), constant(-2))
    S3c = add(add(R3, Rc), constant(-2))
    M4c = add(multiply(R4, Rc), constant(-1))
    M3c = add(multiply(R3, Rc), constant(-1))
    B0 = add(
        add(
            add(multiply(multiply(R3, R4), Rc), R3, -1),
            R4,
            -1,
        ),
        Rc,
        -1,
    )
    B0 = add(B0, constant(2))

    Q3_plus = add(
        add(multiply(M4c, power(h3, 2)), scale(multiply(S4c, h3), -2)),
        multiply(R3, S4c),
    )
    Q4_plus = add(
        add(multiply(M3c, power(h4, 2)), scale(multiply(S3c, h4), -2)),
        multiply(R4, S3c),
    )
    Q3_minus = add(
        add(multiply(S4c, power(h3, 2)), scale(multiply(S4c, h3), -2)),
        multiply(R3, M4c),
    )
    Q4_minus = add(
        add(multiply(S3c, power(h4, 2)), scale(multiply(S3c, h4), -2)),
        multiply(R4, M3c),
    )

    leading_slice = slice_with_degree(orientation_numerator, "h0", 4)
    trailing_slice = slice_with_degree(orientation_numerator, "h0", 0)
    assert leading_slice == multiply(power(h0, 4), multiply(Q3_plus, Q4_plus))
    assert trailing_slice == multiply(power(R0, 2), multiply(Q3_minus, Q4_minus))

    for quadratic, positive_sum in (
        (Q3_plus, S4c),
        (Q4_plus, S3c),
        (Q3_minus, S4c),
        (Q4_minus, S3c),
    ):
        assert quadratic_discriminant(
            quadratic,
            "h3" if degrees(quadratic)["h3"] == 2 else "h4",
        ) == scale(multiply(positive_sum, B0), -4)

    records = {
        "route_A": route_a,
        "orientation_N": orientation_numerator,
        "orientation_h0_leading": leading_slice,
        "orientation_h0_trailing": trailing_slice,
        "B0": B0,
    }
    print(json.dumps({
        "schema": "amra.opg1757.round7.route-matrix-chamber.v1",
        "reconstruction": {
            "deletion_forests": forest_count,
            "endpoint_connected_forests": connected_count,
        },
        "route_matrix": {
            "K": "diag(R0,R3,R4,Rc) with every off-diagonal entry 1",
            "A": "det(K)=R0*R3*R4*Rc-sum_(i<j)Ri*Rj+2*sum_i Ri-3",
            "principal_minor_counts": principal_counts,
            "component": "positive edge floors and K positive definite",
            "projected_component": "projection(C_P)=C_A, using derivative nesting for one inclusion and a large-b lift for the other",
        },
        "orientation": {
            "substitution": "y01=h0,y02=R0/h0; y13=h3,y23=R3/h3; y14=h4,y24=R4/h4; 1+c=Rc",
            "N": "h0^2*h3*h4*Delta_b",
            "expanded_terms": term_count(orientation_numerator),
            "orientation_support": support_count(
                orientation_numerator,
                ("h0", "h3", "h4"),
            ),
            "degrees": {name: degrees(orientation_numerator)[name] for name in ("h0", "h3", "h4")},
            "h0_outer_slices": "both products of two positive quadratics on K>0",
            "quadratic_discriminant": "-4*(positive 2x2 route sum)*(positive complementary 3x3 principal minor B0)",
        },
        "records": {
            name: {"terms": term_count(poly), "sha256": digest(poly)}
            for name, poly in records.items()
        },
        "scope": "exact projected chamber and orientation compression; middle h0 coefficients and generic Delta_b sign remain open",
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
