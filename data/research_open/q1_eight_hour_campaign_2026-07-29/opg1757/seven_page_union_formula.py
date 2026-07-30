#!/usr/bin/env python3
"""Exact 877-state seven-page determinant and B7 finite audit."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import sympy as sp

from fixed_page_union_formula import (
    BETA,
    S,
    fixed_page_profile_polynomial,
    integer_convolution,
    linear_power,
)
from five_page_union_formula import (
    combine_polynomials,
    k3_coefficients,
    k4_coefficients,
    k5_coefficients,
)
from six_page_union_formula import k6_coefficients
from tp2_barrier_search import pooled_t_newton_rows


def k7_coefficients(s: int | sp.Expr) -> list[int | sp.Expr]:
    return [
        1,
        100,
        10 * (5 * s + 453),
        60 * (77 * s + 2038),
        30 * (40 * s**2 + 6354 * s + 72513),
        168 * (600 * s**2 + 27399 * s + 158428),
        420 * (43 * s**3 + 8839 * s**2 + 170460 * s + 539340),
        120
        * (
            11256 * s**3
            + 651595 * s**2
            + 6190899 * s
            + 11023313
        ),
        15
        * (
            12453 * s**4
            + 2885316 * s**3
            + 68609478 * s**2
            + 342599308 * s
            + 337908599
        ),
        20
        * (
            606123 * s**4
            + 38484110 * s**3
            + 433191366 * s**2
            + 1142127174 * s
            + 575188859
        ),
        2
        * (
            686217 * s**5
            + 163647225 * s**4
            + 4102800800 * s**3
            + 22781179428 * s**2
            + 29603885607 * s
            + 5872229027
        ),
        20
        * s
        * (
            3746295 * s**4
            + 235470718 * s**3
            + 2623832460 * s**2
            + 6846534048 * s
            + 3411019675
        ),
        210
        * s**2
        * (
            34310 * s**4
            + 7791186 * s**3
            + 181598497 * s**2
            + 888596684 * s
            + 858265555
        ),
        5880
        * s**3
        * (
            54143 * s**3
            + 3043161 * s**2
            + 28066561 * s
            + 48474286
        ),
        20580
        * s**4
        * (
            1300 * s**3
            + 257138 * s**2
            + 4771053 * s
            + 14513179
        ),
        57624 * s**5 * (15650 * s**2 + 681956 * s + 3760207),
        252105 * s**6 * (269 * s**2 + 40472 * s + 437180),
        7058940 * s**7 * (221 * s + 5500),
        8235430 * s**8 * (13 * s + 1101),
        1268256220 * s**9,
        80707214 * s**10,
    ]


def k7_polynomial() -> sp.Expr:
    return sum(
        coefficient * BETA**degree
        for degree, coefficient in enumerate(k7_coefficients(S))
    )


def derive_seven_page_determinant() -> tuple[list[sp.Expr], sp.Expr]:
    profiles = [
        fixed_page_profile_polynomial(7, two_blocks)
        for two_blocks in range(3)
    ]
    u7 = 1 + 7 * BETA
    normalized: list[sp.Expr] = []
    for two_blocks, profile in enumerate(profiles):
        exponent = S - (6 + 2 * two_blocks)
        normalized.append(sp.cancel(sp.factor(profile) / u7**exponent))
    reduced = sp.expand(normalized[1] ** 2 - normalized[0] * normalized[2])
    if sp.expand(reduced - 84 * BETA**4 * k7_polynomial()) != 0:
        raise AssertionError("the reduced seven-page determinant failed")
    return (
        profiles,
        84
        * BETA**4
        * u7 ** (2 * S - 16)
        * k7_polynomial(),
    )


def b7_bracket_coefficients(s: int) -> list[int]:
    if s < 8:
        raise ValueError("the B7 bracket starts at s=8")
    specifications = [
        (1, 0, 7, 2 * s - 16, k7_coefficients(s)),
        (-5, 2, 6, 2 * s - 14, k6_coefficients(s)),
        (-10, 6, 4, 2 * s - 10, k4_coefficients(s)),
        (10, 4, 5, 2 * s - 12, k5_coefficients(s)),
        (5, 8, 3, 2 * s - 8, k3_coefficients(s)),
        (-1, 10, 2, 2 * s - 6, [1]),
    ]
    terms: list[tuple[int, list[int]]] = []
    for multiplier, lambda_degree, base, exponent, kernel in specifications:
        polynomial = integer_convolution(
            linear_power(s, lambda_degree),
            linear_power(base, exponent),
        )
        polynomial = integer_convolution(
            polynomial, [int(value) for value in kernel]
        )
        terms.append((multiplier, polynomial))
    return combine_polynomials(*terms)


def b7_coefficients(s: int) -> list[int]:
    if s < 7:
        return [0]
    if s == 7:
        return [0] * 14 + [
            1253568960,
            21961658880,
            165977864640,
            622090264320,
            1029362866560,
        ]
    if s == 8:
        boundary = [
            229263,
            9163072,
            166537216,
            1802240000,
            12751831040,
            60682141696,
            190635311104,
            363595825152,
            324957896704,
        ]
        return [0] * 14 + [60480 * value for value in boundary]
    bracket = b7_bracket_coefficients(s)
    return [0] * 4 + [
        84 * value
        for value in integer_convolution(
            linear_power(s, 2 * s - 18), bracket
        )
    ]


def recurrence_remainder_coefficients(s: int) -> list[int]:
    return combine_polynomials(
        (1, b7_bracket_coefficients(s + 1)),
        (
            -1,
            integer_convolution(
                linear_power(7, 2),
                b7_bracket_coefficients(s),
            ),
        ),
    )


def build_certificate(maximum_s: int = 120) -> dict[str, object]:
    profiles, determinant = derive_seven_page_determinant()
    rows: list[list[object]] = []
    for s in range(7, 11):
        pooled = {
            degree: int(coefficient)
            for order, degree, coefficient in pooled_t_newton_rows(
                s, 4 * s - 8
            )
            if order == 7
        }
        formula = {
            degree: coefficient
            for degree, coefficient in enumerate(b7_coefficients(s))
            if coefficient
        }
        if pooled != formula:
            raise AssertionError(f"B7 mismatch at s={s}")
        rows.extend(
            [s, degree, str(coefficient)]
            for degree, coefficient in sorted(pooled.items())
        )

    summaries: list[list[object]] = []
    recurrence_summaries: list[list[object]] = []
    first_negative = None
    first_recurrence_negative = None
    for s in range(8, maximum_s + 1):
        coefficients = b7_bracket_coefficients(s)
        support = [(d, value) for d, value in enumerate(coefficients) if value]
        if first_negative is None:
            for degree, value in enumerate(coefficients):
                if value < 0:
                    first_negative = [s, degree, str(value)]
                    break
        summaries.append(
            [s, support[0][0], support[-1][0], str(min(x[1] for x in support))]
        )
        if s < maximum_s:
            remainder = recurrence_remainder_coefficients(s)
            remainder_support = [
                (d, value) for d, value in enumerate(remainder) if value
            ]
            if first_recurrence_negative is None:
                for degree, value in enumerate(remainder):
                    if value < 0:
                        first_recurrence_negative = [s, degree, str(value)]
                        break
            recurrence_summaries.append(
                [
                    s,
                    remainder_support[0][0],
                    remainder_support[-1][0],
                    str(min(x[1] for x in remainder_support)),
                ]
            )

    payload = json.dumps(rows, separators=(",", ":")).encode("utf-8")
    return {
        "schema": "amra.complete_split.seven_page_union.v1",
        "partition_state_count": 877,
        "profile_polynomials_seven_pages": [str(value) for value in profiles],
        "seven_page_determinant": str(determinant),
        "K7": str(k7_polynomial()),
        "B7_formula": (
            "For s>=9, B7=84 beta^4 lambda^(2s-18) F_s, where "
            "F_s=u7^(2s-16)K7-5lambda^2*u6^(2s-14)K6"
            "+10lambda^4*u5^(2s-12)K5"
            "-10lambda^6*u4^(2s-10)K4"
            "+5lambda^8*u3^(2s-8)K3-lambda^10*u2^(2s-6)."
        ),
        "boundary_values": {
            "s7": (
                "987840*beta^14*(1042034*beta^4+629748*beta^3"
                "+168021*beta^2+22232*beta+1269)"
            ),
            "s8": (
                "60480*beta^14*(324957896704*beta^8"
                "+363595825152*beta^7+190635311104*beta^6"
                "+60682141696*beta^5+12751831040*beta^4"
                "+1802240000*beta^3+166537216*beta^2"
                "+9163072*beta+229263)"
            ),
        },
        "pooled_transfer_rows_s7_to_s10": rows,
        "sha256_pooled_rows": hashlib.sha256(payload).hexdigest(),
        "finite_bracket_audit": {
            "s_range": [8, maximum_s],
            "first_negative": first_negative,
            "summaries": summaries,
        },
        "finite_recurrence_audit": {
            "s_range": [8, maximum_s - 1],
            "first_negative": first_recurrence_negative,
            "summaries": recurrence_summaries,
        },
        "proof_status": (
            "The 877-state determinant and all-s alternating formula are "
            "proved. The coefficient audits are finite; uniform B7 "
            "positivity is not proved."
        ),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--maximum-s", type=int, default=120)
    parser.add_argument("--output", type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    certificate = build_certificate(args.maximum_s)
    rendered = json.dumps(certificate, indent=2, sort_keys=True)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + "\n", encoding="utf-8")
        print(f"wrote {args.output}")
    else:
        print(rendered)


if __name__ == "__main__":
    main()
