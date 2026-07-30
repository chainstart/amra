#!/usr/bin/env python3
"""Independent exact audit of the sixth ordinary long-recurrence band.

This script deliberately does not import the author's
``verify_ordinary_sixth_long_recurrence_band`` module.  It imports only
the previously audited printed rank-six ordinary symbol and rebuilds
the three required triangles here.
"""

from __future__ import annotations

import json
from functools import lru_cache

import sympy as sp

from independent_verify_ordinary_rank_six_symbol import (
    rank_six_polynomial,
)


D = sp.symbols("d", integer=True)
N = sp.symbols("n", integer=True, nonnegative=True)
J = sp.symbols("j", integer=True, nonnegative=True)
U = sp.symbols("u", integer=True, nonnegative=True)

SIXTH_DENOMINATOR = sp.Integer(15359376162816000)
R5_COEFFICIENTS = (
    810123093896375,
    -25921081431700875,
    313490671217497970,
    -1492874651122299900,
    -1887303336152228890,
    49625869946758088130,
    -167524355872717489604,
    -106706576731710308472,
    1816293817555406107219,
    -3108681098587146424959,
    -2327663884048779946070,
    9529661544865824480588,
    -493471326045590983080,
    -8190583449886689443856,
    -15710022013283259194016,
    29745938852108657679744,
    -5169307325421355490304,
)
SHIFTED_NUMERATOR_COEFFICIENTS = (
    810123093896375,
    117470706187957500,
    7916160141456279720,
    329090197951577059200,
    9446873816558259471810,
    198583558207712884868760,
    3162912470191756651508636,
    38951480639440722082621584,
    375079850835431480188544199,
    2836468344865020127987279932,
    16817548301644562228270567652,
    77567404341593653627142341584,
    274129824219295871333741310776,
    723941511230071673766897349008,
    1371903306568738801868891133792,
    1742598030043436615873060144832,
    1304914777582506924209367824640,
    421161144536910289212100915200,
)
FIRST_ADMISSIBLE_VALUE = sp.Rational(
    3316778722205903687, 120960
)


def polynomial_from_descending(
    coefficients: tuple[int, ...],
    variable: sp.Symbol,
) -> sp.Expr:
    degree = len(coefficients) - 1
    return sum(
        sp.Integer(coefficient) * variable ** (degree - index)
        for index, coefficient in enumerate(coefficients)
    )


def printed_lower_rank_symbols(variable: sp.Symbol = D) -> list[sp.Expr]:
    """Return the printed beta_(d,0),...,beta_(d,5) identities."""

    x = variable
    return [
        sp.Integer(1),
        -(
            22 * x**3 + 147 * x**2 + 161 * x - 258
        )
        / sp.Integer(36),
        (
            286 * x**6
            + 3546 * x**5
            + 12721 * x**4
            - 7812 * x**3
            - 86231 * x**2
            + 40338 * x
            + 209160
        )
        / sp.Integer(5184),
        -(
            158450 * x**9
            + 2651625 * x**8
            + 15805020 * x**7
            + 6658380 * x**6
            - 213815208 * x**5
            - 151402725 * x**4
            + 2063879770 * x**3
            + 1562087520 * x**2
            - 10631426832 * x
            - 6142443840
        )
        / sp.Integer(83980800),
        (
            5672590 * x**12
            + 111345780 * x**11
            + 940800098 * x**10
            + 1247424360 * x**9
            - 19928038791 * x**8
            - 49386060432 * x**7
            + 332001672380 * x**6
            + 627890141256 * x**5
            - 5187992393129 * x**4
            - 5254056336228 * x**3
            + 25894282085892 * x**2
            + 59075314211664 * x
            - 31756394113920
        )
        / sp.Integer(169305292800),
        (
            -15479380 * x**15
            - 325941210 * x**14
            - 3742393522 * x**13
            - 6592418448 * x**12
            + 111326408900 * x**11
            + 573131680737 * x**10
            - 2606390331587 * x**9
            - 10630453797180 * x**8
            + 79178201476618 * x**7
            + 110117646980439 * x**6
            - 1139766102529649 * x**5
            - 2901603595595082 * x**4
            + 14532178406634252 * x**3
            + 4464839765897784 * x**2
            + 14350329772954848 * x
            - 57046347650960640
        )
        / sp.Integer(42664933785600),
    ]


def polynomial_binomial(top: sp.Expr, bottom: int) -> sp.Expr:
    """Polynomial version of binomial(top,bottom), bottom >= 0."""

    if bottom < 0:
        return sp.Integer(0)
    return sp.prod(top - offset for offset in range(bottom)) / sp.factorial(
        bottom
    )


@lru_cache(maxsize=None)
def signed_stirling_loss_rows(maximum_loss: int) -> tuple[sp.Expr, ...]:
    """Build s(n,n-r) independently via Newton's identities.

    Since
        (x)_n = product_{a=0}^{n-1}(x-a),
    the signed near-diagonal coefficient is
        s(n,n-r)=(-1)^r e_r(0,1,...,n-1).
    Newton's identities construct the elementary symmetric functions
    from exact Faulhaber power sums.  This is independent of the
    antidifference implementation used in the earlier audit.
    """

    elementary = [sp.Integer(1)]
    power_sums = {
        power: sp.expand(
            sp.summation(J**power, (J, 0, N - 1))
        )
        for power in range(1, maximum_loss + 1)
    }
    for loss in range(1, maximum_loss + 1):
        next_elementary = sum(
            (-1) ** (power - 1)
            * elementary[loss - power]
            * power_sums[power]
            for power in range(1, loss + 1)
        ) / sp.Integer(loss)
        elementary.append(
            sp.factor(sp.cancel(next_elementary))
        )

    signed = tuple(
        sp.factor((-1) ** loss * elementary[loss])
        for loss in range(maximum_loss + 1)
    )
    for loss in range(1, maximum_loss + 1):
        recurrence_residual = (
            signed[loss].subs(N, N + 1)
            - signed[loss]
            + N * signed[loss - 1]
        )
        assert sp.expand(recurrence_residual) == 0
        assert signed[loss].subs(N, 0) == 0
    return signed


@lru_cache(maxsize=None)
def derive_triangles() -> tuple[tuple[sp.Expr, ...], tuple[sp.Expr, ...]]:
    """Rebuild h_(d,0..6) and gamma_(d,0..5) from printed symbols."""

    beta = printed_lower_rank_symbols(D)
    beta.append(rank_six_polynomial(D))
    stirling = signed_stirling_loss_rows(6)

    h_rows = [sp.Integer(1)]
    for loss in range(1, 7):
        ordinary_coefficient = sum(
            beta[rank]
            * polynomial_binomial(D - rank, loss - rank)
            * 2 ** (loss - rank)
            for rank in range(loss + 1)
        )
        lower_falling_rows = sum(
            h_rows[row]
            * stirling[loss - row].subs(N, D - row)
            for row in range(loss)
        )
        h_rows.append(
            sp.factor(
                sp.cancel(
                    sp.expand(ordinary_coefficient - lower_falling_rows)
                )
            )
        )

    bands: list[sp.Expr] = []
    for band in range(6):
        coefficient = (
            h_rows[band + 1]
            - h_rows[band + 1].subs(D, D + 1)
        )
        coefficient -= sum(
            bands[lower_band]
            * h_rows[band - lower_band].subs(
                D, D - 1 - 2 * lower_band
            )
            for lower_band in range(band)
        )
        bands.append(
            sp.factor(sp.cancel(sp.expand(coefficient)))
        )
    return tuple(h_rows), tuple(bands)


def expected_sixth_band() -> sp.Expr:
    r5 = polynomial_from_descending(R5_COEFFICIENTS, D)
    return (D - 10) * r5 / SIXTH_DENOMINATOR


def audit() -> dict[str, object]:
    h_rows, bands = derive_triangles()
    gamma5 = sp.cancel(bands[5])
    expected = sp.cancel(expected_sixth_band())

    assert sp.cancel(gamma5 - expected) == 0
    numerator, denominator = gamma5.as_numer_denom()
    assert denominator == SIXTH_DENOMINATOR
    assert sp.expand(numerator) == sp.expand(
        (D - 10) * polynomial_from_descending(R5_COEFFICIENTS, D)
    )
    assert sp.Poly(
        polynomial_from_descending(R5_COEFFICIENTS, D), D
    ).degree() == 16
    assert sp.Poly(gamma5, D).degree() == 17

    shifted = sp.Poly(
        sp.expand(SIXTH_DENOMINATOR * gamma5.subs(D, U + 11)),
        U,
    )
    shifted_coefficients = tuple(
        int(value) for value in shifted.all_coeffs()
    )
    assert shifted_coefficients == SHIFTED_NUMERATOR_COEFFICIENTS
    assert len(shifted_coefficients) == 18
    assert all(value > 0 for value in shifted_coefficients)

    actual_first_value = sp.cancel(gamma5.subs(D, 11))
    assert actual_first_value == FIRST_ADMISSIBLE_VALUE

    h6 = sp.cancel(h_rows[6])
    forced_factor = sp.prod(D - root for root in range(6, 12))
    h6_quotient = sp.cancel(h6 / forced_factor)
    quotient_expression_numerator, quotient_denominator = (
        h6_quotient.as_numer_denom()
    )
    assert not quotient_denominator.has(D)
    assert sp.cancel(h6 - forced_factor * h6_quotient) == 0
    for root in range(6, 12):
        assert h6.subs(D, root) == 0
    quotient_numerator = sp.Poly(quotient_expression_numerator, D)
    assert quotient_numerator.degree() == 12
    assert quotient_numerator.LC() > 0
    assert sp.gcd(quotient_numerator, sp.Poly(forced_factor, D)).degree() == 0
    assert all(
        h6_quotient.subs(D, root) != 0 for root in range(6, 12)
    )

    # A direct boundary-index check: every lower h-call used for q=5
    # is at its legal first depth when d=11.
    boundary_calls = tuple(
        (lower_band, 10 - 2 * lower_band, 5 - lower_band)
        for lower_band in range(5)
    )
    assert all(depth == 2 * row for _, depth, row in boundary_calls)

    return {
        "schema": (
            "amra.opg1757.sixth-long-recurrence-band."
            "independent-audit.v1"
        ),
        "status": "PASS",
        "forbidden_author_verifier_imported": False,
        "signed_stirling_method": (
            "Newton identities from exact Faulhaber power sums"
        ),
        "derived_band": 5,
        "gamma_degree": 17,
        "reduced_denominator": str(denominator),
        "r5_degree": 16,
        "r5_coefficients": list(R5_COEFFICIENTS),
        "shift": "d=u+11",
        "positive_shift_coefficient_count": len(
            shifted_coefficients
        ),
        "positive_shift_coefficients": list(shifted_coefficients),
        "gamma_11_5": str(actual_first_value),
        "h6_forced_roots": list(range(6, 12)),
        "h6_forced_roots_are_simple": True,
        "h6_quotient_denominator": str(quotient_denominator),
        "h6_quotient_degree": quotient_numerator.degree(),
        "h6_quotient_positive_leading_coefficient": True,
        "boundary_lower_calls": [list(item) for item in boundary_calls],
    }


def main() -> None:
    print(json.dumps(audit(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
