#!/usr/bin/env python3
"""Independent exact audit of rank seven and the seventh long band.

The author's ``verify_ordinary_rank_seven_and_seventh_band`` module is
not imported.  Fixed-depth values are regenerated from the audited
finite profile source, with a new exact Lagrange implementation.
"""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from functools import lru_cache

import sympy as sp

from independent_verify_all_fixed_rank_ordinary_symbol_algorithm import (
    D as PROFILE_D,
    exact_ordinary_value,
)
from independent_verify_ordinary_rank_six_symbol import (
    rank_six_polynomial,
)
from independent_verify_ordinary_sixth_long_recurrence_band import (
    printed_lower_rank_symbols,
)


# Deliberately use a different printed name and different assumptions
# from PROFILE_D.  Every imported polynomial function receives DEPTH
# explicitly.
DEPTH = sp.symbols("depth", integer=True)
PAGE = sp.symbols("page")
INDEX = sp.symbols("index", integer=True, nonnegative=True)
COUNT = sp.symbols("count", integer=True, nonnegative=True)
SHIFT = sp.symbols("shift", integer=True, nonnegative=True)

RANK_SEVEN_DENOMINATOR = sp.Integer(2189632665771048960000)
RANK_SEVEN_COEFFICIENTS = (
    30217328900,
    588271610850,
    13643387596300,
    -13878287091900,
    -206865593275440,
    -13510109661967215,
    72376793545393304,
    23072778779075520,
    639389903532886168,
    -17666060968351929996,
    84496255105723314960,
    489445758683198578404,
    -5864687888148553029676,
    15666213093792343586097,
    -42538398347646927587972,
    643254880572068718227472,
    -3764530202112123124432752,
    10480876675598477563463664,
    -26911510436413086105307392,
    76861878762263173992232704,
    -137796321367666244115302400,
    129244798226101901724057600,
)
SEVENTH_BAND_DENOMINATOR = sp.Integer(121646259209502720000)
SEVENTH_BAND_SHIFTED_COEFFICIENTS = (
    3271787244462017050,
    623648042617358143000,
    55856875934329452263050,
    3124374449017856908566000,
    122355759286004351589595575,
    3564341289917374275903469920,
    80099132802493969498884814000,
    1421058904493630987185394627680,
    20200960399253804993196252363940,
    232183805877904273159570354721976,
    2167537096961864786157429994245990,
    16446364861467480300030466642161360,
    101115582702312578695739865178530355,
    500203837038278678128508374054816528,
    1967490179042233169037740486691569800,
    6042615980557589009769445887708502560,
    14099566784784874077474835182924882480,
    23963972915208111433458538784014037376,
    27687602384655981572175962384529653760,
    19132079682860615978089318293170457600,
    5797589639494004327761299341549568000,
)
FIRST_SEVENTH_BAND_VALUE = sp.Rational(
    5764882926530737865899, 120960
)
EXPECTED_NEWTON_DENOMINATOR = (
    sp.Integer(162188424826230242096971776000000)
    * DEPTH**2
    * (DEPTH - 6)
    * (DEPTH - 5) ** 2
    * (DEPTH - 4) ** 2
    * (DEPTH - 3) ** 2
    * (DEPTH - 2) ** 2
    * (DEPTH - 1) ** 2
)


def descending_polynomial(coefficients, variable):
    degree = len(coefficients) - 1
    return sum(
        sp.Integer(coefficient) * variable ** (degree - position)
        for position, coefficient in enumerate(coefficients)
    )


def rank_seven_polynomial(variable=DEPTH):
    return -descending_polynomial(
        RANK_SEVEN_COEFFICIENTS, variable
    ) / RANK_SEVEN_DENOMINATOR


def exact_lagrange_polynomial(points, variable=PAGE):
    """Interpolate by the defining Lagrange products, exactly."""

    result = sp.Poly(0, variable, domain=sp.QQ)
    for abscissa, ordinate in points:
        basis = sp.Poly(1, variable, domain=sp.QQ)
        denominator = sp.Integer(1)
        for other_abscissa, _ in points:
            if other_abscissa == abscissa:
                continue
            basis *= sp.Poly(
                variable - other_abscissa, variable, domain=sp.QQ
            )
            denominator *= abscissa - other_abscissa
        result += basis.mul_ground(sp.Rational(ordinate) / denominator)
    return result


@lru_cache(maxsize=None)
def independently_generated_rank_seven_value(depth: int):
    """Regenerate beta_(depth,7) without exact_ordinary_polynomial."""

    if depth < 7:
        raise ValueError("rank seven requires depth >= 7")
    start = max(2, (depth + 5) // 2) + 1
    points = []
    for page_count in range(start, start + depth + 1):
        value: Fraction = exact_ordinary_value(page_count, depth)
        points.append(
            (
                page_count,
                sp.Rational(value.numerator, value.denominator),
            )
        )
    polynomial = exact_lagrange_polynomial(points, PAGE)
    assert polynomial.degree() == depth
    assert polynomial.LC() == 1

    # Two page-count holdouts certify the independently rebuilt
    # fixed-depth ordinary polynomial before extracting rank seven.
    for page_count in (start + depth + 1, start + depth + 2):
        source_value: Fraction = exact_ordinary_value(
            page_count, depth
        )
        expected = sp.Rational(
            source_value.numerator, source_value.denominator
        )
        assert polynomial.eval(page_count) == expected

    return polynomial.coeff_monomial(PAGE ** (depth - 7))


@lru_cache(maxsize=1)
def reconstruct_rank_seven():
    interpolation_depths = tuple(range(8, 30))
    holdout_depths = (7, 30, 31, 32)
    interpolation_points = tuple(
        (
            depth,
            independently_generated_rank_seven_value(depth),
        )
        for depth in interpolation_depths
    )
    interpolated = exact_lagrange_polynomial(
        interpolation_points, DEPTH
    )
    assert interpolated.degree() == 21
    for depth in holdout_depths:
        assert interpolated.eval(depth) == (
            independently_generated_rank_seven_value(depth)
        )
    return interpolated, interpolation_depths, holdout_depths


@lru_cache(maxsize=None)
def signed_stirling_rows(maximum_loss: int):
    """Construct s(n,n-r) by Newton identities and power sums."""

    elementary = [sp.Integer(1)]
    power_sums = {
        power: sp.expand(
            sp.summation(
                INDEX**power, (INDEX, 0, COUNT - 1)
            )
        )
        for power in range(1, maximum_loss + 1)
    }
    for loss in range(1, maximum_loss + 1):
        elementary.append(
            sp.factor(
                sp.cancel(
                    sum(
                        (-1) ** (power - 1)
                        * elementary[loss - power]
                        * power_sums[power]
                        for power in range(1, loss + 1)
                    )
                    / sp.Integer(loss)
                )
            )
        )
    signed = tuple(
        sp.factor((-1) ** loss * elementary[loss])
        for loss in range(maximum_loss + 1)
    )
    for loss in range(1, maximum_loss + 1):
        assert sp.expand(
            signed[loss].subs(COUNT, COUNT + 1)
            - signed[loss]
            + COUNT * signed[loss - 1]
        ) == 0
    return signed


def polynomial_binomial(top, bottom):
    return (
        sp.prod(top - offset for offset in range(bottom))
        / sp.factorial(bottom)
    )


@lru_cache(maxsize=1)
def derive_newton_and_long_recurrence():
    lower = printed_lower_rank_symbols(DEPTH)
    beta = lower + [
        rank_six_polynomial(DEPTH),
        rank_seven_polynomial(DEPTH),
    ]
    assert len(beta) == 8
    assert all(PROFILE_D not in value.free_symbols for value in beta)
    stirling = signed_stirling_rows(7)

    h_rows = [sp.Integer(1)]
    for loss in range(1, 8):
        ordinary_coefficient = sum(
            beta[rank]
            * polynomial_binomial(DEPTH - rank, loss - rank)
            * 2 ** (loss - rank)
            for rank in range(loss + 1)
        )
        correction = sum(
            h_rows[row]
            * stirling[loss - row].subs(COUNT, DEPTH - row)
            for row in range(loss)
        )
        h_rows.append(
            sp.factor(
                sp.cancel(
                    sp.expand(ordinary_coefficient - correction)
                )
            )
        )

    bands = []
    for band in range(7):
        value = (
            h_rows[band + 1]
            - h_rows[band + 1].subs(DEPTH, DEPTH + 1)
        )
        value -= sum(
            bands[lower_band]
            * h_rows[band - lower_band].subs(
                DEPTH, DEPTH - 1 - 2 * lower_band
            )
            for lower_band in range(band)
        )
        bands.append(
            sp.factor(sp.cancel(sp.expand(value)))
        )
    return tuple(h_rows), tuple(bands)


def positive_shift_coefficients(expression, shift):
    numerator = sp.cancel(expression).as_numer_denom()[0]
    polynomial = sp.Poly(
        sp.expand(numerator.subs(DEPTH, SHIFT + shift)), SHIFT
    )
    coefficients = tuple(int(value) for value in polynomial.all_coeffs())
    assert all(value > 0 for value in coefficients)
    return coefficients


def coefficient_hash(coefficients):
    payload = ",".join(str(value) for value in coefficients)
    return hashlib.sha256(payload.encode("ascii")).hexdigest()


@lru_cache(maxsize=1)
def audit():
    assert DEPTH != PROFILE_D
    assert DEPTH.name == "depth"
    assert PROFILE_D.name == "d"

    interpolated, interpolation_depths, holdout_depths = (
        reconstruct_rank_seven()
    )
    derived_beta7 = sp.cancel(interpolated.as_expr())
    printed_beta7 = sp.cancel(rank_seven_polynomial(DEPTH))
    assert sp.cancel(derived_beta7 - printed_beta7) == 0
    beta7_numerator, beta7_denominator = (
        printed_beta7.as_numer_denom()
    )
    assert beta7_denominator == RANK_SEVEN_DENOMINATOR
    assert sp.expand(-beta7_numerator) == descending_polynomial(
        RANK_SEVEN_COEFFICIENTS, DEPTH
    )

    p7_shift = positive_shift_coefficients(-printed_beta7, 7)
    assert len(p7_shift) == 22

    beta5 = printed_lower_rank_symbols(DEPTH)[5]
    beta6 = rank_six_polynomial(DEPTH)
    a5 = -beta5 / polynomial_binomial(DEPTH, 5)
    a6 = beta6 / polynomial_binomial(DEPTH, 6)
    a7 = -printed_beta7 / polynomial_binomial(DEPTH, 7)
    newton = sp.cancel(a6**2 - a5 * a7)
    newton_numerator, newton_denominator = newton.as_numer_denom()
    assert sp.factor(newton_denominator) == sp.factor(
        EXPECTED_NEWTON_DENOMINATOR
    )
    newton_shift = positive_shift_coefficients(newton, 7)
    assert len(newton_shift) == 38

    c3_gap = sp.cancel((3 * DEPTH**2) ** 7 - a7)
    c3_numerator, c3_denominator = c3_gap.as_numer_denom()
    c3_shift = positive_shift_coefficients(c3_gap, 7)
    assert len(c3_shift) == 22
    assert positive_shift_coefficients(a7, 7)

    h_rows, bands = derive_newton_and_long_recurrence()
    gamma6 = sp.cancel(bands[6])
    gamma_numerator, gamma_denominator = gamma6.as_numer_denom()
    assert gamma_denominator == SEVENTH_BAND_DENOMINATOR
    assert sp.Poly(gamma6, DEPTH).degree() == 20
    gamma_shift = tuple(
        int(value)
        for value in sp.Poly(
            sp.expand(gamma_numerator.subs(DEPTH, SHIFT + 13)),
            SHIFT,
        ).all_coeffs()
    )
    assert gamma_shift == SEVENTH_BAND_SHIFTED_COEFFICIENTS
    assert all(value > 0 for value in gamma_shift)
    assert sp.rem(gamma_numerator, DEPTH - 12, DEPTH) == 0
    assert gamma6.subs(DEPTH, 13) == FIRST_SEVENTH_BAND_VALUE

    h7 = sp.cancel(h_rows[7])
    forced_factor = sp.prod(DEPTH - root for root in range(7, 14))
    h7_quotient = sp.cancel(h7 / forced_factor)
    quotient_numerator, quotient_denominator = (
        h7_quotient.as_numer_denom()
    )
    assert not quotient_denominator.has(DEPTH)
    assert sp.cancel(h7 - forced_factor * h7_quotient) == 0
    assert all(h7.subs(DEPTH, root) == 0 for root in range(7, 14))
    forced_roots_are_simple = (
        sp.gcd(
            sp.Poly(quotient_numerator, DEPTH),
            sp.Poly(forced_factor, DEPTH),
        ).degree()
        == 0
    )

    boundary_calls = tuple(
        (lower_band, 12 - 2 * lower_band, 6 - lower_band)
        for lower_band in range(6)
    )
    assert all(depth == 2 * row for _, depth, row in boundary_calls)

    return {
        "schema": (
            "amra.opg1757.rank-seven-seventh-band."
            "independent-audit.v1"
        ),
        "status": "PASS",
        "author_verifier_imported": False,
        "symbol_audit": {
            "profile_symbol": repr(PROFILE_D),
            "audit_symbol": repr(DEPTH),
            "symbols_are_distinct": True,
            "profile_symbol_absent_from_all_triangle_betas": True,
        },
        "rank_seven": {
            "degree": interpolated.degree(),
            "degree_bound_used": 21,
            "interpolation_depths": list(interpolation_depths),
            "holdout_depths": list(holdout_depths),
            "fixed_depth_method": (
                "exact_ordinary_value plus independent defining "
                "Lagrange products and two page-count holdouts"
            ),
            "denominator": str(beta7_denominator),
            "p7_shifted_coefficients": list(p7_shift),
            "p7_shifted_coefficient_count": len(p7_shift),
            "p7_shifted_sha256": coefficient_hash(p7_shift),
        },
        "sixth_normalized_newton": {
            "reduced_denominator": str(
                sp.factor(newton_denominator)
            ),
            "shifted_coefficients": list(newton_shift),
            "shifted_coefficient_count": len(newton_shift),
            "shifted_sha256": coefficient_hash(newton_shift),
        },
        "rank_seven_c3": {
            "reduced_denominator": str(
                sp.factor(c3_denominator)
            ),
            "shifted_coefficients": list(c3_shift),
            "shifted_coefficient_count": len(c3_shift),
            "shifted_sha256": coefficient_hash(c3_shift),
        },
        "seventh_band": {
            "degree": 20,
            "denominator": str(gamma_denominator),
            "shifted_coefficients": list(gamma_shift),
            "shifted_coefficient_count": len(gamma_shift),
            "shifted_sha256": coefficient_hash(gamma_shift),
            "first_admissible_value": str(
                gamma6.subs(DEPTH, 13)
            ),
            "forced_factor": "depth-12",
            "h7_forced_roots": list(range(7, 14)),
            "h7_forced_roots_are_simple": forced_roots_are_simple,
            "h7_quotient_denominator": str(quotient_denominator),
            "boundary_lower_calls": [
                list(item) for item in boundary_calls
            ],
        },
    }


def main():
    print(json.dumps(audit(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
