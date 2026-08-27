#!/usr/bin/env python3
"""Discovery-only A2/H scan with both nonshared pages in negative charts."""

from __future__ import annotations

from fractions import Fraction
from pathlib import Path
import sys


SCRATCH = Path(__file__).parent
EVIDENCE = (
    Path(__file__).parents[1]
    / "campaigns"
    / "opg-1757-transverse-lift-round7"
    / "evidence"
)
sys.path[:0] = [str(SCRATCH), str(EVIDENCE)]

from explore_opg_round7_plr_quartic import (  # noqa: E402
    bernstein_entries,
    divide_monomial,
    divide_one_minus_variable,
)
from verify_c_zero_fibre import (  # noqa: E402
    EDGES,
    add as add_original,
    derivative,
    multiply as multiply_original,
    reconstruct_original,
    restrict_original_zero,
)
from verify_nonnegative_route_chambers import (  # noqa: E402
    B_EDGE,
    add,
    coefficient,
    constant,
    multiply,
    power,
    scale,
)
from verify_shared_page_discriminant import (  # noqa: E402
    C_EDGE,
    X01,
    X02,
    X13,
    X14,
    X23,
    X24,
    coefficient as original_coefficient,
    divide_monomial as original_divide_monomial,
)


# Local slots: (c,b=x02,q=q3,u,r=q4,s).
COUNT = 6
ZERO = (0,) * COUNT


def local_constant(value):
    value = Fraction(value)
    return {} if not value else {ZERO: value}


def local_variable(slot, scalar=1):
    monomial = [0] * COUNT
    monomial[slot] = 1
    return {tuple(monomial): Fraction(scalar)}


def local_power(poly, exponent):
    result = local_constant(1)
    for _ in range(exponent):
        result = local_multiply(result, poly)
    return result


def local_add(left, right, scalar=1):
    scalar = Fraction(scalar)
    result = dict(left)
    for monomial, value in right.items():
        result[monomial] = result.get(monomial, Fraction()) + scalar * value
    return {monomial: value for monomial, value in result.items() if value}


def local_multiply(left, right):
    result = {}
    for lm, lv in left.items():
        for rm, rv in right.items():
            monomial = tuple(a + b for a, b in zip(lm, rm))
            result[monomial] = result.get(monomial, Fraction()) + lv * rv
    return {monomial: value for monomial, value in result.items() if value}


def local_scale(poly, scalar):
    return {monomial: Fraction(scalar) * value for monomial, value in poly.items()}


def route_factors(side, q, t):
    negative = local_scale(t, -1)
    positive = local_add(q, t)
    denominator = local_add(local_constant(1), t, -1)
    return (negative, positive, denominator) if side == "L" else (positive, negative, denominator)


def substitute(poly, sides):
    c, b, q, u, r, s = (local_variable(slot) for slot in range(COUNT))
    result = {}
    page3 = route_factors(sides[0], q, u)
    page4 = route_factors(sides[1], r, s)
    for monomial, value in poly.items():
        assert monomial[EDGES.index(B_EDGE)] == 0
        assert monomial[EDGES.index(X01)] == 0
        term = local_constant(value)
        term = local_multiply(term, local_power(c, monomial[EDGES.index(C_EDGE)]))
        term = local_multiply(term, local_power(b, monomial[EDGES.index(X02)]))
        for edges, factors in (
            ((X13, X23), page3),
            ((X14, X24), page4),
        ):
            left_degree = monomial[EDGES.index(edges[0])]
            right_degree = monomial[EDGES.index(edges[1])]
            left, right, denominator = factors
            term = local_multiply(term, local_power(left, left_degree))
            term = local_multiply(term, local_power(right, right_degree))
            positive_degree = right_degree if factors is page3 and sides[0] == "L" else None
            if factors is page4:
                positive_degree = right_degree if sides[1] == "L" else left_degree
            elif sides[0] == "R":
                positive_degree = left_degree
            term = local_multiply(term, local_power(denominator, 2 - positive_degree))
        result = local_add(result, term)
    return result


def maximal_one_minus_power(poly, slot):
    quotient = poly
    power_count = 0
    while True:
        try:
            candidate = divide_one_minus_variable(quotient, slot)
        except AssertionError:
            return power_count, quotient
        quotient = candidate
        power_count += 1


def signs(poly):
    return len(poly), sum(value < 0 for value in poly.values())


def common_monomial(poly):
    count = len(next(iter(poly)))
    return tuple(min(monomial[slot] for monomial in poly) for slot in range(count))


def determinant(entries):
    return local_add(
        local_multiply(entries[0], entries[2]),
        local_multiply(entries[1], entries[1]),
        -1,
    )


def scan(poly, sides, label):
    cleared = substitute(poly, sides)
    u_power, quotient = maximal_one_minus_power(cleared, 3)
    s_power, quotient = maximal_one_minus_power(quotient, 5)
    result = {
        "label": label,
        "sides": sides,
        "cleared": signs(cleared),
        "factors": (u_power, s_power),
        "quotient": signs(quotient),
        "degrees": [max(m[slot] for m in quotient) for slot in range(COUNT)],
        "directions": [],
    }
    for slot, name in ((3, "u"), (5, "s")):
        degree = max(m[slot] for m in quotient)
        if degree != 2:
            continue
        entries = bernstein_entries(quotient, slot, 2)
        det = determinant(entries)
        common = common_monomial(det)
        residual = divide_monomial(det, common)
        subrows = []
        for vslot, vname in ((0, "c"), (1, "b"), (2, "q"), (4, "r")):
            vdegree = max(m[vslot] for m in residual)
            if vdegree != 2:
                continue
            coeffs = tuple(coefficient(residual, vslot, k) for k in range(3))
            disc = local_add(
                local_multiply(coeffs[1], coeffs[1]),
                local_multiply(coeffs[0], coeffs[2]),
                -4,
            )
            subrows.append((vname, [signs(x) for x in coeffs], signs(disc), common_monomial(disc)))
        result["directions"].append({
            "first": name,
            "entries": [signs(entry) for entry in entries],
            "det": signs(det),
            "common": common,
            "residual": signs(residual),
            "quadratics": subrows,
        })
    return result


def build_shared():
    deletion, connectivity, _, _ = reconstruct_original()
    a_slope = derivative(deletion, (B_EDGE,))
    c_zero = restrict_original_zero(deletion, B_EDGE)
    d_slope = derivative(connectivity, (B_EDGE,))
    e_zero = restrict_original_zero(connectivity, B_EDGE)
    delta = add_original(
        multiply_original(a_slope, e_zero),
        multiply_original(d_slope, c_zero),
        -1,
    )
    a2 = original_coefficient(delta, X01, 2)
    a1 = original_coefficient(delta, X01, 1)
    a0 = original_coefficient(delta, X01, 0)
    disc = add_original(multiply_original(a1, a1), multiply_original(a2, a0), -4)
    divided = original_divide_monomial(
        disc, {C_EDGE: 2, X02: 2, X13: 2, X14: 2}
    )
    H = {monomial: -value // 4 for monomial, value in divided.items()}
    return a2, H


def main():
    a2, H = build_shared()
    for sides in ("LL", "LR", "RR"):
        print(scan(a2, sides, "A2"))
        print(scan(H, sides, "H"))


if __name__ == "__main__":
    main()
