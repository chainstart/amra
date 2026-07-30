#!/usr/bin/env python3
"""Exact five-page determinant, B5 bracket, and recurrence audit.

The 52 page partitions are handled by ``fixed_page_profile_polynomial``.
The resulting determinant gives an all-s closed form.  Fast integer
convolutions then audit every coefficient of the B5 bracket and of the
candidate s-recurrence remainder.
"""

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
    k3_polynomial,
    k4_polynomial,
    linear_power,
)
from tp2_barrier_search import pooled_t_newton_rows


def k5_polynomial() -> sp.Expr:
    return (
        1
        + 48 * BETA
        + (24 * S + 960) * BETA**2
        + (980 * S + 10180) * BETA**3
        + (255 * S**2 + 15840 * S + 60045) * BETA**4
        + (8340 * S**2 + 126036 * S + 186420) * BETA**5
        + (
            1480 * S**3
            + 100240 * S**2
            + 494158 * S
            + 238210
        )
        * BETA**6
        + (35640 * S**3 + 528024 * S**2 + 766380 * S) * BETA**7
        + (4755 * S**4 + 283440 * S**3 + 1034550 * S**2)
        * BETA**8
        + (76300 * S**4 + 749000 * S**3) * BETA**9
        + (8250 * S**5 + 306750 * S**4) * BETA**10
        + 67500 * S**5 * BETA**11
        + 6250 * S**6 * BETA**12
    )


def k3_coefficients(s: int) -> list[int]:
    return [1, 12, 6 * s + 30, 28 * s, 6 * s**2]


def k4_coefficients(s: int) -> list[int]:
    return [
        1,
        28,
        14 * s + 288,
        292 * s + 1264,
        75 * s**2 + 1918 * s + 2008,
        968 * s**2 + 4064 * s,
        160 * s**3 + 3072 * s**2,
        1024 * s**3,
        128 * s**4,
    ]


def k5_coefficients(s: int) -> list[int]:
    return [
        1,
        48,
        24 * s + 960,
        980 * s + 10180,
        255 * s**2 + 15840 * s + 60045,
        8340 * s**2 + 126036 * s + 186420,
        1480 * s**3 + 100240 * s**2 + 494158 * s + 238210,
        35640 * s**3 + 528024 * s**2 + 766380 * s,
        4755 * s**4 + 283440 * s**3 + 1034550 * s**2,
        76300 * s**4 + 749000 * s**3,
        8250 * s**5 + 306750 * s**4,
        67500 * s**5,
        6250 * s**6,
    ]


def combine_polynomials(*terms: tuple[int, list[int]]) -> list[int]:
    maximum = max(len(coefficients) for _, coefficients in terms)
    result = [
        sum(
            multiplier
            * (coefficients[degree] if degree < len(coefficients) else 0)
            for multiplier, coefficients in terms
        )
        for degree in range(maximum)
    ]
    while len(result) > 1 and result[-1] == 0:
        result.pop()
    return result


def derive_five_page_determinant() -> tuple[list[sp.Expr], sp.Expr]:
    profiles = [
        fixed_page_profile_polynomial(5, two_blocks)
        for two_blocks in range(3)
    ]
    determinant = sp.powsimp(
        profiles[1] ** 2 - profiles[0] * profiles[2],
        force=True,
    )
    expected = (
        40
        * BETA**4
        * (1 + 5 * BETA) ** (2 * S - 12)
        * k5_polynomial()
    )
    ratio = sp.cancel(sp.powsimp(determinant / expected, force=True))
    if sp.factor(sp.expand_func(ratio)) != 1:
        raise AssertionError("the five-page determinant formula failed")
    return profiles, expected


def b5_bracket_coefficients(s: int) -> list[int]:
    """Coefficients of the four-exponential bracket F_s, for s>=6."""

    if s < 6:
        raise ValueError("the polynomial bracket starts at s=6")
    term5 = integer_convolution(
        linear_power(5, 2 * s - 12),
        k5_coefficients(s),
    )
    term4 = integer_convolution(
        integer_convolution(
            linear_power(s, 2),
            linear_power(4, 2 * s - 10),
        ),
        k4_coefficients(s),
    )
    term3 = integer_convolution(
        integer_convolution(
            linear_power(s, 4),
            linear_power(3, 2 * s - 8),
        ),
        k3_coefficients(s),
    )
    term2 = integer_convolution(
        linear_power(s, 6),
        linear_power(2, 2 * s - 6),
    )
    return combine_polynomials(
        (1, term5),
        (-3, term4),
        (3, term3),
        (-1, term2),
    )


def b5_expression_at_s(s: int) -> sp.Expr:
    if s < 5:
        return sp.S.Zero
    if s == 5:
        return 12000 * BETA**10
    if s == 6:
        return (
            1440
            * BETA**10
            * (
                54000 * BETA**4
                + 44352 * BETA**3
                + 15408 * BETA**2
                + 2600 * BETA
                + 181
            )
        )
    bracket = sum(
        coefficient * BETA**degree
        for degree, coefficient in enumerate(b5_bracket_coefficients(s))
    )
    return sp.expand(
        40
        * BETA**4
        * (1 + s * BETA) ** (2 * s - 14)
        * bracket
    )


def recurrence_remainder_coefficients(s: int) -> list[int]:
    """Coefficients of F_{s+1}-(1+5 beta)^2 F_s."""

    current = b5_bracket_coefficients(s)
    following = b5_bracket_coefficients(s + 1)
    transported = integer_convolution(linear_power(5, 2), current)
    return combine_polynomials((1, following), (-1, transported))


def build_certificate(maximum_s: int = 200) -> dict[str, object]:
    profiles, determinant = derive_five_page_determinant()
    rows: list[list[object]] = []
    for s in range(5, 10):
        pooled = {
            degree: int(coefficient)
            for order, degree, coefficient in pooled_t_newton_rows(
                s, 4 * s - 8
            )
            if order == 5
        }
        expected_polynomial = sp.Poly(b5_expression_at_s(s), BETA)
        expected = {
            degree: int(expected_polynomial.coeff_monomial(BETA**degree))
            for degree in range(expected_polynomial.degree() + 1)
            if expected_polynomial.coeff_monomial(BETA**degree)
        }
        if pooled != expected:
            raise AssertionError(f"B5 mismatch at s={s}")
        rows.extend(
            [s, degree, str(coefficient)]
            for degree, coefficient in sorted(pooled.items())
        )

    bracket_summaries: list[list[object]] = []
    recurrence_summaries: list[list[object]] = []
    first_negative: list[object] | None = None
    first_recurrence_negative: list[object] | None = None
    digest = hashlib.sha256()
    recurrence_digest = hashlib.sha256()
    for s in range(6, maximum_s + 1):
        coefficients = b5_bracket_coefficients(s)
        support = [
            (degree, value)
            for degree, value in enumerate(coefficients)
            if value
        ]
        for degree, value in enumerate(coefficients):
            digest.update(f"{s},{degree},{value}\n".encode("ascii"))
            if value < 0 and first_negative is None:
                first_negative = [s, degree, str(value)]
        bracket_summaries.append(
            [s, support[0][0], support[-1][0], str(min(x[1] for x in support))]
        )
        if s < maximum_s:
            remainder = recurrence_remainder_coefficients(s)
            remainder_support = [
                (degree, value)
                for degree, value in enumerate(remainder)
                if value
            ]
            for degree, value in enumerate(remainder):
                recurrence_digest.update(
                    f"{s},{degree},{value}\n".encode("ascii")
                )
                if value < 0 and first_recurrence_negative is None:
                    first_recurrence_negative = [s, degree, str(value)]
            recurrence_summaries.append(
                [
                    s,
                    remainder_support[0][0],
                    remainder_support[-1][0],
                    str(min(x[1] for x in remainder_support)),
                ]
            )

    row_payload = json.dumps(rows, separators=(",", ":")).encode("utf-8")
    return {
        "schema": "amra.complete_split.five_page_union.v1",
        "partition_state_count": 52,
        "profile_polynomials_five_pages": [str(value) for value in profiles],
        "five_page_determinant": str(determinant),
        "K5": str(k5_polynomial()),
        "B5_formula": (
            "For s>=7, B5=40 beta^4 lambda^(2s-14) F_s, where "
            "F_s=(1+5beta)^(2s-12)K5"
            "-3lambda^2(1+4beta)^(2s-10)K4"
            "+3lambda^4(1+3beta)^(2s-8)K3"
            "-lambda^6(1+2beta)^(2s-6). "
            "The exact boundary values are stored separately."
        ),
        "boundary_values": {
            "s_lt_5": "0",
            "s5": "12000*beta^10",
            "s6": (
                "1440*beta^10*(54000*beta^4+44352*beta^3"
                "+15408*beta^2+2600*beta+181)"
            ),
        },
        "pooled_transfer_rows_s5_to_s9": rows,
        "sha256_pooled_rows": hashlib.sha256(row_payload).hexdigest(),
        "bracket_counterexample_search": {
            "s_range": [6, maximum_s],
            "first_negative": first_negative,
            "all_searched_coefficients_nonnegative": first_negative is None,
            "summaries_s_first_degree_last_degree_minimum": bracket_summaries,
            "sha256_all_lines": digest.hexdigest(),
        },
        "candidate_positive_recurrence_search": {
            "identity": "R_s=F_(s+1)-(1+5beta)^2 F_s",
            "s_range": [6, maximum_s - 1],
            "first_negative": first_recurrence_negative,
            "all_searched_coefficients_nonnegative": (
                first_recurrence_negative is None
            ),
            "summaries_s_first_degree_last_degree_minimum": (
                recurrence_summaries
            ),
            "sha256_all_lines": recurrence_digest.hexdigest(),
        },
        "proof_status": (
            "The 52-state determinant and the all-s B5 formula are proved. "
            "The complete coefficient scans and recurrence scans are finite "
            "audits, not an unbounded-s positivity proof."
        ),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--maximum-s", type=int, default=200)
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
