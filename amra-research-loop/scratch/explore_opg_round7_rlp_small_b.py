#!/usr/bin/env python3
"""Exact diagnostics for the small-direction projective RLP corner.

Starting from the local projective variables

    x=1-u, a=1-A, z=1-s0, b=1-B, v=s4, t=1-tau,

reverse ``b`` once more so slot five is the actual small direction ratio B.
On the subregion x <= B*v*t, put x=B*v*t*y and divide the exact common
factor B**5*v**2*t**3.  The resulting polynomial lives on a small rational
box and is suitable for exact Bernstein diagnostics.
"""

from __future__ import annotations

from fractions import Fraction
from pathlib import Path
import sys


ROOT = Path(__file__).parents[1]
EVIDENCE = ROOT / "campaigns" / "opg-1757-transverse-lift-round7" / "evidence"
sys.path[:0] = [str(EVIDENCE), str(Path(__file__).parent)]

from verify_negative_c_direct_chambers import (  # noqa: E402
    add,
    bernstein_transform,
    constant,
    multiply,
    power,
    variable,
)
from verify_negative_q0_no_positive_gram import (  # noqa: E402
    coefficient,
    common_monomial,
    divide_monomial,
)
from explore_opg_round7_rlp_tau import build  # noqa: E402
from search_opg_round7_rlp_projective_boxes import (  # noqa: E402
    local_corner,
    reverse_slot,
)


SLOTS = (0, 1, 2, 5, 6, 7)
WIDTHS = {
    0: Fraction(1),
    1: Fraction(1, 128),
    2: Fraction(1, 16),
    5: Fraction(1, 2),
    6: Fraction(1, 128),
    7: Fraction(1, 32),
}


def substitute_x_bvt(poly):
    """Substitute x=B*v*t*y, reusing slot zero for y."""
    result = {}
    for monomial, value in poly.items():
        exponent = monomial[0]
        transformed = list(monomial)
        transformed[5] += exponent
        transformed[6] += exponent
        transformed[7] += exponent
        key = tuple(transformed)
        result[key] = result.get(key, 0) + value
    return {monomial: value for monomial, value in result.items() if value}


def scale_slots(poly, widths):
    """Map the indicated rational box to a unit cube."""
    result = {}
    for monomial, value in poly.items():
        scale = value
        for slot, width in widths.items():
            scale *= width ** monomial[slot]
        if scale:
            result[monomial] = scale
    return result


def pareto_monomials(poly):
    """Return coordinatewise-minimal exponent tuples on the active slots."""
    support = {
        tuple(monomial[slot] for slot in SLOTS)
        for monomial, value in poly.items()
        if value
    }
    return sorted(
        exponent for exponent in support
        if not any(
            other != exponent
            and all(left <= right for left, right in zip(other, exponent))
            for other in support
        )
    )


def homogeneous(poly, degree, slots=SLOTS):
    return {
        monomial: value for monomial, value in poly.items()
        if sum(monomial[slot] for slot in slots) == degree
    }


def sympy_factor(poly):
    import sympy as sp

    symbols = sp.symbols("y a z B v t")
    expression = 0
    for monomial, value in poly.items():
        term = sp.Rational(value.numerator, value.denominator)
        for symbol, slot in zip(symbols, SLOTS):
            term *= symbol ** monomial[slot]
        expression += term
    return sp.factor(expression)


def normalized(maximum_slot):
    local = local_corner(build()[0], maximum_slot)
    small_b = reverse_slot(local, 5)
    blown_up = substitute_x_bvt(small_b)
    common = common_monomial(blown_up)
    assert common[5] == 5 and common[6] == 2 and common[7] == 3
    return small_b, divide_monomial(blown_up, common), common


def root_coordinates(poly):
    """Put w=D*z-N and return D**4*poly(z=(N+w)/D).

    The B=0 face is a positive multiplier times ``w**2``.  Slot two is
    reused for w.  The exact substitution is expanded sparsely, without any
    symbolic rational-function machinery.
    """
    y, z, v, t = (variable(slot) for slot in (0, 2, 6, 7))
    d = multiply(add(constant(1), multiply(t, y)),
                 add(constant(1), multiply(multiply(t, v), y)))
    n = add(
        multiply(multiply(power(t, 2), v), power(y, 2)),
        multiply(multiply(t, v), y),
        2,
    )
    n = add(n, multiply(power(v, 2), y))
    n = add(n, multiply(v, y), -2)
    n = add(n, v)
    n = add(n, y)
    w_plus_n = add(z, n)

    result = constant(0)
    for degree in range(5):
        row = coefficient(poly, 2, degree)
        if not row:
            continue
        result = add(
            result,
            multiply(
                row,
                multiply(power(w_plus_n, degree), power(d, 4 - degree)),
            ),
        )
    return result, d, n


def main():
    for maximum_slot, name in ((0, "c"), (1, "q0")):
        small_b, quotient, common = normalized(maximum_slot)
        print(name, "small_b_terms", len(small_b), "common", common,
              "quotient_terms", len(quotient))
        print(name, "pareto", pareto_monomials(quotient))
        minimum_degree = min(
            sum(monomial[slot] for slot in SLOTS) for monomial in quotient
        )
        for degree in range(minimum_degree, minimum_degree + 5):
            face = homogeneous(quotient, degree)
            if face:
                print(name, "degree", degree, "terms", len(face),
                      "factor", sympy_factor(face))

        unit = scale_slots(quotient, WIDTHS)
        bernstein = bernstein_transform(unit, list(SLOTS))
        negatives = [(monomial, value) for monomial, value in bernstein.items()
                     if value < 0]
        print(name, "bernstein_terms", len(bernstein),
              "negative", len(negatives),
              "minimum", min(bernstein.values()))
        print(name, "negative_examples", sorted(negatives, key=lambda item: item[1])[:10])


if __name__ == "__main__":
    main()
