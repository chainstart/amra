#!/usr/bin/env python3
"""Exact 203-state six-page determinant and B6 coefficient audit."""

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
from tp2_barrier_search import pooled_t_newton_rows


def k6_polynomial() -> sp.Expr:
    return sum(
        coefficient * BETA**degree
        for degree, coefficient in enumerate(k6_coefficients(S))
    )


def k6_coefficients(s: int | sp.Expr) -> list[int | sp.Expr]:
    return [
        1,
        72,
        36 * s + 2280,
        2328 * s + 41376,
        606 * s**2 + 64584 * s + 469440,
        34200 * s**2 + 993696 * s + 3401856,
        6132 * s**3 + 801000 * s**2 + 9138432 * s + 15351552,
        290760 * s**3 + 9949536 * s**2 + 50186016 * s + 39415680,
        (
            40005 * s**4
            + 5475600 * s**3
            + 69145068 * s**2
            + 152427744 * s
            + 44093376
        ),
        (
            1519680 * s**4
            + 51293056 * s**3
            + 255254400 * s**2
            + 197743104 * s
        ),
        (
            169776 * s**5
            + 21571680 * s**4
            + 239604480 * s**3
            + 391841280 * s**2
        ),
        4871232 * s**5 + 136035072 * s**4 + 447731712 * s**3,
        461376 * s**6 + 46699200 * s**5 + 322548480 * s**4,
        8978688 * s**6 + 150045696 * s**5,
        746496 * s**7 + 44043264 * s**6,
        7464960 * s**7,
        559872 * s**8,
    ]


def derive_six_page_determinant() -> tuple[list[sp.Expr], sp.Expr]:
    """Use factored profiles to avoid expanding symbolic powers of u6."""

    profiles = [
        fixed_page_profile_polynomial(6, two_blocks)
        for two_blocks in range(3)
    ]
    u6 = 1 + 6 * BETA
    normalized: list[sp.Expr] = []
    for two_blocks, profile in enumerate(profiles):
        factored = sp.factor(profile)
        exponent = S - (2 * two_blocks + 5)
        normalized.append(sp.cancel(factored / u6**exponent))
    reduced_determinant = sp.expand(
        normalized[1] ** 2 - normalized[0] * normalized[2]
    )
    expected_reduced = 60 * BETA**4 * k6_polynomial()
    if sp.expand(reduced_determinant - expected_reduced) != 0:
        raise AssertionError("the reduced six-page determinant failed")
    determinant = (
        60
        * BETA**4
        * u6 ** (2 * S - 14)
        * k6_polynomial()
    )
    return profiles, determinant


def b6_bracket_coefficients(s: int) -> list[int]:
    """Coefficients of the five-exponential bracket F_s^(6), s>=7."""

    if s < 7:
        raise ValueError("the B6 bracket polynomial starts at s=7")
    term6 = integer_convolution(
        linear_power(6, 2 * s - 14),
        [int(value) for value in k6_coefficients(s)],
    )
    term5 = integer_convolution(
        integer_convolution(
            linear_power(s, 2),
            linear_power(5, 2 * s - 12),
        ),
        k5_coefficients(s),
    )
    term4 = integer_convolution(
        integer_convolution(
            linear_power(s, 4),
            linear_power(4, 2 * s - 10),
        ),
        k4_coefficients(s),
    )
    term3 = integer_convolution(
        integer_convolution(
            linear_power(s, 6),
            linear_power(3, 2 * s - 8),
        ),
        k3_coefficients(s),
    )
    term2 = integer_convolution(
        linear_power(s, 8),
        linear_power(2, 2 * s - 6),
    )
    return combine_polynomials(
        (1, term6),
        (-4, term5),
        (6, term4),
        (-4, term3),
        (1, term2),
    )


def b6_coefficients(s: int) -> list[int]:
    if s < 6:
        return [0]
    if s == 6:
        return [0] * 12 + [3732480, 27371520, 74649600]
    if s == 7:
        boundary = [
            7019,
            181174,
            2059813,
            13220592,
            50848378,
            112001848,
            112001848,
        ]
        return [0] * 12 + [7200 * value for value in boundary]
    bracket = b6_bracket_coefficients(s)
    return [0] * 4 + [
        60 * value
        for value in integer_convolution(
            linear_power(s, 2 * s - 16),
            bracket,
        )
    ]


def recurrence_remainder_coefficients(s: int) -> list[int]:
    current = b6_bracket_coefficients(s)
    following = b6_bracket_coefficients(s + 1)
    transported = integer_convolution(linear_power(6, 2), current)
    return combine_polynomials((1, following), (-1, transported))


def build_certificate(maximum_s: int = 200) -> dict[str, object]:
    profiles, determinant = derive_six_page_determinant()
    rows: list[list[object]] = []
    for s in range(6, 10):
        pooled = {
            degree: int(coefficient)
            for order, degree, coefficient in pooled_t_newton_rows(
                s, 4 * s - 8
            )
            if order == 6
        }
        formula_coefficients = b6_coefficients(s)
        formula = {
            degree: coefficient
            for degree, coefficient in enumerate(formula_coefficients)
            if coefficient
        }
        if pooled != formula:
            raise AssertionError(f"B6 mismatch at s={s}")
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
    for s in range(7, maximum_s + 1):
        coefficients = b6_bracket_coefficients(s)
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

    payload = json.dumps(rows, separators=(",", ":")).encode("utf-8")
    return {
        "schema": "amra.complete_split.six_page_union.v1",
        "partition_state_count": 203,
        "profile_polynomials_six_pages": [str(value) for value in profiles],
        "six_page_determinant": str(determinant),
        "K6": str(k6_polynomial()),
        "B6_formula": (
            "For s>=8, B6=60 beta^4 lambda^(2s-16) F_s, where "
            "F_s=u6^(2s-14)K6-4lambda^2*u5^(2s-12)K5"
            "+6lambda^4*u4^(2s-10)K4"
            "-4lambda^6*u3^(2s-8)K3+lambda^8*u2^(2s-6)."
        ),
        "boundary_values": {
            "s_lt_6": "0",
            "s6": "1244160*beta^12*(60*beta^2+22*beta+3)",
            "s7": (
                "7200*beta^12*(112001848*beta^6+112001848*beta^5"
                "+50848378*beta^4+13220592*beta^3+2059813*beta^2"
                "+181174*beta+7019)"
            ),
        },
        "pooled_transfer_rows_s6_to_s9": rows,
        "sha256_pooled_rows": hashlib.sha256(payload).hexdigest(),
        "bracket_counterexample_search": {
            "s_range": [7, maximum_s],
            "first_negative": first_negative,
            "all_searched_coefficients_nonnegative": first_negative is None,
            "summaries_s_first_degree_last_degree_minimum": bracket_summaries,
            "sha256_all_lines": digest.hexdigest(),
        },
        "candidate_recurrence_search": {
            "identity": "R_s=F_(s+1)-(1+6beta)^2 F_s",
            "s_range": [7, maximum_s - 1],
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
            "The 203-state determinant and all-s B6 formula are proved. "
            "The coefficient and recurrence scans are finite audits; "
            "uniform B6 positivity is not proved here."
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
