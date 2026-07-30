#!/usr/bin/env python3
"""Symbolic regression for the coefficientwise B4 positivity proof.

It verifies four exact reductions:

* the explicit binomial formula for every coefficient of the B4 bracket;
* the first nonzero coefficient formula;
* failure of the tempting geometric-mean/AM-GM strengthening.
* the positive s-recurrence decomposition proving the remaining lemma.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path

from fixed_page_union_formula import (
    b4_bracket_coefficients,
    integer_convolution,
    linear_power,
)


def choose(n: int, k: int) -> int:
    return math.comb(n, k) if 0 <= k <= n else 0


def powered_choose(n: int, k: int, base: int) -> int:
    return choose(n, k) * base**k if 0 <= k <= n else 0


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


def bracket_coefficient_formula(s: int, degree: int) -> int:
    """Closed three-sum formula for [beta^degree] L_s^(4)."""

    if s < 5:
        raise ValueError("s must be at least 5")
    m = 2 * s - 10
    positive_four = sum(
        coefficient
        * powered_choose(m, degree - order, 4)
        for order, coefficient in enumerate(k4_coefficients(s))
    )
    negative_three = 0
    for lambda_degree in range(3):
        lambda_coefficient = choose(2, lambda_degree) * s**lambda_degree
        negative_three += lambda_coefficient * sum(
            coefficient
            * powered_choose(
                m + 2,
                degree - lambda_degree - order,
                3,
            )
            for order, coefficient in enumerate(k3_coefficients(s))
        )
    positive_two = sum(
        choose(4, lambda_degree)
        * s**lambda_degree
        * powered_choose(m + 4, degree - lambda_degree, 2)
        for lambda_degree in range(5)
    )
    return positive_four - 2 * negative_three + positive_two


def amgm_gap_coefficients(s: int) -> list[int]:
    """Coefficients of A*C-B^2 for the failed AM-GM strengthening."""

    m = 2 * s - 10
    a = integer_convolution(
        linear_power(4, m), k4_coefficients(s)
    )
    b = integer_convolution(
        integer_convolution(linear_power(s, 2), linear_power(3, m + 2)),
        k3_coefficients(s),
    )
    c = integer_convolution(
        linear_power(s, 4), linear_power(2, m + 4)
    )
    ac = integer_convolution(a, c)
    bb = integer_convolution(b, b)
    maximum = max(len(ac), len(bb))
    return [
        (ac[degree] if degree < len(ac) else 0)
        - (bb[degree] if degree < len(bb) else 0)
        for degree in range(maximum)
    ]


def add_polynomials(left: list[int], right: list[int]) -> list[int]:
    maximum = max(len(left), len(right))
    return [
        (left[index] if index < len(left) else 0)
        + (right[index] if index < len(right) else 0)
        for index in range(maximum)
    ]


def scale_polynomial(coefficients: list[int], scalar: int) -> list[int]:
    return [scalar * coefficient for coefficient in coefficients]


def shift_polynomial(coefficients: list[int], degree: int) -> list[int]:
    return [0] * degree + coefficients


def trim_polynomial(coefficients: list[int]) -> list[int]:
    while len(coefficients) > 1 and coefficients[-1] == 0:
        coefficients.pop()
    return coefficients


def positive_recurrence_components(
    s: int,
) -> tuple[list[int], list[int], list[int]]:
    """Return D/beta^2, Q/beta^2, and I/(2 beta^4).

    Here n=s-5, D=K4_{s+1}-K4_s,
    Q=D+2 H3, and I is the merged r=0,1,2 layer in the proof.
    Every displayed coefficient is a polynomial in n with nonnegative
    integer coefficients, so all three returned beta-polynomials are
    coefficientwise nonnegative for every s>=5.
    """

    if s < 5:
        raise ValueError("s must be at least 5")
    n = s - 5
    d_bar = [
        14,
        292,
        150 * n + 2743,
        8 * (242 * n + 1839),
        32 * (15 * n**2 + 357 * n + 1511),
        1024 * (3 * n**2 + 33 * n + 91),
        128 * (2 * n + 11) * (2 * n**2 + 22 * n + 61),
    ]
    q_bar = [
        2 * (2 * n + 5),
        4 * (n**2 + 17 * n + 47),
        74 * n**2 + 646 * n + 1695,
        8 * (3 * n**3 + 76 * n**2 + 490 * n + 1145),
        4 * (49 * n**3 + 718 * n**2 + 3880 * n + 7819),
        8 * (
            3 * n**4
            + 94 * n**3
            + 1020 * n**2
            + 4728 * n
            + 8044
        ),
        4 * (
            21 * n**4
            + 440 * n**3
            + 3480 * n**2
            + 12320 * n
            + 16480
        ),
    ]
    i_bar = [
        (n + 7) * (2 * n**2 + 22 * n + 27),
        2 * (n**4 + 32 * n**3 + 601 * n**2 + 2130 * n + 1974),
        76 * n**4 + 1429 * n**3 + 15241 * n**2 + 42266 * n + 35086,
        4
        * (
            6 * n**5
            + 201 * n**4
            + 3462 * n**3
            + 25238 * n**2
            + 57629 * n
            + 42843
        ),
        2
        * (
            110 * n**5
            + 2828 * n**4
            + 36819 * n**3
            + 194748 * n**2
            + 371397 * n
            + 245175
        ),
        8
        * (
            3 * n**6
            + 115 * n**5
            + 2802 * n**4
            + 26849 * n**3
            + 107106 * n**2
            + 170502 * n
            + 98430
        ),
        2
        * (
            42 * n**6
            + 1795 * n**5
            + 24517 * n**4
            + 150304 * n**3
            + 439416 * n**2
            + 568736 * n
            + 279360
        ),
    ]
    return d_bar, q_bar, i_bar


def recurrence_remainder_direct(s: int) -> list[int]:
    """Coefficients of R_s=L_{s+1}-(1+4 beta)^2 L_s."""

    current = b4_bracket_coefficients(s)
    following = b4_bracket_coefficients(s + 1)
    transported = integer_convolution(linear_power(4, 2), current)
    maximum = max(len(following), len(transported))
    return trim_polynomial(
        [
            (following[index] if index < len(following) else 0)
            - (transported[index] if index < len(transported) else 0)
            for index in range(maximum)
        ]
    )


def recurrence_remainder_positive_decomposition(s: int) -> list[int]:
    """Reconstruct R_s from its manifestly positive z=1+2 beta layers."""

    if s < 5:
        raise ValueError("s must be at least 5")
    m = 2 * s - 10
    d_bar, q_bar, i_bar = positive_recurrence_components(s)
    # I=2 beta^4 i_bar and the merged initial contribution is z^m I.
    result = integer_convolution(
        linear_power(2, m),
        shift_polynomial(scale_polynomial(i_bar, 2), 4),
    )
    # For r>=3, A_r=Q+(2^r-1)D.  Since
    # D=beta^2*d_bar and Q=beta^2*q_bar, each layer is positive.
    for r in range(3, m + 3):
        a_bar = add_polynomials(
            q_bar,
            scale_polynomial(d_bar, 2**r - 1),
        )
        layer = integer_convolution(
            linear_power(2, m + 2 - r),
            shift_polynomial(
                scale_polynomial(a_bar, choose(m + 2, r)),
                r + 2,
            ),
        )
        result = add_polynomials(result, layer)
    return trim_polynomial(result)


def build_audit(maximum_s: int = 30) -> dict[str, object]:
    rows: list[list[object]] = []
    for s in range(5, maximum_s + 1):
        direct = b4_bracket_coefficients(s)
        reconstructed = [
            bracket_coefficient_formula(s, degree)
            for degree in range(len(direct))
        ]
        if direct != reconstructed:
            raise AssertionError(f"coefficient formula mismatch at s={s}")
        first = bracket_coefficient_formula(s, 4)
        expected_first = (
            (s - 4) * (s**3 + 6 * s**2 - 10 * s - 141)
        )
        if first != expected_first:
            raise AssertionError(f"first coefficient mismatch at s={s}")
        recurrence_direct = recurrence_remainder_direct(s)
        recurrence_positive = recurrence_remainder_positive_decomposition(s)
        if recurrence_direct != recurrence_positive:
            raise AssertionError(f"positive recurrence mismatch at s={s}")
        if not all(value >= 0 for value in recurrence_positive):
            raise AssertionError(f"negative recurrence coefficient at s={s}")
        rows.append([s, str(first), len([value for value in direct if value])])

    base = b4_bracket_coefficients(5)
    expected_base = shift_polynomial(
        scale_polynomial(
            integer_convolution(
                linear_power(5, 2),
                [7, 40, 75],
            ),
            12,
        ),
        4,
    )
    if base != expected_base:
        raise AssertionError("the positive s=5 base formula changed")

    gap = amgm_gap_coefficients(5)
    if gap[4] != -60:
        raise AssertionError("the AM-GM no-go coefficient changed")
    payload = json.dumps(rows, separators=(",", ":")).encode("utf-8")
    return {
        "schema": "amra.complete_split.b4_uniform_positivity_audit.v2",
        "theorem": (
            "For every integer s>=5, L_s is coefficientwise nonnegative. "
            "Hence B4>=0 for beta>=0."
        ),
        "positive_recurrence": (
            "L_(s+1)=(1+4beta)^2 L_s+R_s; after z=1+2beta, "
            "R_s=z^(2s-10) I_s + sum_(r=3)^(2s-8) "
            "C(2s-8,r) beta^r z^(2s-8-r) A_(s,r), "
            "where I_s=2beta^4 i_(s-5), "
            "A_(s,r)=beta^2(q_(s-5)+(2^r-1)d_(s-5)), "
            "and every coefficient of i,q,d in beta and n=s-5 is "
            "a nonnegative integer."
        ),
        "positive_base": "L_5=12beta^4(1+5beta)^2(7+40beta+75beta^2)",
        "amgm_strengthening_failure": {
            "attempt": "A*C>=B^2, which would imply A-2B+C>=0",
            "minimal_checked_parameters": {"s": 5, "beta_degree": 4},
            "exact_coefficient": "-60",
        },
        "first_nonzero_coefficient": (
            "(s-4)*(s^3+6s^2-10s-141), positive for s>=5"
        ),
        "regression_rows_s_first_coefficient_nonzero_count": rows,
        "sha256_rows": hashlib.sha256(payload).hexdigest(),
        "status": "proved by a manifestly coefficientwise positive s-recurrence",
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--maximum-s", type=int, default=30)
    parser.add_argument("--output", type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    audit = build_audit(args.maximum_s)
    rendered = json.dumps(audit, indent=2, sort_keys=True)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + "\n", encoding="utf-8")
        print(f"wrote {args.output}")
    else:
        print(rendered)


if __name__ == "__main__":
    main()
