#!/usr/bin/env python3
"""Exact symbolic certificate for the OPG-1757 q=4 pooled layer.

For ``n=2*s-9`` this verifier checks 63 endpoint formulas at the 588 exact
values required by the denominator-aware Abel lemma, assembles all nine
beta offsets, proves their signs, and invokes an independent 135-value
primitive-transfer certificate for the final rational identities.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from functools import lru_cache

import sympy as sp

from audit_fifth_q4_independent import audit_rational_q4_certificate
from verify_fourth_q3 import Q3_ENDPOINT_POLYNOMIALS
from verify_second_deficit import (
    S,
    U,
    cleared_component_degree_bound,
    falling,
    normalized_component_value,
    rational_certificate_point_count,
)


Q4_DEFICIT = 4
Q4_ENDPOINT_SAMPLE_START = 9
Q4_COEFFICIENT_SAMPLE_START = 6


def _q4_endpoint_polynomials() -> dict[tuple[int, int, int], sp.Expr]:
    """The 45 inherited endpoints plus 18 new q=4 boundary entries."""

    table = dict(Q3_ENDPOINT_POLYNOMIALS)
    table.update(
        {
            (0, 0, 6): (S - 5)
            * (S - 4)
            * (S - 3)
            * (S - 2)
            * (S - 1)
            * (
                S**5
                + 40 * S**4
                + 835 * S**3
                + 10960 * S**2
                + 87636 * S
                + 332640
            )
            / 3840,
            (1, 0, 6): (S - 6)
            * (S - 5)
            * (S - 4)
            * (S - 3)
            * (S - 2)
            * (
                S**5
                + 40 * S**4
                + 835 * S**3
                + 10960 * S**2
                + 87636 * S
                + 332640
            )
            / 3840,
            (2, 0, 6): (S - 7)
            * (S - 6)
            * (S - 5)
            * (S - 4)
            * (
                S**6
                + 37 * S**5
                + 705 * S**4
                + 8095 * S**3
                + 48626 * S**2
                + 12792 * S
                - 1235520
            )
            / 3840,
            (0, 1, 5): (S - 6)
            * (S - 5)
            * (S - 4)
            * (S - 3)
            * (S - 2)
            * (S - 1)
            * (
                3 * S**4
                + 98 * S**3
                + 1557 * S**2
                + 13766 * S
                + 55440
            )
            / 2304,
            (1, 1, 5): (S - 7)
            * (S - 6)
            * (S - 5)
            * (S - 4)
            * (S - 3)
            * (S - 2)
            * (
                3 * S**4
                + 98 * S**3
                + 1557 * S**2
                + 13766 * S
                + 55440
            )
            / 2304,
            (2, 1, 5): (S - 8)
            * (S - 7)
            * (S - 6)
            * (S - 5)
            * (S - 4)
            * (
                3 * S**5
                + 89 * S**4
                + 1239 * S**3
                + 8435 * S**2
                + 6546 * S
                - 201960
            )
            / 2304,
            (0, 2, 4): (S - 6)
            * (S - 5)
            * (S - 4)
            * (S - 3)
            * (S - 2)
            * (S - 1)
            * (
                3 * S**4
                + 58 * S**3
                + 383 * S**2
                - 928 * S
                - 20160
            )
            / 1152,
            (1, 2, 4): (S - 7)
            * (S - 6)
            * (S - 5)
            * (S - 4)
            * (S - 3)
            * (S - 2)
            * (
                3 * S**4
                + 55 * S**3
                + 308 * S**2
                - 1734 * S
                - 23760
            )
            / 1152,
            (2, 2, 4): (S - 8)
            * (S - 7)
            * (S - 6)
            * (S - 5)
            * (S - 4)
            * (
                3 * S**5
                + 43 * S**4
                + 59 * S**3
                - 3437 * S**2
                - 19132 * S
                + 97020
            )
            / 1152,
            (0, 3, 3): (S - 6)
            * (S - 5)
            * (S - 4)
            * (S - 3)
            * (S - 2)
            * (S - 1)
            * (
                15 * S**4
                + 90 * S**3
                - 945 * S**2
                - 7556 * S
                + 40544
            )
            / 5760,
            (1, 3, 3): (S - 7)
            * (S - 6)
            * (S - 5)
            * (S - 4)
            * (S - 3)
            * (S - 2)
            * (
                5 * S**4
                + 20 * S**3
                - 425 * S**2
                - 2432 * S
                + 19008
            )
            / 1920,
            (2, 3, 3): (S - 8)
            * (S - 7)
            * (S - 6)
            * (S - 5)
            * (S - 4)
            * (
                15 * S**5
                - 15 * S**4
                - 1725 * S**3
                - 1471 * S**2
                + 101012 * S
                - 260460
            )
            / 5760,
            (0, 4, 2): (S - 6)
            * (S - 5)
            * (S - 4)
            * (S - 3)
            * (S - 2)
            * (S - 1)
            * (
                15 * S**4
                - 110 * S**3
                - 795 * S**2
                + 8546 * S
                - 18368
            )
            / 11520,
            (1, 4, 2): (S - 7)
            * (S - 6)
            * (S - 5)
            * (S - 4)
            * (S - 3)
            * (S - 2)
            * (
                15 * S**4
                - 155 * S**3
                - 660 * S**2
                + 11536 * S
                - 31296
            )
            / 11520,
            (2, 4, 2): (S - 8)
            * (S - 7)
            * (S - 6)
            * (S - 5)
            * (S - 4)
            * (
                15 * S**5
                - 245 * S**4
                + 135 * S**3
                + 16701 * S**2
                - 98142 * S
                + 158976
            )
            / 11520,
            (0, 5, 1): (S - 6) ** 2
            * (S - 5) ** 2
            * (S - 4)
            * (S - 3)
            * (S - 2)
            * (S - 1)
            * (3 * S**2 - 29 * S + 64)
            / 11520,
            (1, 5, 1): (S - 7) ** 2
            * (S - 6) ** 2
            * (S - 5)
            * (S - 4)
            * (S - 3)
            * (S - 2)
            * (3 * S**2 - 35 * S + 96)
            / 11520,
            (2, 5, 1): (S - 8) ** 2
            * (S - 7) ** 2
            * (S - 6)
            * (S - 5)
            * (S - 4)
            * (S - 3)
            * (3 * S**2 - 41 * S + 134)
            / 11520,
        }
    )
    expected_entries = {
        (h, excess, components)
        for h in range(3)
        for excess in range(6)
        for components in range(1, 7 - excess)
    }
    if set(table) != expected_entries:
        raise AssertionError("q=4 endpoint table is incomplete")
    return {key: sp.cancel(value) for key, value in table.items()}


Q4_ENDPOINT_POLYNOMIALS = _q4_endpoint_polynomials()


def q4_endpoint_entries() -> list[tuple[int, int, int]]:
    return sorted(Q4_ENDPOINT_POLYNOMIALS)


def audit_q4_endpoint_table() -> list[list[object]]:
    """Certify the 63 formulas with exactly 588 endpoint values."""

    rows: list[list[object]] = []
    for h, excess, components in q4_endpoint_entries():
        expected = Q4_ENDPOINT_POLYNOMIALS[
            (h, excess, components)
        ]
        cleared = sp.cancel(S**excess * expected)
        numerator, denominator = sp.fraction(cleared)
        if sp.degree(denominator, S) > 0:
            raise AssertionError("q=4 endpoint retained an s denominator")
        degree_bound = cleared_component_degree_bound(
            excess, components
        )
        if sp.degree(numerator, S) > degree_bound:
            raise AssertionError("q=4 endpoint exceeds the Abel degree bound")
        sample_count = rational_certificate_point_count(
            excess, components
        )
        for sample_s in range(
            Q4_ENDPOINT_SAMPLE_START,
            Q4_ENDPOINT_SAMPLE_START + sample_count,
        ):
            measured = sp.Rational(
                normalized_component_value(
                    sample_s, h, excess, components
                )
            )
            if sp.cancel(expected.subs(S, sample_s) - measured) != 0:
                raise AssertionError(
                    "q=4 endpoint mismatch at "
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
    if len(rows) != 63 or sum(row[4] for row in rows) != 588:
        raise AssertionError("q=4 endpoint certificate size changed")
    return rows


@lru_cache(maxsize=None)
def normalized_q4_layer(offset: int) -> sp.Expr:
    """Return [beta^(2*n+r)]B_n/(n!*s^(2*s-16+r))."""

    if offset < 0 or offset > 8:
        raise ValueError("q=4 offset must lie in 0..8")
    total = sp.Integer(0)
    for overlap in range(offset // 2 + 1):
        remaining = offset - 2 * overlap
        lambda_exponent = 5 - overlap
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
                    7
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
                        positive_left in Q4_ENDPOINT_POLYNOMIALS
                        and positive_right in Q4_ENDPOINT_POLYNOMIALS
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
                            * Q4_ENDPOINT_POLYNOMIALS[positive_left]
                            * Q4_ENDPOINT_POLYNOMIALS[positive_right]
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
                        negative_left in Q4_ENDPOINT_POLYNOMIALS
                        and negative_right in Q4_ENDPOINT_POLYNOMIALS
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
                            * Q4_ENDPOINT_POLYNOMIALS[negative_left]
                            * Q4_ENDPOINT_POLYNOMIALS[negative_right]
                        )
                    total += prefactor * (positive - negative)
    return sp.factor(sp.cancel(total))


EXPECTED_Q4_NORMALIZED_LAYERS = (
    sp.Rational(1, 6)
    * (S - 5)
    * (S - 4)
    * (
        S**6
        + 25 * S**5
        + 229 * S**4
        + 211 * S**3
        - 10101 * S**2
        - 36081 * S
        + 183330
    ),
    sp.Rational(4, 3)
    * (S - 5)
    * (S - 4)
    * (
        S**6
        + 19 * S**5
        + 111 * S**4
        - 321 * S**3
        - 5409 * S**2
        - 3867 * S
        + 61110
    ),
    sp.Rational(2, 9)
    * (S - 5)
    * (S - 4)
    * (
        24 * S**6
        + 312 * S**5
        + 565 * S**4
        - 11427 * S**3
        - 42073 * S**2
        + 165669 * S
        + 98280
    ),
    sp.Rational(4, 15)
    * (S - 5)
    * (S - 4)
    * (
        50 * S**6
        + 355 * S**5
        - 1420 * S**4
        - 16156 * S**3
        + 21221 * S**2
        + 186954 * S
        - 305424
    ),
    sp.Rational(1, 3)
    * (S - 5)
    * (S - 4)
    * (
        68 * S**6
        + 88 * S**5
        - 3185 * S**4
        - 3446 * S**3
        + 64500 * S**2
        - 77429 * S
        - 68112
    ),
    sp.Rational(4, 9)
    * (S - 5)
    * (S - 4)
    * (
        60 * S**6
        - 264 * S**5
        - 1967 * S**4
        + 10074 * S**3
        + 10232 * S**2
        - 96345 * S
        + 103680
    ),
    sp.Rational(8, 3)
    * (S - 5)
    * (S - 4)
    * (2 * S - 9)
    * (
        4 * S**5
        - 22 * S**4
        - 54 * S**3
        + 489 * S**2
        - 704 * S
        - 18
    ),
    sp.Rational(4, 3)
    * (S - 5)
    * (S - 4)
    * (2 * S - 9)
    * (2 * S - 7)
    * (S**2 - S - 8)
    * (2 * S**2 - 13 * S + 19),
    sp.Rational(1, 90)
    * (S - 5)
    * (S - 4)
    * (S - 3)
    * (2 * S - 9)
    * (2 * S - 7)
    * (
        60 * S**3
        - 600 * S**2
        + 1865 * S
        - 1706
    ),
)


def audit_symbolic_q4_layers() -> list[list[object]]:
    """Check all nine formulas, degree bounds, and shifted signs."""

    rows: list[list[object]] = []
    for offset, expected in enumerate(EXPECTED_Q4_NORMALIZED_LAYERS):
        measured = normalized_q4_layer(offset)
        expected = sp.factor(expected)
        if sp.cancel(measured - expected) != 0:
            raise AssertionError(
                f"q=4 symbolic layer mismatch at offset {offset}"
            )
        numerator, denominator = sp.fraction(sp.cancel(measured))
        if sp.degree(denominator, S) > 0:
            raise AssertionError(
                f"q=4 denominator did not cancel at offset {offset}"
            )
        cleared_coefficient = sp.expand(S**offset * measured)
        if (
            sp.degree(cleared_coefficient, S)
            > 2 * Q4_DEFICIT + offset + 2
        ):
            raise AssertionError(
                f"q=4 coefficient degree bound failed at {offset}"
            )
        shifted = sp.Poly(sp.expand(expected.subs(S, U + 5)), U)
        increasing_coefficients = list(reversed(shifted.all_coeffs()))
        if increasing_coefficients[0] != 0:
            raise AssertionError("q=4 boundary s=5 did not vanish")
        if any(
            coefficient <= 0
            for coefficient in increasing_coefficients[1:]
        ):
            raise AssertionError(
                f"q=4 shifted positivity failed at offset {offset}"
            )
        rows.append(
            [
                offset,
                str(expected),
                [str(value) for value in increasing_coefficients],
            ]
        )
    return rows


def q4_coefficients(s: int) -> dict[int, int]:
    """The complete nine coefficients of B_(2*s-9), for s>=5."""

    if s < 5:
        raise ValueError("q=4 has nonnegative depth only for s>=5")
    depth = 2 * s - 9
    result: dict[int, int] = {}
    for offset, polynomial in enumerate(
        EXPECTED_Q4_NORMALIZED_LAYERS
    ):
        value = sp.cancel(
            sp.factorial(depth)
            * sp.Integer(s) ** (2 * s - 16 + offset)
            * polynomial.subs(S, s)
        )
        if not value.is_Integer:
            raise AssertionError("q=4 coefficient formula was fractional")
        if value:
            result[4 * s - 18 + offset] = int(value)
    return result


def audit_independent_q4_coefficients() -> int:
    """Run the exact 135-point primitive rational certificate."""

    rows = audit_rational_q4_certificate(
        Q4_COEFFICIENT_SAMPLE_START
    )
    if len(rows) != 135:
        raise AssertionError("independent q=4 point count changed")
    return len(rows)


def build_certificate() -> dict[str, object]:
    endpoint_rows = audit_q4_endpoint_table()
    symbolic_rows = audit_symbolic_q4_layers()
    independent_coefficient_points = (
        audit_independent_q4_coefficients()
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
        "schema": "amra.opg1757.fifth_attack_q4.v1",
        "status": "PASS",
        "theorem_status": "PROVED",
        "proved_layer": (
            "B_(2s-9)=0 at s=5 and is coefficientwise strictly "
            "positive for every integer s>=6"
        ),
        "exact_formula": (
            "B_(2s-9)=(2s-9)!*s^(2s-16)*beta^(4s-18)"
            "*sum_(r=0)^8 s^r*P_r(s)*beta^r"
        ),
        "endpoint_formulas": endpoint_rows,
        "endpoint_count": len(endpoint_rows),
        "denominator_aware_endpoint_values": sum(
            row[4] for row in endpoint_rows
        ),
        "endpoint_s_range": [
            Q4_ENDPOINT_SAMPLE_START,
            max(
                Q4_ENDPOINT_SAMPLE_START + row[4] - 1
                for row in endpoint_rows
            ),
        ],
        "normalized_layers": symbolic_rows,
        "offset_count": len(symbolic_rows),
        "overlap_orders": [0, 1, 2, 3, 4],
        "independent_coefficient_values": (
            independent_coefficient_points
        ),
        "independent_coefficient_s_range": [6, 24],
        "boundary": "B_1(5,beta)=0",
        "scope_firewall": (
            "This proves only q=4 for the complete-split pooled layer. "
            "It does not prove arbitrary fixed q, all B_n, or arbitrary "
            "host OPG-1757."
        ),
        "sha256": hashlib.sha256(payload).hexdigest(),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.parse_args()
    print(json.dumps(build_certificate(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
