#!/usr/bin/env python3
"""Independent symbolic audit of the first five long-recurrence bands."""

from __future__ import annotations

import argparse
import json

import sympy as sp


d = sp.symbols("d", integer=True)
u = sp.symbols("u", integer=True, nonnegative=True)


def beta_polynomials(variable=d):
    """The six previously proved ordinary-power symbols."""
    x = variable
    return [
        sp.Integer(1),
        -(
            22 * x**3 + 147 * x**2 + 161 * x - 258
        ) / sp.Integer(36),
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


def near_diagonal_stirling(maximum_loss: int):
    """Construct s(n,n-m) by exact antidifference, not interpolation."""
    n, k = sp.symbols("n k", integer=True, nonnegative=True)
    rows = [sp.Integer(1)]
    for loss in range(1, maximum_loss + 1):
        previous_at_k = rows[-1].subs(n, k)
        current = sp.summation(-k * previous_at_k, (k, 0, n - 1))
        current = sp.factor(current)
        assert sp.expand(current.subs(n, 0)) == 0
        assert sp.expand(
            current.subs(n, n + 1) - current + n * rows[-1]
        ) == 0
        rows.append(current)
    return n, rows


def ordinary_to_newton_rows(maximum_row: int = 5):
    n, stirling_rows = near_diagonal_stirling(maximum_row)
    betas = beta_polynomials(d)
    h_rows = [sp.Integer(1)]
    for ell in range(1, maximum_row + 1):
        moment = sum(
            betas[rank]
            * sp.binomial(d - rank, ell - rank)
            * 2 ** (ell - rank)
            for rank in range(ell + 1)
        )
        correction = sum(
            h_rows[index]
            * stirling_rows[ell - index].subs(n, d - index)
            for index in range(ell)
        )
        # Expand polynomial binomials explicitly; otherwise SymPy retains
        # binomial(d-r, ell-r) as a non-polynomial function node.
        h_rows.append(
            sp.factor(sp.cancel(sp.expand_func(moment - correction)))
        )
    return h_rows


def recurrence_bands(maximum_band: int = 4):
    h_rows = ordinary_to_newton_rows(maximum_band + 1)
    gammas = []
    for band in range(maximum_band + 1):
        value = h_rows[band + 1] - h_rows[band + 1].subs(d, d + 1)
        value -= sum(
            gammas[index]
            * h_rows[band - index].subs(d, d - 1 - 2 * index)
            for index in range(band)
        )
        gammas.append(sp.factor(sp.cancel(sp.expand_func(value))))
    return h_rows, gammas


def expected_gamma_polynomials():
    return [
        (d + 1) * (11 * d + 43) / sp.Integer(6),
        (d - 2)
        * (
            341 * d**4
            + 3269 * d**3
            + 10852 * d**2
            + 15838 * d
            + 11094
        )
        / sp.Integer(432),
        (d - 4)
        * (
            371585 * d**7
            + 3038100 * d**6
            + 6227486 * d**5
            - 2746356 * d**4
            - 12009655 * d**3
            + 7914888 * d**2
            + 37057752 * d
            + 36634680
        )
        / sp.Integer(933120),
        (d - 6)
        * (
            477026935 * d**10
            + 373655975 * d**9
            - 13198014515 * d**8
            - 2356653705 * d**7
            + 116744157150 * d**6
            + 348820236 * d**5
            - 321203446846 * d**4
            - 58621959506 * d**3
            + 534175684124 * d**2
            + 708834254088 * d
            - 180164960640
        )
        / sp.Integer(2351462400),
        (d - 8)
        * (
            8756143850 * d**13
            - 110386703260 * d**12
            + 169932034915 * d**11
            + 2946121856418 * d**10
            - 11807084667619 * d**9
            - 13369462591602 * d**8
            + 122184475184308 * d**7
            - 78467819453648 * d**6
            - 324534244911847 * d**5
            + 252862845724584 * d**4
            + 483781271752093 * d**3
            + 76417691692068 * d**2
            - 1176624827988660 * d
            + 229574732844240
        )
        / sp.Integer(84652646400),
    ]


def shifted_positive_rows(gammas):
    denominators = [
        6,
        432,
        933120,
        2351462400,
        84652646400,
    ]
    rows = []
    for band, (gamma, denominator) in enumerate(
        zip(gammas, denominators)
    ):
        shifted = sp.Poly(
            sp.cancel(denominator * gamma.subs(d, u + 2 * band + 1)),
            u,
        )
        coefficients = [int(value) for value in shifted.all_coeffs()]
        assert all(value > 0 for value in coefficients)
        rows.append(coefficients)
    return rows


def forced_factor_audit(h_rows):
    factor4 = sp.prod(d - value for value in range(4, 8))
    factor5 = sp.prod(d - value for value in range(5, 10))
    quotient4 = sp.cancel(h_rows[4] / factor4)
    quotient5_signed = sp.cancel(h_rows[5] / (-factor5))
    assert not sp.denom(quotient4).has(d)
    assert not sp.denom(quotient5_signed).has(d)
    assert sp.cancel(h_rows[4] - factor4 * quotient4) == 0
    assert sp.cancel(h_rows[5] + factor5 * quotient5_signed) == 0
    assert sp.LC(sp.Poly(sp.numer(quotient4), d)) > 0
    assert sp.LC(sp.Poly(sp.numer(quotient5_signed), d)) > 0
    for value in range(4, 8):
        assert h_rows[4].subs(d, value) == 0
    for value in range(5, 10):
        assert h_rows[5].subs(d, value) == 0
    return {
        "h4_forced_roots": list(range(4, 8)),
        "h5_forced_roots": list(range(5, 10)),
        "h4_quotient_degree": int(sp.degree(quotient4, d)),
        "h5_signed_quotient_degree": int(
            sp.degree(quotient5_signed, d)
        ),
        "h4_quotient_leading_positive": True,
        "h5_after_minus_quotient_leading_positive": True,
    }


def index_audit(gammas):
    records = []
    for band, gamma in enumerate(gammas):
        minimum_depth = 2 * band + 1
        value = sp.cancel(gamma.subs(d, minimum_depth))
        assert value > 0
        # Every lower H index in the triangular sum is legal at d_min.
        calls = [
            (
                minimum_depth - 1 - 2 * index,
                band - index,
            )
            for index in range(band)
        ]
        assert all(depth >= 2 * row for depth, row in calls)
        records.append(
            {
                "band": band,
                "minimum_depth": minimum_depth,
                "minimum_value": str(value),
                "lower_h_calls": calls,
            }
        )
    return records


def audit():
    h_rows, gammas = recurrence_bands()
    expected = expected_gamma_polynomials()
    for actual, target in zip(gammas, expected):
        assert sp.cancel(actual - target) == 0
    shifted = shifted_positive_rows(gammas)
    return {
        "schema": "amra.opg1757.ordinary-first-five-long-bands-independent.v1",
        "verdict": "PASS",
        "scope": (
            "Independent symbolic recomputation from the six printed beta "
            "polynomials, exact Stirling antidifferences, and the triangular "
            "recurrence. No author verifier is imported."
        ),
        "gamma_identity_checks": len(gammas),
        "shifted_positive_row_lengths": [len(row) for row in shifted],
        "shifted_positive_rows": shifted,
        "index_audit": index_audit(gammas),
        "forced_factor_audit": forced_factor_audit(h_rows),
        "author_verifier_imported": False,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    print(json.dumps(audit(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
