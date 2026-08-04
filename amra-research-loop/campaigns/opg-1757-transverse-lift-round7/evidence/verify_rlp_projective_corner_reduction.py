#!/usr/bin/env python3
"""Exact projective/Newton reduction for the open q3:RLP chamber.

This verifier deliberately stops short of a chamber certificate.  It proves
the exact asymptotic faces, the three projective-chart Newton principals, two
small-direction square faces, and a tridiagonal quartic Gram reduction for
the hardest small-direction blow-up.  All arithmetic is rational and only
Python's standard library is used.
"""

from __future__ import annotations

from fractions import Fraction
from math import comb
import json

from verify_mixed_three_negative import divide_polynomial
from verify_negative_c_direct_chambers import (
    add,
    constant,
    multiply,
    power,
    variable,
)
from verify_negative_nonshared_same_side_gram import (
    cleared_polynomial,
    positive_route_data,
)
from verify_negative_page_direct_chambers import digest
from verify_negative_q0_no_positive_gram import (
    build_delta,
    coefficient,
    common_monomial,
    divide_monomial,
    gram,
)


ROUTES = (0, 1, 5)
ACTIVE = (0, 1, 2, 5, 6, 7)
ROUTE_DEGREE_MIN = 7
ROUTE_DEGREE_MAX = 14


def scale(poly, scalar):
    scalar = Fraction(scalar)
    return {
        monomial: scalar * value
        for monomial, value in poly.items()
        if scalar * value
    }


def product(*polynomials):
    result = constant(1)
    for polynomial in polynomials:
        result = multiply(result, polynomial)
    return result


def polynomial_sum(*polynomials):
    result = constant(0)
    for polynomial in polynomials:
        result = add(result, polynomial)
    return result


def square(polynomial):
    return multiply(polynomial, polynomial)


def row(poly):
    return {
        "terms": len(poly),
        "negative_coefficients": sum(value < 0 for value in poly.values()),
        "degrees": [
            max(monomial[slot] for monomial in poly)
            for slot in range(8)
        ],
        "sha256": digest(poly),
    }


def rlp_manifest_factor():
    c, s3, q4, s4 = (variable(slot) for slot in (0, 4, 5, 6))
    return product(
        c,
        add(constant(1), s3, -1),
        q4,
        add(constant(1), multiply(q4, s4)),
    )


def reconstruct_h1884():
    delta, forest_count, connected_count = build_delta()
    cleared = cleared_polynomial(delta, "RLP", 1)
    manifest = rlp_manifest_factor()
    core = divide_polynomial(cleared, manifest)
    assert cleared == multiply(manifest, core)

    determinant = gram(core, 4)[3]
    common = common_monomial(determinant)
    residual = divide_monomial(determinant, common)
    q0, s0 = variable(1), variable(2)
    determinant_sum = positive_route_data(1)[2]
    positive_factor = multiply(power(add(q0, s0), 2), determinant_sum)
    h1884 = divide_polynomial(residual, positive_factor)
    assert residual == multiply(positive_factor, h1884)

    assert len(cleared) == 2098
    assert len(core) == 786
    assert len(determinant) == 5802
    assert common == (1, 0, 2, 0, 0, 1, 0, 0)
    assert len(h1884) == 1884
    assert digest(h1884) == (
        "f680804eafab4019dfb825d87d6d8734e3a515348bbe9d1dce36da8a9c2b45d5"
    )
    return h1884, {
        "deletion_forests": forest_count,
        "endpoint_connected_forests": connected_count,
        "Delta_b_original_terms": len(delta),
        "cleared_terms": len(cleared),
        "cleared_sha256": digest(cleared),
        "core_terms": len(core),
        "core_sha256": digest(core),
        "outer_gram_determinant_terms": len(determinant),
        "outer_gram_common_monomial": list(common),
        "H1884": row(h1884),
    }


def route_face(poly, degree):
    return {
        monomial: value
        for monomial, value in poly.items()
        if sum(monomial[slot] for slot in ROUTES) == degree
    }


def route_boundary_record(h1884):
    c, q0, s0, q4, s4, tau = (
        variable(slot) for slot in (0, 1, 2, 5, 6, 7)
    )
    one = constant(1)
    route_degrees = [
        sum(monomial[slot] for slot in ROUTES) for monomial in h1884
    ]
    assert min(route_degrees) == ROUTE_DEGREE_MIN
    assert max(route_degrees) == ROUTE_DEGREE_MAX

    negative_kernel = polynomial_sum(
        product(c, q0, tau),
        scale(multiply(c, q0), -1),
        scale(multiply(c, q4), -1),
        product(q0, q4, tau),
        scale(multiply(q0, q4), -1),
    )
    lowest = scale(
        product(power(s0, 4), add(c, q4), power(negative_kernel, 3)),
        -1,
    )
    assert route_face(h1884, ROUTE_DEGREE_MIN) == lowest

    shape = add(add(s0, s4), one, -1)
    highest_bracket = add(
        multiply(c, square(shape)),
        product(q4, power(s0, 2), power(s4, 2)),
    )
    highest = product(
        power(c, 3),
        power(q0, 5),
        power(q4, 5),
        power(s4, 2),
        power(add(one, tau, -1), 3),
        highest_bracket,
    )
    assert route_face(h1884, ROUTE_DEGREE_MAX) == highest
    return {
        "route_degree_range": [ROUTE_DEGREE_MIN, ROUTE_DEGREE_MAX],
        "lowest_face_terms": len(lowest),
        "lowest_face": "s0^4*(c+q4)*(c*q0*(1-tau)+c*q4+q0*q4*(1-tau))^3",
        "lowest_face_sha256": digest(lowest),
        "highest_face_terms": len(highest),
        "highest_face": "c^3*q0^5*q4^5*s4^2*(1-tau)^3*(c*(s0+s4-1)^2+q4*s0^2*s4^2)",
        "highest_face_sha256": digest(highest),
    }


def projective_chart(poly, maximum_slot):
    assert maximum_slot in ROUTES
    ratio_routes = tuple(slot for slot in ROUTES if slot != maximum_slot)
    result = {}
    for monomial, value in poly.items():
        route_degree = sum(monomial[slot] for slot in ROUTES)
        assert ROUTE_DEGREE_MIN <= route_degree <= ROUTE_DEGREE_MAX
        projected = [0] * 8
        projected[0] = route_degree - ROUTE_DEGREE_MIN
        projected[1] = monomial[ratio_routes[0]]
        projected[5] = monomial[ratio_routes[1]]
        projected[2] = monomial[2]
        projected[6] = monomial[6]
        projected[7] = monomial[7]
        key = tuple(projected)
        result[key] = result.get(key, Fraction()) + value
    return {monomial: value for monomial, value in result.items() if value}


def compactify_scale(poly):
    u = variable(0)
    one_minus_u = add(constant(1), u, -1)
    result = constant(0)
    for monomial, value in poly.items():
        exponent = monomial[0]
        reduced = list(monomial)
        reduced[0] = 0
        term = {tuple(reduced): value}
        term = product(term, power(u, exponent), power(one_minus_u, 7 - exponent))
        result = add(result, term)
    return result


def reverse_slot(poly, slot):
    result = {}
    for monomial, value in poly.items():
        exponent = monomial[slot]
        for degree in range(exponent + 1):
            transformed = list(monomial)
            transformed[slot] = degree
            key = tuple(transformed)
            result[key] = result.get(key, Fraction()) + (
                value * (-1 if degree % 2 else 1) * comb(exponent, degree)
            )
    return {monomial: value for monomial, value in result.items() if value}


def local_corner(poly, maximum_slot):
    result = compactify_scale(projective_chart(poly, maximum_slot))
    # x=1-u, a=1-A, z=1-s0, b=1-B, t=1-tau; v=s4.
    for slot in (0, 1, 2, 5, 7):
        result = reverse_slot(result, slot)
    return result


def pareto_support(poly):
    support = set(poly)
    return {
        monomial
        for monomial in support
        if not any(
            other != monomial
            and all(other[slot] <= monomial[slot] for slot in ACTIVE)
            for other in support
        )
    }


def local_principal(name):
    one = constant(1)
    x, a, z, b, v, t = (
        variable(slot) for slot in (0, 1, 2, 5, 6, 7)
    )
    A = add(one, a, -1)
    B = add(one, b, -1)
    direction_difference = add(v, z, -1)
    if name == "c":
        return product(
            power(A, 4),
            power(B, 3),
            polynomial_sum(
                multiply(add(one, B), power(x, 3)),
                product(
                    A,
                    t,
                    polynomial_sum(
                        square(add(x, product(B, v, t, direction_difference))),
                        multiply(B, square(add(x, product(B, power(v, 2), t)))),
                    ),
                ),
            ),
        )
    if name == "q0":
        return product(
            power(A, 3),
            power(B, 3),
            polynomial_sum(
                multiply(add(A, B), power(x, 3)),
                product(
                    t,
                    polynomial_sum(
                        multiply(B, square(add(x, product(B, power(v, 2), t)))),
                        multiply(
                            A,
                            square(add(x, product(B, v, t, direction_difference))),
                        ),
                    ),
                ),
            ),
        )
    assert name == "q4"
    return product(
        power(A, 3),
        power(B, 4),
        polynomial_sum(
            multiply(add(one, A), power(x, 3)),
            product(
                B,
                t,
                polynomial_sum(
                    square(add(x, product(power(v, 2), t))),
                    multiply(
                        A,
                        square(add(x, product(v, t, direction_difference))),
                    ),
                ),
            ),
        ),
    )


def local_total_degree(monomial):
    return sum(monomial[slot] for slot in ACTIVE)


def equal_direction_record(h1884):
    records = {}
    expected_terms = {"c": 235, "q0": 196, "q4": 205}
    for maximum_slot, name in ((0, "c"), (1, "q0"), (5, "q4")):
        chart = projective_chart(h1884, maximum_slot)
        compact = compactify_scale(chart)
        local = local_corner(h1884, maximum_slot)
        principal = local_principal(name)
        assert len(principal) == expected_terms[name]
        assert pareto_support(local) == pareto_support(principal)
        assert len(pareto_support(local)) == 7
        assert all(local[monomial] == principal[monomial]
                   for monomial in pareto_support(local))
        remainder = add(local, principal, -1)
        assert min(map(local_total_degree, remainder)) == 4
        records[name] = {
            "chart_terms": len(chart),
            "chart_sha256": digest(chart),
            "compact_terms": len(compact),
            "compact_sha256": digest(compact),
            "local_terms": len(local),
            "local_sha256": digest(local),
            "principal_terms": len(principal),
            "principal_sha256": digest(principal),
            "pareto_terms": len(pareto_support(local)),
            "remainder_minimum_local_degree": 4,
        }
    return {
        "coordinates": "x=1-u, a=1-A, z=1-s0, b=1-B, v=s4, t=1-tau",
        "common_equal_direction_principal": "2*x^3+t*(x+v^2*t)^2+t*(x+v*t*(v-z))^2",
        "manifest_sign": "each chart principal is a sum of x^3 and two squares with nonnegative A,B,t coefficients",
        "charts": records,
        "scope": "the exact Newton/Pareto face is nonnegative; the local remainder starts at total degree four but is not discarded or declared nonnegative",
    }


def substitute_x_bvt(poly):
    result = {}
    for monomial, value in poly.items():
        exponent = monomial[0]
        transformed = list(monomial)
        transformed[5] += exponent
        transformed[6] += exponent
        transformed[7] += exponent
        key = tuple(transformed)
        result[key] = result.get(key, Fraction()) + value
    return {monomial: value for monomial, value in result.items() if value}


def small_direction_normalized(h1884, maximum_slot):
    small_b = reverse_slot(local_corner(h1884, maximum_slot), 5)
    blown_up = substitute_x_bvt(small_b)
    common = common_monomial(blown_up)
    assert common == (0, 0, 0, 0, 0, 5, 2, 3)
    return small_b, divide_monomial(blown_up, common)


def small_direction_faces(h1884):
    one = constant(1)
    x, a, z, B, v, t = (
        variable(slot) for slot in (0, 1, 2, 5, 6, 7)
    )
    A = add(one, a, -1)
    one_minus_z = add(one, z, -1)
    z_minus_v = add(z, v, -1)
    records = {}
    normalized = {}
    for maximum_slot, name in ((0, "c"), (1, "q0")):
        small_b, quotient = small_direction_normalized(h1884, maximum_slot)
        normalized[name] = quotient
        b_zero = coefficient(small_b, 5, 0)
        x_zero = coefficient(small_b, 0, 0)
        if name == "c":
            linear = polynomial_sum(multiply(x, a), scale(multiply(x, z), -1), A)
            expected_b_zero = product(
                power(A, 3), power(x, 5), power(t, 3),
                power(one_minus_z, 2), square(linear),
            )
            expected_x_zero = product(
                power(A, 5), power(B, 5), power(v, 2), power(t, 3),
                add(
                    square(z_minus_v),
                    product(B, power(v, 2), power(one_minus_z, 2)),
                ),
            )
            normalized_A_power = 5
        else:
            expected_b_zero = product(
                power(A, 4), power(x, 5), power(t, 3),
                power(one_minus_z, 2), square(add(one, multiply(x, z), -1)),
            )
            expected_x_zero = product(
                power(A, 3), power(B, 5), power(v, 2), power(t, 3),
                add(
                    multiply(A, square(z_minus_v)),
                    product(B, power(v, 2), power(one_minus_z, 2)),
                ),
            )
            normalized_A_power = 4
        assert b_zero == expected_b_zero
        assert x_zero == expected_x_zero

        f = polynomial_sum(
            product(power(t, 2), v, power(x, 2), z),
            scale(product(power(t, 2), v, power(x, 2)), -1),
            product(t, v, x, z),
            scale(product(t, v, x), -2),
            product(t, x, z),
            scale(product(power(v, 2), x), -1),
            scale(product(v, x), 2),
            scale(v, -1),
            scale(x, -1),
            z,
        )
        normalized_b_zero = coefficient(quotient, 5, 0)
        expected_normalized_b_zero = product(
            power(A, normalized_A_power),
            add(one, product(t, v, x)),
            square(f),
        )
        assert normalized_b_zero == expected_normalized_b_zero
        records[name] = {
            "small_B_face": row(b_zero),
            "x_zero_face": row(x_zero),
            "normalized_terms": len(quotient),
            "normalized_sha256": digest(quotient),
            "normalized_B_zero_face": row(normalized_b_zero),
        }
    return records, normalized["q0"]


def root_coordinates(poly):
    # Reuse slot two for w where w=D*z-N and z=(N+w)/D.
    one = constant(1)
    y, w, v, t = (variable(slot) for slot in (0, 2, 6, 7))
    D = product(add(one, multiply(t, y)), add(one, product(t, v, y)))
    N = polynomial_sum(
        product(power(t, 2), v, power(y, 2)),
        scale(product(t, v, y), 2),
        product(power(v, 2), y),
        scale(product(v, y), -2),
        v,
        y,
    )
    result = constant(0)
    assert max(monomial[2] for monomial in poly) == 4
    for degree in range(5):
        result = add(
            result,
            product(
                coefficient(poly, 2, degree),
                power(add(w, N), degree),
                power(D, 4 - degree),
            ),
        )
    return result


def f4_factor():
    rows = (
        (-1, (0, 0, 0, 1, 0)),
        (1, (0, 1, 0, 1, 0)),
        (-1, (1, 0, 0, 0, 2)),
        (-1, (1, 0, 0, 2, 1)),
        (1, (1, 0, 1, 2, 1)),
        (-1, (1, 0, 1, 2, 2)),
        (1, (1, 1, 0, 0, 2)),
        (1, (1, 1, 0, 2, 1)),
        (-1, (1, 1, 1, 2, 1)),
        (-1, (2, 0, 0, 1, 3)),
        (-1, (2, 0, 1, 1, 2)),
        (1, (2, 0, 1, 3, 2)),
        (1, (2, 0, 2, 3, 3)),
        (1, (2, 1, 0, 1, 3)),
        (1, (2, 1, 1, 1, 2)),
        (-1, (2, 1, 1, 1, 3)),
        (-1, (2, 1, 1, 3, 2)),
    )
    result = {}
    for value, exponents in rows:
        monomial = [0] * 8
        for slot, exponent in zip((0, 1, 5, 6, 7), exponents):
            monomial[slot] = exponent
        result[tuple(monomial)] = Fraction(value)
    return result


def q0_root_gram_record(q0_normalized):
    root_poly = root_coordinates(q0_normalized)
    assert len(root_poly) == 37709
    assert max(monomial[2] for monomial in root_poly) == 4
    rows = [coefficient(root_poly, 2, degree) for degree in range(5)]
    expected_counts = [16469, 11141, 6567, 2950, 582]
    assert [len(item) for item in rows] == expected_counts

    one = constant(1)
    y, a, B, v, t = (variable(slot) for slot in (0, 1, 5, 6, 7))
    A = add(one, a, -1)
    C1 = add(A, B)
    C2 = add(
        multiply(A, add(one, product(t, v, y))),
        product(B, v, y, add(A, multiply(a, t))),
    )
    F4 = f4_factor()
    assert len(C2) == 7 and len(F4) == 17
    assert digest(C2) == "e616137c2c997416c5fe94f63a7bfb500399926e0ed02a2ecba92f2839c89603"
    assert digest(F4) == "0230ad40c10c93a19d9ce10b0f21d09bdf4f666e4411fc4a7aa97600a2f7e961"

    r3_common = (1, 0, 0, 0, 0, 1, 1, 0)
    r3_reduced = divide_monomial(rows[3], r3_common)
    H = scale(
        divide_polynomial(divide_polynomial(r3_reduced, C2), F4),
        Fraction(-1, 2),
    )
    assert len(H) == 260
    assert digest(H) == "10bcc0d40facb5ce239debf9297088ccb5771aa993ef67bc189bc4abd273573e"
    assert rows[3] == scale(
        product({r3_common: Fraction(1)}, C2, F4, H), -2
    )
    assert rows[4] == product(
        {(2, 0, 0, 0, 0, 2, 2, 0): Fraction(1)},
        C1,
        C2,
        square(F4),
    )

    K24 = add(
        multiply(C1, rows[2]),
        product(C2, square(H)),
        -1,
    )
    assert len(K24) == 8599
    assert common_monomial(K24) == (0, 0, 0, 0, 0, 1, 0, 0)
    assert digest(K24) == "05aaa1919f1291802019d5a7e7894bbcf681c46d5c3a4ea024d1c277d326c9c5"
    K24_reduced = divide_monomial(K24, common_monomial(K24))
    assert digest(K24_reduced) == (
        "e851b946099e4d6314c5c7ecda93095343c9fa8f7af293dc6c6d8745de0c0af3"
    )
    return {
        "coordinate": "w=(1+t*y)*(1+t*v*y)*z-(t^2*v*y^2+2*t*v*y+v^2*y-2*v*y+v+y)",
        "clearing_factor": "((1+t*y)*(1+t*v*y))^4",
        "quartic_terms": len(root_poly),
        "quartic_sha256": digest(root_poly),
        "rows": [row(item) for item in rows],
        "tridiagonal_gram": "[[r0,r1/2,0],[r1/2,r2,r3/2],[0,r3/2,r4]]",
        "r3_factorization": "-2*y*B*v*C2*F4*H260",
        "r4_factorization": "y^2*B^2*v^2*C1*C2*F4^2",
        "C1": "1+B-a",
        "C2": "(1-a)*(1+t*v*y)+B*v*y*(1-a+a*t)",
        "F4": row(F4),
        "H260": row(H),
        "lower_gram_minor": "4*y^2*B^2*v^2*C2*F4^2*K24",
        "K24": row(K24),
        "K24_common_monomial": list(common_monomial(K24)),
        "K24_reduced": row(K24_reduced),
        "scope": "the factorization is exact; nonnegativity of K24/B and the other Gram principal minors remains open",
    }


def main():
    h1884, reconstruction = reconstruct_h1884()
    route_boundary = route_boundary_record(h1884)
    equal_direction = equal_direction_record(h1884)
    small_faces, q0_normalized = small_direction_faces(h1884)
    root_gram = q0_root_gram_record(q0_normalized)
    print(json.dumps({
        "schema": "amra.opg1757.round7.rlp-projective-corner-reduction.v1",
        "domain": "the still-open q3:RLP representative outer-Gram core H1884; all route scales are nonnegative and the bounded activity/tau parameters lie in their unit intervals",
        "reconstruction": reconstruction,
        "route_boundary_faces": route_boundary,
        "equal_direction_newton_reduction": equal_direction,
        "small_direction_square_faces": small_faces,
        "q0_chart_root_quartic_reduction": root_gram,
        "conclusion": "all scale-infinity boundary faces and the common projective Newton principal are manifestly nonnegative; the singular small-direction branch is reduced exactly to a quartic tridiagonal Gram problem with an 8599-term lower-minor core",
        "coverage_change": 0,
        "remaining_negative_page_chambers": 18,
        "scope": "this is a structural reduction, not a sign certificate for H1884 or q3:RLP; no activity chamber, the generic Delta_b sign, or OPG-1757 is claimed closed",
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
