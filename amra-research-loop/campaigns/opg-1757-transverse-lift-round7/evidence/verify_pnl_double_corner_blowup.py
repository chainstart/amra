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


def projective_chart(poly, maximum_slot):
    """Compact a positive route cone in one of its three maximum charts."""
    assert maximum_slot in ROUTES
    ratio_slots = tuple(slot for slot in ROUTES if slot != maximum_slot)
    result = {}
    for monomial, value in poly.items():
        route_degree = sum(monomial[slot] for slot in ROUTES)
        assert ROUTE_MIN <= route_degree <= ROUTE_MAX
        transformed = [0] * 8
        transformed[0] = route_degree - ROUTE_MIN
        transformed[1] = monomial[ratio_slots[0]]
        transformed[5] = monomial[ratio_slots[1]]
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


def projectivize_homogeneous(poly, slots, maximum_slot, degree):
    """Set the largest homogeneous coordinate to one in a compact chart."""
    assert maximum_slot in slots
    result = {}
    for monomial, value in poly.items():
        assert sum(monomial[slot] for slot in slots) == degree
        transformed = list(monomial)
        transformed[maximum_slot] = 0
        key = tuple(transformed)
        result[key] = result.get(key, Fraction()) + value
    return {monomial: value for monomial, value in result.items() if value}


def substitute_slot(poly, slot, numerator, denominator=None):
    """Substitute numerator/denominator and clear the maximal denominator."""
    degree = max(monomial[slot] for monomial in poly)
    denominator = constant(1) if denominator is None else denominator
    factors = [
        multiply(power(numerator, exponent), power(denominator, degree - exponent))
        for exponent in range(degree + 1)
    ]
    result = constant(0)
    for monomial, value in poly.items():
        exponent = monomial[slot]
        reduced = list(monomial)
        reduced[slot] = 0
        for factor_monomial, factor_value in factors[exponent].items():
            target = tuple(
                left + right for left, right in zip(reduced, factor_monomial)
            )
            result[target] = result.get(target, Fraction()) + value * factor_value
    return {monomial: value for monomial, value in result.items() if value}, degree


def rescale_slot(poly, slot, scalar):
    scalar = Fraction(scalar)
    return {
        monomial: value * scalar ** monomial[slot]
        for monomial, value in poly.items()
        if value * scalar ** monomial[slot]
    }


def radial_projective_chart(poly, radial_slots, maximum_slot, order):
    """Factor the common radial order in one maximum-direction chart."""
    assert maximum_slot in radial_slots
    result = {}
    for monomial, value in poly.items():
        radial_degree = sum(monomial[slot] for slot in radial_slots)
        assert radial_degree >= order
        transformed = list(monomial)
        transformed[maximum_slot] = radial_degree - order
        key = tuple(transformed)
        result[key] = result.get(key, Fraction()) + value
    return {monomial: value for monomial, value in result.items() if value}


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
    c_projective = compactify_scale(projective_chart(x_chart, 0))
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

    # In the q0-maximal chart the observed zero stratum is
    # x=q4/q0=1-y=1-z=0.  Its equal-weight principal is a quadratic in t.
    q0_projective = compactify_scale(projective_chart(x_chart, 1))
    q0_boundary = q0_projective
    for slot in (4, 6):
        q0_boundary = reverse_slot(q0_boundary, slot)
    q0_boundary_slots = (2, 4, 5, 6)
    assert min(
        sum(monomial[slot] for slot in q0_boundary_slots)
        for monomial in q0_boundary
    ) == 3
    q0_mixed_face = {
        monomial: value
        for monomial, value in q0_boundary.items()
        if sum(monomial[slot] for slot in q0_boundary_slots) == 3
    }

    u, A, x, B, e, t = (
        variable(slot) for slot in (0, 1, 2, 5, 6, 7)
    )
    one_minus_u = add(one, u, -1)
    root_linear = polynomial_sum(
        scale(product(B, u), -1), product(e, u), scale(e, -1)
    )
    root_middle = polynomial_sum(
        scale(product(square(B), u), -2),
        scale(product(B, e, u), 2),
        scale(product(B, e), -2),
        product(B, square(u), x),
        scale(product(B, u, x), -1),
        product(e, square(u), x),
        scale(product(e, u, x), -2),
        product(e, x),
    )
    q0_t0 = product(B, u, square(root_linear))
    q0_t1 = scale(product(u, root_linear, root_middle), -1)
    q0_t2 = product(
        B,
        square(
            polynomial_sum(
                root_linear,
                product(square(u), x),
                scale(product(u, x), -1),
            )
        ),
    )
    q0_kernel = polynomial_sum(q0_t0, multiply(t, q0_t1), product(square(t), q0_t2))
    assert q0_mixed_face == product(
        power(A, 4), one_minus_u, q0_kernel
    )

    q0_b0 = q0_t0
    q0_b1 = add(q0_t0, scale(q0_t1, Fraction(1, 2)))
    q0_b2 = polynomial_sum(q0_t0, q0_t1, q0_t2)
    positive_root = polynomial_sum(product(B, u), product(one_minus_u, e))
    assert q0_b1 == scale(
        product(
            one_minus_u,
            x,
            u,
            positive_root,
            polynomial_sum(product(one_minus_u, e), scale(product(B, u), -1)),
        ),
        Fraction(1, 2),
    )

    q0_b2_a = reverse_slot(q0_b2, 0)
    q0_b2_charts = {}
    for maximum_slot in (2, 5, 6):
        ratio_slots = tuple(slot for slot in (2, 5, 6) if slot != maximum_slot)
        chart = projectivize_homogeneous(
            q0_b2_a, (2, 5, 6), maximum_slot, 3
        )
        controls = bernstein_transform(chart, [0, *ratio_slots])
        assert all(value >= 0 for value in controls.values())
        q0_b2_charts[str(maximum_slot)] = {
            "controls_nonzero": len(controls),
            "minimum_nonzero": str(min(controls.values())),
        }

    q0_determinant = add(
        multiply(q0_b0, q0_b2), multiply(q0_b1, q0_b1), -1
    )
    q0_determinant_a = reverse_slot(q0_determinant, 0)
    a = variable(0)
    one_minus_a = add(one, a, -1)
    conditional_y = variable(4)

    # Negative q0_b1 means a*e < B*(1-a).  Put
    # e=B*(1-a)*conditional_y/a, 0<=conditional_y<=1, then split x/B.
    q0_det_B, denominator_degree_B = substitute_slot(
        q0_determinant_a,
        6,
        product(B, one_minus_a, conditional_y),
        a,
    )
    assert denominator_degree_B == 4
    q0_det_B, _ = substitute_slot(q0_det_B, 2, product(B, x))
    assert common_monomial(q0_det_B) == (5, 0, 0, 0, 0, 6, 0, 0)
    q0_det_B = divide_monomial(
        q0_det_B, (5, 0, 0, 0, 0, 6, 0, 0)
    )
    q = variable(2)
    one_minus_y = add(one, conditional_y, -1)
    one_plus_y = add(one, conditional_y)
    J_B = polynomial_sum(
        product(square(a), square(q), square(one_minus_y)),
        product(a, square(q), add(constant(4), square(one_minus_y), -1)),
        scale(product(a, q, add(one, square(conditional_y), -1)), 4),
        scale(product(add(one, q), square(one_plus_y)), 4),
    )
    assert q0_det_B == scale(
        product(power(one_minus_a, 5), square(one_plus_y), J_B),
        Fraction(1, 4),
    )

    q0_det_x, denominator_degree_x = substitute_slot(
        q0_determinant_a,
        6,
        product(B, one_minus_a, conditional_y),
        a,
    )
    assert denominator_degree_x == 4
    q0_det_x, _ = substitute_slot(q0_det_x, 5, product(x, B))
    assert common_monomial(q0_det_x) == (5, 0, 6, 0, 0, 4, 0, 0)
    q0_det_x = divide_monomial(
        q0_det_x, (5, 0, 6, 0, 0, 4, 0, 0)
    )
    q = variable(5)
    J_x = polynomial_sum(
        product(square(a), square(one_minus_y)),
        product(a, add(constant(4), square(one_minus_y), -1)),
        scale(product(a, q, add(one, square(conditional_y), -1)), 4),
        scale(product(q, add(one, q), square(one_plus_y)), 4),
    )
    assert q0_det_x == scale(
        product(power(one_minus_a, 5), square(one_plus_y), J_x),
        Fraction(1, 4),
    )

    # In the q4-maximal chart the infinity/c corner has a binary quadratic
    # principal in a=1-scale and A=c/q4.
    q4_projective = compactify_scale(projective_chart(x_chart, 5))
    q4_boundary = reverse_slot(q4_projective, 0)
    assert min(monomial[0] + monomial[1] for monomial in q4_boundary) == 3
    q4_mixed_face = {
        monomial: value
        for monomial, value in q4_boundary.items()
        if monomial[0] + monomial[1] == 3
    }
    a, A, x, y, route_ratio, t = (
        variable(slot) for slot in (0, 1, 2, 4, 5, 7)
    )
    one_minus_xy = add(one, multiply(x, y), -1)
    q4_A2 = Px
    K = polynomial_sum(
        scale(product(t, square(x), square(y)), 2),
        scale(product(t, y), -2),
        scale(product(square(x), square(y)), -1),
        scale(y, 2),
        scale(one, -1),
    )
    q4_cross = scale(product(t, x, K), -1)
    q4_a2 = product(square(t), square(x), y)
    q4_kernel = polynomial_sum(
        product(square(A), q4_A2),
        product(A, a, q4_cross),
        product(square(a), q4_a2),
    )
    assert q4_mixed_face == product(
        power(route_ratio, 4),
        y,
        square(add(one, x, -1)),
        polynomial_sum(a, multiply(A, one_minus_xy)),
        q4_kernel,
    )
    q4_J = polynomial_sum(
        scale(product(square(t), square(x), square(y)), -4),
        scale(product(t, square(x), square(y)), 4),
        scale(product(t, x, y), 4),
        scale(product(t, y), -4),
        scale(product(square(x), square(y)), -1),
        scale(product(x, y), -2),
        scale(y, 4),
        scale(one, -1),
    )
    q4_determinant = add(
        scale(multiply(q4_A2, q4_a2), 4), square(q4_cross), -1
    )
    assert q4_determinant == product(
        square(t), square(x), square(one_minus_xy), q4_J
    )
    q4_conditional_residual = add(q4_J, K, -1)
    q4_conditional_bernstein = bernstein_transform(
        q4_conditional_residual, [2, 4, 7]
    )
    assert all(value >= 0 for value in q4_conditional_bernstein.values())

    # All three h-dominant projective charts accumulate at the same all-one
    # boundary.  Their common principal is a moving square, so introduce its
    # exact root coordinate and split the admissible root interval by sign.
    h_deviation_slots = (0, 1, 4, 5, 6, 7)
    h_projective_rows = {}
    h_common_faces = []
    h_boundaries = {}
    for maximum_slot, name in ((0, "c"), (1, "q0"), (5, "q4")):
        chart = compactify_scale(projective_chart(h_chart, maximum_slot))
        for slot in h_deviation_slots:
            chart = reverse_slot(chart, slot)
        minimum_degree = min(
            sum(monomial[slot] for slot in h_deviation_slots)
            for monomial in chart
        )
        assert minimum_degree == 3
        face = {
            monomial: value
            for monomial, value in chart.items()
            if sum(monomial[slot] for slot in h_deviation_slots) == 3
        }
        h_projective_rows[name] = row(chart)
        h_common_faces.append(face)
        h_boundaries[name] = chart
    assert h_common_faces[0] == h_common_faces[1] == h_common_faces[2]
    h_common_face = h_common_faces[0]

    a, root_ratio, H, s = (variable(slot) for slot in (0, 2, 4, 7))
    L = polynomial_sum(H, scale(a, 3))
    root_denominator = add(L, s)
    moving_root = add(multiply(root_ratio, root_denominator), s, -1)
    expected_h_common_face = product(
        constant(3),
        L,
        square(add(one, root_ratio, -1)),
        square(moving_root),
    )
    assert h_common_face == expected_h_common_face

    # w=root_denominator*y-s lies in [-s,L].  For w>=0 write w=L*z;
    # for w<=0 write w=-s*z.  These substitutions map both pieces to z in
    # [0,1] and keep the radial Newton grading exact.
    positive_root_numerator = add(s, multiply(L, root_ratio))
    negative_root_numerator = multiply(s, add(one, root_ratio, -1))
    h_root_positive, positive_degree = substitute_slot(
        h_boundaries["c"], 2, positive_root_numerator, root_denominator
    )
    h_root_negative, negative_degree = substitute_slot(
        h_boundaries["c"], 2, negative_root_numerator, root_denominator
    )
    assert positive_degree == negative_degree == 4
    positive_minimum = min(
        sum(monomial[slot] for slot in h_deviation_slots)
        for monomial in h_root_positive
    )
    negative_minimum = min(
        sum(monomial[slot] for slot in h_deviation_slots)
        for monomial in h_root_negative
    )
    assert positive_minimum == negative_minimum == 7
    h_positive_face = {
        monomial: value
        for monomial, value in h_root_positive.items()
        if sum(monomial[slot] for slot in h_deviation_slots) == 7
    }
    h_negative_face = {
        monomial: value
        for monomial, value in h_root_negative.items()
        if sum(monomial[slot] for slot in h_deviation_slots) == 7
    }
    expected_h_positive_face = product(
        constant(3),
        power(L, 5),
        square(root_ratio),
        square(add(one, root_ratio, -1)),
        square(root_denominator),
    )
    expected_h_negative_face = product(
        constant(3),
        L,
        square(add(L, multiply(s, root_ratio))),
        square(s),
        square(root_ratio),
        square(root_denominator),
    )
    assert h_positive_face == expected_h_positive_face
    assert h_negative_face == expected_h_negative_face

    h_negative_closed_charts = {}
    for maximum_slot, name in ((4, "H"), (7, "s")):
        radial = radial_projective_chart(
            h_root_negative, h_deviation_slots, maximum_slot, 7
        )
        control_slots = [
            maximum_slot,
            2,
            *(
                slot
                for slot in h_deviation_slots
                if slot != maximum_slot
            ),
        ]
        controls = bernstein_transform(radial, control_slots)
        assert all(value > 0 for value in controls.values())
        h_negative_closed_charts[name] = {
            "radial_polynomial": row(radial),
            "control_slots": control_slots,
            "bernstein_nonzero": len(controls),
            "bernstein_minimum": str(min(controls.values())),
            "bernstein_sha256": digest(controls),
        }

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
    assert len(q0_mixed_face) == 46
    assert digest(q0_mixed_face) == (
        "90b617e606b1d323f1a621879af390196cb542937f4bb4cf1763a461d0395ed5"
    )
    assert len(q4_mixed_face) == 86
    assert digest(q4_mixed_face) == (
        "0ee49446a7ff4500b68c96b7e12c4a6f5caece17f7cc9b2d4f4f9a7797217bad"
    )
    assert [h_projective_rows[name]["terms"] for name in ("c", "q0", "q4")] == [
        22786, 21692, 20982
    ]
    assert [h_projective_rows[name]["sha256"] for name in ("c", "q0", "q4")] == [
        "d2affe6d31e5d97c7700f2b7c8f3e3692f17a86499b4efeb4e9adc4773aaf5d2",
        "34c5c2e9b7bf4527ce7d6bc97945d2c330c326bc6b1454b79bfa10f55efd29e1",
        "0c64cc969560e2d52acd4ffb5dd0582796fcf2afc576def7a5b7e79f3bbfef55",
    ]
    assert len(h_common_face) == 34
    assert digest(h_common_face) == (
        "d9977ef66ad7af78683ad9fe381e596525d593f72af3a618c9f3936cafb9a146"
    )
    assert (len(h_root_positive), len(h_root_negative)) == (86464, 59892)
    assert [digest(h_root_positive), digest(h_root_negative)] == [
        "09d8ca3826c7f94e59a50014055611fc3c537475d2b8ad323607c4432eff2539",
        "c8eb9954de0d5402b7942e9cc9bfdcb6e3942efddcc67674ae8d92866737d896",
    ]
    assert (len(h_positive_face), len(h_negative_face)) == (63, 36)
    assert [digest(h_positive_face), digest(h_negative_face)] == [
        "9f2c7a08f5d4a3c98c72f9481cb6eb4ce1a83f4f7c98076113ce049929308eb1",
        "da265dfd8f13e278358239cd778a82dbdf91d1c8c55eed6d7cb750647e54e388",
    ]
    assert [
        h_negative_closed_charts[name]["radial_polynomial"]["sha256"]
        for name in ("H", "s")
    ] == [
        "49ff9a52e41960a6d6d0e96cfab55c4af529548516813b82cf20d0cbb958a665",
        "941f1a4e7d665cbe3a40e466dc58b93dc758913e1becd666b21402d24c196404",
    ]
    assert [
        h_negative_closed_charts[name]["bernstein_nonzero"]
        for name in ("H", "s")
    ] == [427058, 540935]
    assert [
        h_negative_closed_charts[name]["bernstein_minimum"]
        for name in ("H", "s")
    ] == ["1/51710400", "1/25116480"]
    assert [
        h_negative_closed_charts[name]["bernstein_sha256"]
        for name in ("H", "s")
    ] == [
        "bc264f5b31e19203e154443d9dc6256cc681c3cf6f53856edbbee561d337a6ff",
        "82e2019058e14cc55fe49c97f6fefb56182df060be72ca2d11b44a88857033b5",
    ]

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
        "c_max_mixed_corner": {
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
        "q0_max_mixed_corner": {
            "coordinates": "q0-maximal projective chart; u=scale, A=c/q0, B=q4/q0, v=1-y, e=1-z",
            "compact_polynomial": row(q0_boundary),
            "weight": "equal weight on (x,v,B,e)",
            "leading_face": row(q0_mixed_face),
            "identity": "A^4*(1-u)*Q(t), with q0=B*u*L^2, q1=-u*L*M, q2=B*(L+u^2*x-u*x)^2 and L=-B*u+e*u-e",
            "endpoint_t1_projective_bernstein": q0_b2_charts,
            "conditional_sign": "the middle t-Bernstein row is a*x*u*(B*u+a*e)*(a*e-B*u)/2; when negative put a*e=B*u*y and split x/B.  In both maximum charts the determinant is a positive prefactor times a displayed sum J_B or J_x of nonnegative terms",
        },
        "q4_max_infinity_corner": {
            "coordinates": "q4-maximal projective chart; a=1-scale, A=c/q4, B=q0/q4",
            "compact_polynomial": row(q4_boundary),
            "weight": "equal weight on (a,A)",
            "leading_face": row(q4_mixed_face),
            "identity": "B^4*y*(1-x)^2*(a+A*(1-x*y))*(A^2*Px(t)-A*a*t*x*K+a^2*t^2*x^2*y)",
            "conditional_sign": "Px is the proved degree-12 quadratic; if -t*x*K is negative then K>0, while the binary determinant is t^2*x^2*(1-x*y)^2*J and J-K has nonnegative tridegree-(2,2,2) Bernstein controls",
            "J_minus_K_bernstein_total": 27,
            "J_minus_K_bernstein_nonzero": len(q4_conditional_bernstein),
            "J_minus_K_bernstein_minimum_including_implicit_zero": "0",
        },
        "h_dominant_common_root": {
            "coordinates": "in each dominant-route chart reverse scale, both route ratios, h, z, and t; retain y=x/h",
            "projective_charts": h_projective_rows,
            "leading_face": row(h_common_face),
            "leading_identity": "3*(H+3*a)*(1-y)^2*(y*(H+3*a+s)-s)^2",
            "root_coordinate": "w=y*(H+3*a+s)-s, with -s<=w<=H+3*a",
            "positive_root_branch": {
                "substitution": "w=(H+3*a)*z, 0<=z<=1",
                "polynomial": row(h_root_positive),
                "leading_face": row(h_positive_face),
                "leading_identity": "3*(H+3*a)^5*z^2*(1-z)^2*(H+3*a+s)^2",
            },
            "negative_root_branch": {
                "substitution": "w=-s*z, 0<=z<=1",
                "polynomial": row(h_root_negative),
                "leading_face": row(h_negative_face),
                "leading_identity": "3*(H+3*a)*(H+3*a+s*z)^2*s^2*z^2*(H+3*a+s)^2",
                "closed_radial_maximum_charts": h_negative_closed_charts,
            },
        },
        "conclusion": "the PNL all-bounded corner has an exact positive quadratic blow-up, both activity charts have nonnegative zero- and infinite-route-scale faces, the first observed mixed Newton face in each dominant-route x-chart is nonnegative, the common h-chart accumulation is resolved into two nonnegative root principals, and the H- and s-maximal radial charts of its negative-root branch are fully Bernstein-positive",
        "coverage_change": 0,
        "remaining_negative_page_chambers": 18,
        "scope": "route degrees 8 through 11, higher mixed/root Newton orders outside the two closed negative-root radial charts, and the remaining compact interiors are coupled; q3:PNL, its symmetry mate, the generic sign, and OPG-1757 are not claimed",
    }


def main():
    print(json.dumps(build_record(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
