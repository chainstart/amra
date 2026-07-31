#!/usr/bin/env python3
"""Symbolic workbench and certificate for the OPG-1757 q=5 layer."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from functools import lru_cache

import sympy as sp

from audit_sixth_q5_independent import audit_rational_q5_certificate
from verify_fifth_q4 import Q4_ENDPOINT_POLYNOMIALS
from verify_second_deficit import (
    S,
    U,
    cleared_component_degree_bound,
    falling,
    normalized_component_value,
    rational_certificate_point_count,
)


Q5_DEFICIT = 5
Q5_ENDPOINT_SAMPLE_START = 10


def _q5_endpoint_polynomials() -> dict[tuple[int, int, int], sp.Expr]:
    """The 63 inherited endpoints plus 21 new q=5 boundary entries."""

    table = dict(Q4_ENDPOINT_POLYNOMIALS)
    table.update(
        {
            (0, 0, 7): (S - 6)
            * (S - 5)
            * (S - 4)
            * (S - 3)
            * (S - 2)
            * (S - 1)
            * (
                S**6
                + 51 * S**5
                + 1385 * S**4
                + 24885 * S**3
                + 303766 * S**2
                + 2333976 * S
                + 8648640
            )
            / 46080,
            (1, 0, 7): (S - 7)
            * (S - 6)
            * (S - 5)
            * (S - 4)
            * (S - 3)
            * (S - 2)
            * (
                S**6
                + 51 * S**5
                + 1385 * S**4
                + 24885 * S**3
                + 303766 * S**2
                + 2333976 * S
                + 8648640
            )
            / 46080,
            (2, 0, 7): (S - 8)
            * (S - 7)
            * (S - 6)
            * (S - 5)
            * (S - 4)
            * (
                S**7
                + 48 * S**6
                + 1220 * S**5
                + 20160 * S**4
                + 215671 * S**3
                + 1230408 * S**2
                + 12060 * S
                - 32432400
            )
            / 46080,
            (0, 1, 6): (S - 7)
            * (S - 6)
            * (S - 5)
            * (S - 4)
            * (S - 3)
            * (S - 2)
            * (S - 1)
            * (
                3 * S**5
                + 130 * S**4
                + 2865 * S**3
                + 39010 * S**2
                + 319848 * S
                + 1235520
            )
            / 23040,
            (1, 1, 6): (S - 8)
            * (S - 7)
            * (S - 6)
            * (S - 5)
            * (S - 4)
            * (S - 3)
            * (S - 2)
            * (
                3 * S**5
                + 130 * S**4
                + 2865 * S**3
                + 39010 * S**2
                + 319848 * S
                + 1235520
            )
            / 23040,
            (2, 1, 6): (S - 9)
            * (S - 8)
            * (S - 7)
            * (S - 6)
            * (S - 5)
            * (S - 4)
            * (
                3 * S**6
                + 121 * S**5
                + 2445 * S**4
                + 29255 * S**3
                + 182028 * S**2
                + 75676 * S
                - 4564560
            )
            / 23040,
            (0, 2, 5): (S - 7)
            * (S - 6)
            * (S - 5)
            * (S - 4)
            * (S - 3)
            * (S - 2)
            * (S - 1)
            * (
                3 * S**5
                + 86 * S**4
                + 1073 * S**3
                + 4534 * S**2
                - 40288 * S
                - 443520
            )
            / 9216,
            (1, 2, 5): (S - 8)
            * (S - 7)
            * (S - 6)
            * (S - 5)
            * (S - 4)
            * (S - 3)
            * (S - 2)
            * (
                3 * S**5
                + 83 * S**4
                + 967 * S**3
                + 2757 * S**2
                - 56586 * S
                - 510840
            )
            / 9216,
            (2, 2, 5): (S - 9)
            * (S - 8)
            * (S - 7)
            * (S - 6)
            * (S - 5)
            * (S - 4)
            * (
                3 * S**6
                + 71 * S**5
                + 597 * S**4
                - 2103 * S**3
                - 78276 * S**2
                - 327292 * S
                + 2093520
            )
            / 9216,
            (0, 3, 4): (S - 7)
            * (S - 6)
            * (S - 5)
            * (S - 4)
            * (S - 3)
            * (S - 2)
            * (S - 1)
            * (
                45 * S**5
                + 630 * S**4
                - 45 * S**3
                - 62902 * S**2
                - 251776 * S
                + 2597760
            )
            / 103680,
            (1, 3, 4): (S - 8)
            * (S - 7)
            * (S - 6)
            * (S - 5)
            * (S - 4)
            * (S - 3)
            * (S - 2)
            * (
                45 * S**5
                + 540 * S**4
                - 1845 * S**3
                - 73522 * S**2
                - 188486 * S
                + 3478860
            )
            / 103680,
            (2, 3, 4): (S - 9)
            * (S - 8)
            * (S - 7)
            * (S - 6)
            * (S - 5)
            * (S - 4)
            * (
                45 * S**6
                + 315 * S**5
                - 5175 * S**4
                - 71857 * S**3
                + 186360 * S**2
                + 4953796 * S
                - 15810960
            )
            / 103680,
            (0, 4, 3): (S - 7)
            * (S - 6)
            * (S - 5)
            * (S - 4)
            * (S - 3)
            * (S - 2)
            * (S - 1)
            * (
                45 * S**5
                - 30 * S**4
                - 5445 * S**3
                - 3058 * S**2
                + 349808 * S
                - 1117440
            )
            / 138240,
            (1, 4, 3): (S - 8)
            * (S - 7)
            * (S - 6)
            * (S - 5)
            * (S - 4)
            * (S - 3)
            * (S - 2)
            * (
                45 * S**5
                - 165 * S**4
                - 6075 * S**3
                + 10037 * S**2
                + 428350 * S
                - 1759680
            )
            / 138240,
            (2, 4, 3): (S - 9)
            * (S - 8)
            * (S - 7)
            * (S - 6)
            * (S - 5)
            * (S - 4)
            * (
                45 * S**6
                - 435 * S**5
                - 5715 * S**4
                + 48077 * S**3
                + 429156 * S**2
                - 4378388 * S
                + 8849280
            )
            / 138240,
            (0, 5, 2): (S - 7)
            * (S - 6)
            * (S - 5)
            * (S - 4)
            * (S - 3)
            * (S - 2)
            * (S - 1)
            * (
                63 * S**5
                - 966 * S**4
                - 147 * S**3
                + 72898 * S**2
                - 430640 * S
                + 753408
            )
            / 483840,
            (1, 5, 2): (S - 8)
            * (S - 7)
            * (S - 6)
            * (S - 5)
            * (S - 4)
            * (S - 3)
            * (S - 2)
            * (
                63 * S**5
                - 1218 * S**4
                + 2541 * S**3
                + 86170 * S**2
                - 663124 * S
                + 1413648
            )
            / 483840,
            (2, 5, 2): (S - 9)
            * (S - 8)
            * (S - 7)
            * (S - 6)
            * (S - 5)
            * (S - 4)
            * (
                63 * S**6
                - 1659 * S**5
                + 10269 * S**4
                + 81823 * S**3
                - 1294356 * S**2
                + 5569268 * S
                - 7823040
            )
            / 483840,
            (0, 6, 1): (S - 7)
            * (S - 6)
            * (S - 5)
            * (S - 4)
            * (S - 3)
            * (S - 2)
            * (S - 1)
            * (
                63 * S**5
                - 1890 * S**4
                + 22365 * S**3
                - 130186 * S**2
                + 371672 * S
                - 414720
            )
            / 2903040,
            (1, 6, 1): (S - 8)
            * (S - 7)
            * (S - 6)
            * (S - 5)
            * (S - 4)
            * (S - 3)
            * (S - 2)
            * (
                63 * S**5
                - 2205 * S**4
                + 30555 * S**3
                - 209251 * S**2
                + 707014 * S
                - 940896
            )
            / 2903040,
            (2, 6, 1): (S - 9)
            * (S - 8)
            * (S - 7)
            * (S - 6)
            * (S - 5)
            * (S - 4)
            * (S - 3)
            * (
                63 * S**5
                - 2520 * S**4
                + 40005 * S**3
                - 314776 * S**2
                + 1226316 * S
                - 1889984
            )
            / 2903040,
        }
    )
    expected_entries = {
        (h, excess, components)
        for h in range(3)
        for excess in range(7)
        for components in range(1, 8 - excess)
    }
    if set(table) != expected_entries:
        raise AssertionError("q=5 endpoint table is incomplete")
    return {key: sp.cancel(value) for key, value in table.items()}


Q5_ENDPOINT_POLYNOMIALS = _q5_endpoint_polynomials()


def q5_endpoint_entries() -> list[tuple[int, int, int]]:
    return sorted(Q5_ENDPOINT_POLYNOMIALS)


def audit_q5_endpoint_table() -> list[list[object]]:
    """Certify the 84 formulas with exactly 924 endpoint values."""

    rows: list[list[object]] = []
    for h, excess, components in q5_endpoint_entries():
        expected = Q5_ENDPOINT_POLYNOMIALS[
            (h, excess, components)
        ]
        cleared = sp.cancel(S**excess * expected)
        numerator, denominator = sp.fraction(cleared)
        if sp.degree(denominator, S) > 0:
            raise AssertionError("q=5 endpoint retained an s denominator")
        degree_bound = cleared_component_degree_bound(
            excess, components
        )
        if sp.degree(numerator, S) > degree_bound:
            raise AssertionError("q=5 endpoint exceeds the Abel degree bound")
        sample_count = rational_certificate_point_count(
            excess, components
        )
        for sample_s in range(
            Q5_ENDPOINT_SAMPLE_START,
            Q5_ENDPOINT_SAMPLE_START + sample_count,
        ):
            measured = sp.Rational(
                normalized_component_value(
                    sample_s, h, excess, components
                )
            )
            if sp.cancel(expected.subs(S, sample_s) - measured) != 0:
                raise AssertionError(
                    "q=5 endpoint mismatch at "
                    f"{(sample_s, h, excess, components)}"
                )
        rows.append(
            [
                h,
                excess,
                components,
                degree_bound,
                sample_count,
                str(sp.factor(expected)),
            ]
        )
    if len(rows) != 84 or sum(row[4] for row in rows) != 924:
        raise AssertionError(
            "q=5 count firewall failed: full table must be 84/924"
        )
    return rows


@lru_cache(maxsize=None)
def normalized_q5_layer(offset: int) -> sp.Expr:
    """Return [beta^(2*n+r)]B_n/(n!*s^(2*s-18+r))."""

    if offset < 0 or offset > 10:
        raise ValueError("q=5 offset must lie in 0..10")
    total = sp.Integer(0)
    for overlap in range(offset // 2 + 1):
        remaining = offset - 2 * overlap
        lambda_exponent = 6 - overlap
        for left_excess in range(remaining + 1):
            for right_excess in range(
                remaining - left_excess + 1
            ):
                lambda_degree = (
                    remaining - left_excess - right_excess
                )
                if lambda_degree > lambda_exponent:
                    continue
                prefactor = sp.Rational(
                    math.comb(lambda_exponent, lambda_degree),
                    math.factorial(overlap),
                )
                component_sum = (
                    8
                    - overlap
                    - left_excess
                    - right_excess
                )
                for left_components in range(1, component_sum):
                    right_components = (
                        component_sum - left_components
                    )
                    positive = sp.Integer(0)
                    positive_left = (
                        1,
                        left_excess,
                        left_components,
                    )
                    positive_right = (
                        1,
                        right_excess,
                        right_components,
                    )
                    if (
                        positive_left in Q5_ENDPOINT_POLYNOMIALS
                        and positive_right in Q5_ENDPOINT_POLYNOMIALS
                    ):
                        left_order = (
                            S
                            - 1
                            - left_components
                            - left_excess
                        )
                        right_order = (
                            S
                            - 1
                            - right_components
                            - right_excess
                        )
                        positive = (
                            4
                            * falling(left_order, overlap)
                            * falling(right_order, overlap)
                            * Q5_ENDPOINT_POLYNOMIALS[positive_left]
                            * Q5_ENDPOINT_POLYNOMIALS[positive_right]
                        )

                    negative = sp.Integer(0)
                    negative_left = (
                        0,
                        left_excess,
                        left_components,
                    )
                    negative_right = (
                        2,
                        right_excess,
                        right_components,
                    )
                    if (
                        negative_left in Q5_ENDPOINT_POLYNOMIALS
                        and negative_right in Q5_ENDPOINT_POLYNOMIALS
                    ):
                        left_order = (
                            S - left_components - left_excess
                        )
                        right_order = (
                            S
                            - 2
                            - right_components
                            - right_excess
                        )
                        negative = (
                            4
                            * falling(left_order, overlap)
                            * falling(right_order, overlap)
                            * Q5_ENDPOINT_POLYNOMIALS[negative_left]
                            * Q5_ENDPOINT_POLYNOMIALS[negative_right]
                        )
                    total += prefactor * (positive - negative)
    return sp.factor(sp.cancel(total))


EXPECTED_Q5_NORMALIZED_LAYERS = (
    sp.Rational(1, 30)
    * (S - 5)
    * (S - 4)
    * (
        S**8
        + 29 * S**7
        + 321 * S**6
        + 459 * S**5
        - 23239 * S**4
        - 161291 * S**3
        + 565356 * S**2
        + 5972364 * S
        - 18174240
    ),
    sp.Rational(1, 9)
    * (S - 5)
    * (S - 4)
    * (
        3 * S**8
        + 68 * S**7
        + 504 * S**6
        - 1638 * S**5
        - 45762 * S**4
        - 122342 * S**3
        + 1328907 * S**2
        + 3955734 * S
        - 18174240
    ),
    sp.Rational(1, 18)
    * (S - 5)
    * (S - 4)
    * (
        30 * S**8
        + 489 * S**7
        + 1507 * S**6
        - 27821 * S**5
        - 221251 * S**4
        + 486683 * S**3
        + 6647577 * S**2
        - 10477962 * S
        - 22921920
    ),
    sp.Rational(4, 45)
    * (S - 5)
    * (S - 4)
    * (
        60 * S**8
        + 600 * S**7
        - 1660 * S**6
        - 47888 * S**5
        - 67659 * S**4
        + 1513961 * S**3
        + 1517269 * S**2
        - 20404086 * S
        + 21846888
    ),
    sp.Rational(1, 45)
    * (S - 5)
    * (S - 4)
    * (
        540 * S**8
        + 2040 * S**7
        - 35935 * S**6
        - 208854 * S**5
        + 1192098 * S**4
        + 6034869 * S**3
        - 29097509 * S**2
        - 883302 * S
        + 73389888
    ),
    sp.Rational(2, 45)
    * (S - 5)
    * (S - 4)
    * (
        444 * S**8
        - 1044 * S**7
        - 29951 * S**6
        + 35449 * S**5
        + 1048166 * S**4
        - 2139865 * S**3
        - 11917920 * S**2
        + 40844052 * S
        - 29418336
    ),
    sp.Rational(1, 9)
    * (S - 5)
    * (S - 4)
    * (2 * S - 11)
    * (
        108 * S**7
        - 312 * S**6
        - 5189 * S**5
        + 13371 * S**4
        + 106278 * S**3
        - 396539 * S**2
        + 84492 * S
        + 609444
    ),
    sp.Rational(4, 9)
    * (S - 5)
    * (S - 4)
    * (2 * S - 11)
    * (2 * S - 9)
    * (
        12 * S**6
        - 52 * S**5
        - 365 * S**4
        + 1758 * S**3
        + 2151 * S**2
        - 16288 * S
        + 15300
    ),
    sp.Rational(1, 90)
    * (S - 5)
    * (S - 4)
    * (2 * S - 11)
    * (2 * S - 9)
    * (
        300 * S**6
        - 3060 * S**5
        + 4025 * S**4
        + 50419 * S**3
        - 194938 * S**2
        + 175488 * S
        + 64656
    ),
    sp.Rational(1, 45)
    * (S - 5)
    * (S - 4)
    * (2 * S - 11)
    * (2 * S - 9)
    * (2 * S - 7)
    * (S**2 - S - 8)
    * (30 * S**3 - 345 * S**2 + 1255 * S - 1398),
    sp.Rational(1, 90)
    * (S - 5)
    * (S - 4) ** 2
    * (S - 3)
    * (2 * S - 11)
    * (2 * S - 9)
    * (2 * S - 7)
    * (12 * S**3 - 136 * S**2 + 469 * S - 446),
)


def audit_symbolic_q5_layers() -> list[list[object]]:
    """Check all eleven formulas, boundary factors, and signs at s>=6."""

    rows: list[list[object]] = []
    for offset, expected in enumerate(EXPECTED_Q5_NORMALIZED_LAYERS):
        measured = normalized_q5_layer(offset)
        expected = sp.factor(expected)
        if sp.cancel(measured - expected) != 0:
            raise AssertionError(
                f"q=5 symbolic layer mismatch at offset {offset}"
            )
        numerator, denominator = sp.fraction(sp.cancel(measured))
        if sp.degree(denominator, S) > 0:
            raise AssertionError(
                f"q=5 denominator did not cancel at offset {offset}"
            )
        if sp.rem(numerator, (S - 4) * (S - 5), domain=sp.QQ) != 0:
            raise AssertionError(
                f"q=5 boundary factor failed at offset {offset}"
            )
        cleared_coefficient = sp.expand(S**offset * measured)
        if (
            sp.degree(cleared_coefficient, S)
            > 2 * Q5_DEFICIT + offset + 2
        ):
            raise AssertionError(
                f"q=5 coefficient degree bound failed at {offset}"
            )
        shifted = sp.Poly(sp.expand(expected.subs(S, U + 6)), U)
        increasing_coefficients = list(reversed(shifted.all_coeffs()))
        if any(coefficient <= 0 for coefficient in increasing_coefficients):
            raise AssertionError(
                f"q=5 shifted positivity failed at offset {offset}"
            )
        rows.append(
            [
                offset,
                str(expected),
                [str(value) for value in increasing_coefficients],
            ]
        )
    return rows


def q5_coefficients(s: int) -> dict[int, int]:
    """The complete eleven coefficients of B_(2*s-10), for s>=5."""

    if s < 5:
        raise ValueError("q=5 has nonnegative depth only for s>=5")
    depth = 2 * s - 10
    result: dict[int, int] = {}
    for offset, polynomial in enumerate(
        EXPECTED_Q5_NORMALIZED_LAYERS
    ):
        value = sp.cancel(
            sp.factorial(depth)
            * sp.Integer(s) ** (2 * s - 18 + offset)
            * polynomial.subs(S, s)
        )
        if not value.is_Integer:
            raise AssertionError("q=5 coefficient formula was fractional")
        if value:
            result[4 * s - 20 + offset] = int(value)
    return result


def audit_independent_q5_coefficients() -> int:
    """Run the boundary-factor-reduced 176-point primitive certificate."""

    rows = audit_rational_q5_certificate(6)
    if len(rows) != 176:
        raise AssertionError("independent q=5 point count changed")
    return len(rows)


def build_certificate() -> dict[str, object]:
    endpoint_rows = audit_q5_endpoint_table()
    symbolic_rows = audit_symbolic_q5_layers()
    independent_coefficient_points = (
        audit_independent_q5_coefficients()
    )
    payload = json.dumps(
        [
            endpoint_rows,
            symbolic_rows,
            independent_coefficient_points,
        ],
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return {
        "schema": "amra.opg1757.sixth_attack_q5.v1",
        "status": "PASS",
        "theorem_status": "PROVED",
        "proved_layer": (
            "B_(2s-10)=0 at s=5 and is coefficientwise strictly "
            "positive for every integer s>=6"
        ),
        "exact_formula": (
            "B_(2s-10)=(2s-10)!*s^(2s-18)*beta^(4s-20)"
            "*sum_(r=0)^10 s^r*P_r(s)*beta^r"
        ),
        "endpoint_formulas": endpoint_rows,
        "endpoint_count": len(endpoint_rows),
        "denominator_aware_endpoint_values": sum(
            row[4] for row in endpoint_rows
        ),
        "endpoint_s_range": [
            Q5_ENDPOINT_SAMPLE_START,
            max(
                Q5_ENDPOINT_SAMPLE_START + row[4] - 1
                for row in endpoint_rows
            ),
        ],
        "count_firewall": {
            "full": "84 endpoints / 924 values",
            "top_face_optimized": "81 endpoints / 867 values",
            "forbidden_mixture": "81 endpoints / 924 values",
        },
        "normalized_layers": symbolic_rows,
        "offset_count": len(symbolic_rows),
        "overlap_orders": [0, 1, 2, 3, 4, 5],
        "boundary_factor": "(s-4)*(s-5)",
        "independent_coefficient_values": (
            independent_coefficient_points
        ),
        "independent_coefficient_s_range": [6, 26],
        "boundary": "B_0(5,beta)=0",
        "scope_firewall": (
            "This proves only q=5 for the complete-split pooled layer. "
            "It does not prove arbitrary fixed q positivity, all B_n, "
            "or arbitrary-host OPG-1757."
        ),
        "sha256": hashlib.sha256(payload).hexdigest(),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.parse_args()
    print(json.dumps(build_certificate(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
