#!/usr/bin/env python3
"""Exact double-corner and route-scale faces for the q3:PNL chamber."""

from __future__ import annotations

from fractions import Fraction
import json

from verify_mixed_three_negative import divide_polynomial
from verify_negative_c_direct_chambers import (
    add,
    bernstein_transform,
    constant,
    multiply,
    power,
    variable,
)
from verify_negative_nonshared_double_negative_gram import cleared_polynomial
from verify_negative_page_direct_chambers import digest
from verify_negative_q0_no_positive_gram import (
    build_delta,
    common_monomial,
    divide_monomial,
    scale,
)
from verify_opposite_nonshared_chambers import divide_one_minus_variable
from verify_rlp_projective_corner_reduction import (
    polynomial_sum,
    product,
    reverse_slot,
    square,
)


ROUTES = (0, 1, 5)
ROUTE_MIN = 7
ROUTE_MAX = 12


def activity_blowup(poly, chart):
    """Blow up the ideal (x,h)^2 in the x- or h-dominant chart."""
    assert chart in ("x", "h")
    result = {}
    for monomial, value in poly.items():
        x_degree, h_degree = monomial[2], monomial[4]
        assert x_degree + h_degree >= 2
        transformed = list(monomial)
        if chart == "x":
            # h=x*y; slot two remains x and slot four becomes y.
            transformed[2] = x_degree + h_degree - 2
            transformed[4] = h_degree
        else:
            # x=h*y; slot four remains h and slot two becomes y.
            transformed[4] = x_degree + h_degree - 2
            transformed[2] = x_degree
        key = tuple(transformed)
        result[key] = result.get(key, Fraction()) + value
    return {monomial: value for monomial, value in result.items() if value}


def route_face(poly, degree):
    return {
        monomial: value
        for monomial, value in poly.items()
        if sum(monomial[slot] for slot in ROUTES) == degree
    }


def projective_max_c(poly):
    """Use c as the largest route and retain q0/c,q4/c in slots 1,5."""
    result = {}
    for monomial, value in poly.items():
        route_degree = sum(monomial[slot] for slot in ROUTES)
        assert ROUTE_MIN <= route_degree <= ROUTE_MAX
        transformed = [0] * 8
        transformed[0] = route_degree - ROUTE_MIN
        transformed[1] = monomial[1]
        transformed[5] = monomial[5]
        for slot in (2, 4, 6, 7):
            transformed[slot] = monomial[slot]
        key = tuple(transformed)
        result[key] = result.get(key, Fraction()) + value
    return {monomial: value for monomial, value in result.items() if value}


def compactify_scale(poly):
    scale_variable = variable(0)
    scale_complement = add(constant(1), scale_variable, -1)
    result = constant(0)
    for monomial, value in poly.items():
        exponent = monomial[0]
        reduced = list(monomial)
        reduced[0] = 0
        term = {tuple(reduced): value}
        term = product(
            term,
            power(scale_variable, exponent),
            power(scale_complement, ROUTE_MAX - ROUTE_MIN - exponent),
        )
        result = add(result, term)
    return result


def rescale_slot(poly, slot, scalar):
    scalar = Fraction(scalar)
    return {
        monomial: value * scalar ** monomial[slot]
        for monomial, value in poly.items()
        if value * scalar ** monomial[slot]
    }


def bernstein_quadratic(b0, b1, b2, t):
    one_minus_t = add(constant(1), t, -1)
    return polynomial_sum(
        multiply(square(one_minus_t), b0),
        scale(product(t, one_minus_t, b1), 2),
        multiply(square(t), b2),
    )


def row(poly):
    return {
        "terms": len(poly),
        "degrees": [max(monomial[slot] for monomial in poly) for slot in range(8)],
        "negative_power_coefficients": sum(value < 0 for value in poly.values()),
        "sha256": digest(poly),
    }


def build_record():
    delta, forest_count, connected_count = build_delta()
    cleared = cleared_polynomial(delta, "PNL", 1)
    cleared_common = common_monomial(cleared)
    assert cleared_common == (2, 4, 0, 0, 0, 1, 0, 0)
    core = divide_monomial(cleared, cleared_common)
    quotient = divide_one_minus_variable(core, 6)
    assert core == multiply(
        quotient, add(constant(1), variable(6), -1)
    )

    local = quotient
    for slot in (2, 4, 6, 7):
        local = reverse_slot(local, slot)
    assert min(monomial[2] + monomial[4] for monomial in local) == 2

    c, q0, x, h, q4, z, t = (
        variable(slot) for slot in (0, 1, 2, 4, 5, 6, 7)
    )
    one = constant(1)
    route_pair_sum = polynomial_sum(
        multiply(c, q0), multiply(c, q4), multiply(q0, q4)
    )
    route_schur_sum = add(route_pair_sum, product(c, q0, q4))
    one_minus_t = add(one, t, -1)
    degree_two = {
        monomial: value
        for monomial, value in local.items()
        if monomial[2] + monomial[4] == 2
    }
    expected_degree_two = product(
        power(c, 2),
        q4,
        add(one, q0),
        power(add(add(one, q4), z, -1), 2),
        route_schur_sum,
        polynomial_sum(
            multiply(
                route_schur_sum,
                square(add(x, multiply(h, one_minus_t), -1)),
            ),
            product(
                power(q0, 2),
                add(c, q4),
                square(multiply(h, one_minus_t)),
            ),
        ),
    )
    assert degree_two == expected_degree_two

    x_chart = activity_blowup(local, "x")
    h_chart = activity_blowup(local, "h")
    assert {
        min(sum(monomial[slot] for slot in ROUTES) for monomial in chart)
        for chart in (x_chart, h_chart)
    } == {7}
    assert {
        max(sum(monomial[slot] for slot in ROUTES) for monomial in chart)
        for chart in (x_chart, h_chart)
    } == {12}

    # In the x-dominant chart slot four is y=h/x.
    y = variable(4)
    one_minus_z = add(one, z, -1)
    Gx = polynomial_sum(
        product(t, x, y), scale(product(t, y), -1), y, scale(one, -1)
    )
    x_low = route_face(x_chart, 7)
    expected_x_low = product(
        power(c, 2), q4, square(one_minus_z),
        square(route_pair_sum), square(Gx)
    )
    assert x_low == expected_x_low

    one_minus_x = add(one, x, -1)
    one_minus_xy = add(one, multiply(x, y), -1)
    x_b0 = multiply(y, square(one_minus_x))
    x_b1 = scale(
        product(
            x,
            one_minus_xy,
            polynomial_sum(one, multiply(x, y), scale(y, -2)),
        ),
        Fraction(1, 2),
    )
    x_b2 = multiply(x, square(one_minus_xy))
    Px = bernstein_quadratic(x_b0, x_b1, x_b2, t)
    Fx = multiply(y, Px)
    x_kernel = polynomial_sum(
        product(q0, add(c, q4), Fx),
        product(c, q4, square(Gx)),
    )
    x_high = route_face(x_chart, 12)
    expected_x_high = product(
        power(c, 3), power(q0, 3), power(q4, 4),
        square(one_minus_x), one_minus_xy, x_kernel
    )
    assert x_high == expected_x_high
    x_determinant = add(
        multiply(x_b0, x_b2), multiply(x_b1, x_b1), -1
    )
    x_det_expected = scale(
        product(
            x,
            power(one_minus_xy, 3),
            polynomial_sum(
                multiply(y, square(add(constant(2), x, -1))), scale(x, -1)
            ),
        ),
        Fraction(1, 4),
    )
    assert x_determinant == x_det_expected

    # In the h-dominant chart slot two is y=x/h and slot four is h.
    y = variable(2)
    h = variable(4)
    Gh = polynomial_sum(product(h, t, y), scale(t, -1), scale(y, -1), one)
    h_low = route_face(h_chart, 7)
    expected_h_low = product(
        power(c, 2), q4, square(one_minus_z),
        square(route_pair_sum), square(Gh)
    )
    assert h_low == expected_h_low

    one_minus_h = add(one, h, -1)
    one_minus_hy = add(one, multiply(h, y), -1)
    h_b0 = square(one_minus_hy)
    h_b1 = scale(
        product(
            h,
            y,
            one_minus_h,
            polynomial_sum(constant(2), scale(y, -1), scale(multiply(h, y), -1)),
        ),
        Fraction(-1, 2),
    )
    h_b2 = product(h, square(y), square(one_minus_h))
    Fh = bernstein_quadratic(h_b0, h_b1, h_b2, t)
    h_kernel = polynomial_sum(
        product(q0, add(c, q4), Fh),
        product(c, q4, square(Gh)),
    )
    h_high = route_face(h_chart, 12)
    expected_h_high = product(
        power(c, 3), power(q0, 3), power(q4, 4),
        one_minus_h, square(one_minus_hy), h_kernel
    )
    assert h_high == expected_h_high
    h_determinant = add(
        multiply(h_b0, h_b2), multiply(h_b1, h_b1), -1
    )
    h_J = polynomial_sum(
        scale(multiply(h, y), -4),
        constant(4),
        scale(product(h, square(y), one_minus_h), -1),
    )
    h_det_expected = scale(
        product(h, square(y), power(one_minus_h, 3), h_J),
        Fraction(1, 4),
    )
    assert h_determinant == h_det_expected

    # The difficult projective boxes accumulate where the route scale tends to
    # infinity while q4/c, 1-y, and 1-z tend to zero.  Extract that Newton face
    # exactly in the c-maximal chart.
    c_projective = compactify_scale(projective_max_c(x_chart))
    boundary = c_projective
    for slot in (0, 4, 6):
        boundary = reverse_slot(boundary, slot)
    boundary_slots = (0, 4, 5, 6)
    assert min(
        sum(monomial[slot] for slot in boundary_slots)
        for monomial in boundary
    ) == 4
    mixed_face = {
        monomial: value
        for monomial, value in boundary.items()
        if sum(monomial[slot] for slot in boundary_slots) == 4
    }

    a, route_ratio, x, q4_ratio, t = (
        variable(slot) for slot in (0, 1, 2, 5, 7)
    )
    one_minus_x = add(one, x, -1)
    c_quadratic = polynomial_sum(
        product(add(one, scale(x, 2)), square(t)),
        scale(product(add(constant(2), x), t), -1),
        one,
    )
    mixed_cross = product(
        x,
        add(one, square(x), -1),
        t,
        add(scale(t, 2), one, -1),
    )
    mixed_kernel = polynomial_sum(
        product(square(a), square(t), square(x)),
        product(a, q4_ratio, mixed_cross),
        product(square(q4_ratio), square(one_minus_x), c_quadratic),
    )
    expected_mixed_face = product(
        q4_ratio,
        power(route_ratio, 4),
        square(one_minus_x),
        add(a, multiply(q4_ratio, one_minus_x)),
        mixed_kernel,
    )
    assert mixed_face == expected_mixed_face

    c_discriminant = add(
        square(add(constant(2), x)),
        add(one, scale(x, 2)),
        -4,
    )
    assert c_discriminant == product(x, add(x, constant(4), -1))

    alpha = product(square(t), square(x))
    gamma = product(square(one_minus_x), c_quadratic)
    mixed_determinant = add(
        scale(multiply(alpha, gamma), 4), square(mixed_cross), -1
    )
    J = polynomial_sum(
        constant(3),
        scale(square(x), -1),
        scale(x, -2),
        scale(t, -4),
        scale(product(t, x), 4),
        scale(product(t, square(x)), 4),
        scale(product(square(t), square(x)), -4),
    )
    assert mixed_determinant == product(
        square(t), square(x), square(one_minus_x), J
    )
    J_half = rescale_slot(J, 7, Fraction(1, 2))
    J_half_bernstein = bernstein_transform(J_half, [2, 7])
    assert all(value >= 0 for value in J_half_bernstein.values())

    assert (len(cleared), len(core), len(quotient), len(local)) == (
        4115, 4115, 2591, 2920
    )
    assert digest(local) == (
        "b3236cf596310d4a4151f7cfa161dad9868b467b241dc74bc5e437585833f71d"
    )
    assert digest(degree_two) == (
        "d917c349b0ed10971839fbad7ea99f4592bc473055311b62ef2dcd1f70aa634b"
    )
    assert [digest(x_chart), digest(h_chart)] == [
        "77274fc654cbea0d973f26343a3e4967ed3f45f500aa43a6ab5ff0e568eab975",
        "857eda8615d206b7e3f82bb0186c078715a6fcaa068d37ebd5c9cd5235c9b96d",
    ]
    assert [digest(x_low), digest(x_high), digest(h_low), digest(h_high)] == [
        "0b0f394ed31a793face75665648fc59b78a532a82e2f9c51f01302a97205e1ce",
        "8cc8bbbb5cfca96f2c8d88ee5cc88cf2401b42bf9bb5d7f2a01ac4424de8c430",
        "f801d08122209d086a5f179be9415079a981ca0b5c796469d693b08a74af6837",
        "8d97e408980ae93a1858bddf1fc2be1624280942f2c2d596a828a9f5cd57ba13",
    ]
    assert len(boundary) == 7874
    assert digest(boundary) == (
        "214c0915da3be323759fbeedf5001404c12bc077310dd3b4b62748dd5496c94d"
    )
    assert len(mixed_face) == 46
    assert digest(mixed_face) == (
        "6f3871a7ebff7d842d4979746b52d249a32e08b1adcf70c8c0befebee6902354"
    )

    return {
        "schema": "amra.opg1757.round7.pnl-double-corner-blowup.v1",
        "domain": "q3:PNL nested-odds chart with c,q0,q4>0 and all four bounded parameters in [0,1]",
        "reconstruction": {
            "deletion_forests": forest_count,
            "endpoint_connected_forests": connected_count,
            "Delta_b_original_terms": len(delta),
        },
        "cleared": row(cleared),
        "manifest_factor": "c^2*q0^4*q4*(1-s4)",
        "local_coordinates": "x=1-s0, h=1-s3, z=1-s4, t=1-tau",
        "local_quotient": row(local),
        "double_corner": {
            **row(degree_two),
            "vanishing_order": 2,
            "identity": "c^2*q4*(q0+1)*(q4+1-z)^2*B*(B*(x-h*(1-t))^2+q0^2*(c+q4)*h^2*(1-t)^2), B=c*q0*q4+c*q0+c*q4+q0*q4",
        },
        "activity_blowups": {
            "x_dominant": {
                "coordinate": "h=x*y, divide by x^2",
                "polynomial": row(x_chart),
                "route_degree_range": [7, 12],
                "degree_7_face": row(x_low),
                "degree_12_face": row(x_high),
                "degree_12_sign": "q0*(c+q4)*y*Px(t)+c*q4*Gx^2; if the middle Bernstein row of Px is negative then y*(2-x)>1 and its displayed determinant is nonnegative",
            },
            "h_dominant": {
                "coordinate": "x=h*y, divide by h^2",
                "polynomial": row(h_chart),
                "route_degree_range": [7, 12],
                "degree_7_face": row(h_low),
                "degree_12_face": row(h_high),
                "degree_12_sign": "q0*(c+q4)*Fh(t)+c*q4*Gh^2; the 2x2 Bernstein Gram determinant is h*y^2*(1-h)^3*J/4 with J=4*(1-h*y)-h*y^2*(1-h)>=3*(1-h)",
            },
        },
        "mixed_projective_corner": {
            "coordinates": "c-maximal projective chart; a=1-scale, b=q4/c, v=1-y, e=1-z",
            "compact_polynomial": row(boundary),
            "weight": "equal weight on (a,v,b,e)",
            "leading_face": row(mixed_face),
            "identity": "b*r^4*(1-x)^2*(a+b*(1-x))*H, H=a^2*t^2*x^2+a*b*x*(1-x^2)*t*(2*t-1)+b^2*(1-x)^2*C, C=(1+2*x)*t^2-(x+2)*t+1",
            "sign_certificate": "C has discriminant x*(x-4)<=0; for t>=1/2 every term of H is nonnegative, while for t<=1/2 the binary-quadratic determinant is t^2*x^2*(1-x)^2*J and J(x,s/2) has nonnegative bidegree-(2,2) Bernstein controls [[3,2,1],[2,3/2,1],[0,1,1]]",
            "J_half_bernstein_total": 9,
            "J_half_bernstein_nonzero": len(J_half_bernstein),
            "J_half_bernstein_minimum_including_implicit_zero": "0",
        },
        "conclusion": "the PNL all-bounded corner has an exact positive quadratic blow-up, both activity charts have nonnegative zero- and infinite-route-scale faces, and the first mixed infinity/q4 Newton face is nonnegative",
        "coverage_change": 0,
        "remaining_negative_page_chambers": 18,
        "scope": "route degrees 8 through 11, higher mixed Newton orders, and the compact interiors of both blow-up charts remain coupled; q3:PNL, its symmetry mate, the generic sign, and OPG-1757 are not claimed",
    }


def main():
    print(json.dumps(build_record(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
