#!/usr/bin/env python3
"""Exact symbolic certificate for the OPG-1757 q=3 pooled layer.

For ``n=2*s-8`` this verifier:

* checks all 45 hyperforest endpoints at the 345 values required by the
  denominator-aware Abel bound;
* checks the same 345 values with a direct-position implementation whose
  forest evaluator is independent of the main equal-weight aggregation;
* substitutes the endpoints into the exact overlap/excess formula;
* derives and factors all seven beta-offset coefficients;
* proves their signs by shifting ``s=u+5``;
* compares the complete layer with the earlier primitive pooled transfer.

Finite values certify endpoint identities because

    s**e H_(h,e,c)/(2**h s**(s-h-2c-e))

is already proved to be a polynomial of degree at most ``2*c+3*e-2``.
The verifier therefore does not infer an all-s theorem from an unproved
interpolation premise.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from functools import lru_cache

import sympy as sp

from audit_fourth_q3_independent import (
    audit_primitive_q3,
    independent_endpoint_certificate,
)
from verify_second_deficit import (
    COMPONENT_POLYNOMIALS,
    S,
    U,
    cleared_component_degree_bound,
    falling,
    normalized_component_value,
    rational_certificate_point_count,
)


Q3_DEFICIT = 3
Q3_ENDPOINT_SAMPLE_START = 8


def _q3_endpoint_polynomials() -> dict[tuple[int, int, int], sp.Expr]:
    """The 30 inherited endpoints plus the 15 new q=3 boundary entries."""

    table = dict(COMPONENT_POLYNOMIALS)
    table.update(
        {
            (0, 0, 5): (S - 4)
            * (S - 3)
            * (S - 2)
            * (S - 1)
            * (
                S**4
                + 30 * S**3
                + 451 * S**2
                + 3846 * S
                + 15120
            )
            / 384,
            (1, 0, 5): (S - 5)
            * (S - 4)
            * (S - 3)
            * (S - 2)
            * (
                S**4
                + 30 * S**3
                + 451 * S**2
                + 3846 * S
                + 15120
            )
            / 384,
            (2, 0, 5): (S - 6)
            * (S - 5)
            * (S - 4)
            * (
                S**5
                + 27 * S**4
                + 353 * S**3
                + 2289 * S**2
                + 1354 * S
                - 55440
            )
            / 384,
            (0, 1, 4): (S - 5)
            * (S - 4)
            * (S - 3)
            * (S - 2)
            * (S - 1)
            * (S**3 + 23 * S**2 + 234 * S + 1008)
            / 96,
            (1, 1, 4): (S - 6)
            * (S - 5)
            * (S - 4)
            * (S - 3)
            * (S - 2)
            * (S**3 + 23 * S**2 + 234 * S + 1008)
            / 96,
            (2, 1, 4): (S - 7)
            * (S - 6)
            * (S - 5)
            * (S - 4)
            * (
                S**4
                + 20 * S**3
                + 159 * S**2
                + 202 * S
                - 3600
            )
            / 96,
            (0, 2, 3): (S - 5)
            * (S - 4)
            * (S - 3)
            * (S - 2)
            * (S - 1)
            * (9 * S**3 + 99 * S**2 + 74 * S - 3360)
            / 576,
            (1, 2, 3): (S - 6)
            * (S - 5)
            * (S - 4)
            * (S - 3)
            * (S - 2)
            * (9 * S**3 + 90 * S**2 - 67 * S - 4088)
            / 576,
            (2, 2, 3): (S - 7)
            * (S - 6)
            * (S - 5)
            * (S - 4)
            * (
                9 * S**4
                + 54 * S**3
                - 487 * S**2
                - 4270 * S
                + 16560
            )
            / 576,
            (0, 3, 2): (S - 5)
            * (S - 4)
            * (S - 3)
            * (S - 2)
            * (S - 1)
            * (15 * S**3 - 15 * S**2 - 770 * S + 2352)
            / 1440,
            (1, 3, 2): (S - 6)
            * (S - 5)
            * (S - 4)
            * (S - 3)
            * (S - 2)
            * (15 * S**3 - 45 * S**2 - 860 * S + 3542)
            / 1440,
            (2, 3, 2): (S - 7)
            * (S - 6)
            * (S - 5)
            * (S - 4)
            * (
                15 * S**4
                - 120 * S**3
                - 725 * S**2
                + 8122 * S
                - 16176
            )
            / 1440,
            (0, 4, 1): (S - 5)
            * (S - 4)
            * (S - 3)
            * (S - 2)
            * (S - 1)
            * (15 * S**3 - 195 * S**2 + 830 * S - 1152)
            / 5760,
            (1, 4, 1): (S - 6)
            * (S - 5)
            * (S - 4)
            * (S - 3)
            * (S - 2)
            * (15 * S**3 - 240 * S**2 + 1265 * S - 2192)
            / 5760,
            (2, 4, 1): (S - 7)
            * (S - 6)
            * (S - 5)
            * (S - 4)
            * (S - 3)
            * (15 * S**3 - 285 * S**2 + 1790 * S - 3712)
            / 5760,
        }
    )
    expected_entries = {
        (h, excess, components)
        for h in range(3)
        for excess in range(5)
        for components in range(1, 6 - excess)
    }
    if set(table) != expected_entries:
        raise AssertionError("q=3 endpoint table is incomplete")
    return {key: sp.cancel(value) for key, value in table.items()}


Q3_ENDPOINT_POLYNOMIALS = _q3_endpoint_polynomials()


def q3_endpoint_entries() -> list[tuple[int, int, int]]:
    return sorted(Q3_ENDPOINT_POLYNOMIALS)


def _raw_endpoint_from_formula(
    s: int, h: int, excess: int, components: int
) -> int:
    normalized = sp.Rational(
        Q3_ENDPOINT_POLYNOMIALS[(h, excess, components)].subs(S, s)
    )
    exponent = s - h - 2 * components - excess
    raw = (
        sp.Integer(2) ** h
        * sp.Integer(s) ** exponent
        * normalized
    )
    raw = sp.cancel(raw)
    if not raw.is_Integer:
        raise AssertionError(
            "displayed q=3 endpoint was not an integer at "
            f"{(s, h, excess, components)}"
        )
    return int(raw)


def audit_q3_endpoint_table() -> list[list[object]]:
    """Certify the 45 formulas with exactly 345 main-enumerator values."""

    rows: list[list[object]] = []
    for h, excess, components in q3_endpoint_entries():
        expected = Q3_ENDPOINT_POLYNOMIALS[
            (h, excess, components)
        ]
        cleared = sp.cancel(S**excess * expected)
        numerator, denominator = sp.fraction(cleared)
        if sp.degree(denominator, S) > 0:
            raise AssertionError("cleared endpoint retained an s denominator")
        degree_bound = cleared_component_degree_bound(
            excess, components
        )
        if sp.degree(numerator, S) > degree_bound:
            raise AssertionError("q=3 endpoint exceeds the Abel degree bound")
        sample_count = rational_certificate_point_count(
            excess, components
        )
        for sample_s in range(
            Q3_ENDPOINT_SAMPLE_START,
            Q3_ENDPOINT_SAMPLE_START + sample_count,
        ):
            measured = sp.Rational(
                normalized_component_value(
                    sample_s, h, excess, components
                )
            )
            if sp.cancel(expected.subs(S, sample_s) - measured) != 0:
                raise AssertionError(
                    "main q=3 endpoint mismatch at "
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
    if len(rows) != 45 or sum(row[4] for row in rows) != 345:
        raise AssertionError("q=3 endpoint certificate size changed")
    return rows


def audit_independent_q3_endpoints() -> int:
    """Compare all 345 formulas with the direct-position audit engine."""

    rows = independent_endpoint_certificate(Q3_ENDPOINT_SAMPLE_START)
    for s, h, excess, components, measured in rows:
        expected = _raw_endpoint_from_formula(
            s, h, excess, components
        )
        if measured != expected:
            raise AssertionError(
                "independent q=3 endpoint mismatch at "
                f"{(s, h, excess, components)}: "
                f"{measured} != {expected}"
            )
    if len(rows) != 345:
        raise AssertionError("independent q=3 certificate size changed")
    return len(rows)


@lru_cache(maxsize=None)
def normalized_q3_layer(offset: int) -> sp.Expr:
    """Return the normalized beta-offset coefficient for n=2*s-8.

    The normalization is

        [beta^(2*n+offset)] B_n
        ---------------------------------,  n=2*s-8.
        n! * s^(2*s-14+offset)
    """

    if offset < 0 or offset > 6:
        raise ValueError("q=3 offset must lie in 0..6")
    total = sp.Integer(0)
    for overlap in range(offset // 2 + 1):
        remaining = offset - 2 * overlap
        lambda_exponent = 4 - overlap
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
                    6
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
                        positive_left in Q3_ENDPOINT_POLYNOMIALS
                        and positive_right in Q3_ENDPOINT_POLYNOMIALS
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
                            * Q3_ENDPOINT_POLYNOMIALS[positive_left]
                            * Q3_ENDPOINT_POLYNOMIALS[positive_right]
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
                        negative_left in Q3_ENDPOINT_POLYNOMIALS
                        and negative_right in Q3_ENDPOINT_POLYNOMIALS
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
                            * Q3_ENDPOINT_POLYNOMIALS[negative_left]
                            * Q3_ENDPOINT_POLYNOMIALS[negative_right]
                        )
                    total += prefactor * (positive - negative)
    return sp.factor(sp.cancel(total))


EXPECTED_Q3_NORMALIZED_LAYERS = (
    sp.Rational(2, 3)
    * (S - 4)
    * (
        S**5
        + 16 * S**4
        + 52 * S**3
        - 587 * S**2
        - 3063 * S
        + 12240
    ),
    sp.Rational(4, 3)
    * (S - 4)
    * (
        3 * S**5
        + 31 * S**4
        - 16 * S**3
        - 1217 * S**2
        - 1038 * S
        + 12240
    ),
    sp.Rational(2, 3)
    * (S - 4)
    * (
        18 * S**5
        + 85 * S**4
        - 678 * S**3
        - 3138 * S**2
        + 13195 * S
        - 2475
    ),
    sp.Rational(8, 3)
    * (S - 4)
    * (
        8 * S**5
        - 6 * S**4
        - 314 * S**3
        + 432 * S**2
        + 2847 * S
        - 5265
    ),
    sp.Rational(2, 3)
    * (S - 4)
    * (2 * S - 9)
    * (
        18 * S**4
        - 29 * S**3
        - 391 * S**2
        + 1054 * S
        - 312
    ),
    sp.Rational(4, 3)
    * (S - 4)
    * (2 * S - 9)
    * (2 * S - 7)
    * (3 * S - 7)
    * (S**2 - S - 8),
    sp.Rational(2, 3)
    * (S - 4)
    * (S - 3)
    * (2 * S - 9)
    * (2 * S - 7)
    * (2 * S**2 - 11 * S + 13),
)


def audit_symbolic_q3_layers() -> list[list[object]]:
    """Check all seven reductions, cancellations, and shifted signs."""

    rows: list[list[object]] = []
    for offset, expected in enumerate(EXPECTED_Q3_NORMALIZED_LAYERS):
        measured = normalized_q3_layer(offset)
        expected = sp.factor(expected)
        if sp.cancel(measured - expected) != 0:
            raise AssertionError(
                f"q=3 symbolic layer mismatch at offset {offset}"
            )
        numerator, denominator = sp.fraction(sp.cancel(measured))
        if sp.degree(denominator, S) > 0:
            raise AssertionError(
                f"q=3 denominator did not cancel at offset {offset}"
            )
        cleared_coefficient = sp.expand(S**offset * measured)
        if (
            sp.degree(cleared_coefficient, S)
            > 2 * Q3_DEFICIT + offset + 2
        ):
            raise AssertionError(
                f"q=3 coefficient degree bound failed at {offset}"
            )
        shifted = sp.Poly(sp.expand(expected.subs(S, U + 5)), U)
        increasing_coefficients = list(reversed(shifted.all_coeffs()))
        if any(coefficient <= 0 for coefficient in increasing_coefficients):
            raise AssertionError(
                f"q=3 shifted positivity failed at offset {offset}"
            )
        rows.append(
            [
                offset,
                str(expected),
                [str(value) for value in increasing_coefficients],
            ]
        )
    return rows


def q3_coefficients(s: int) -> dict[int, int]:
    """The complete seven coefficients of B_(2*s-8)."""

    if s < 4:
        raise ValueError("the complete-split core requires s>=4")
    depth = 2 * s - 8
    result: dict[int, int] = {}
    for offset, polynomial in enumerate(
        EXPECTED_Q3_NORMALIZED_LAYERS
    ):
        value = sp.cancel(
            sp.factorial(depth)
            * sp.Integer(s) ** (2 * s - 14 + offset)
            * polynomial.subs(S, s)
        )
        if not value.is_Integer:
            raise AssertionError("q=3 coefficient formula was fractional")
        if value:
            result[4 * s - 16 + offset] = int(value)
    return result


def audit_primitive_q3_rows(
    minimum_s: int = 4, maximum_s: int = 16
) -> list[list[int]]:
    """Compare the formula with the independent primitive pooled engine."""

    independent = audit_primitive_q3(minimum_s, maximum_s)
    rows = [list(row) for row in independent]
    for s in range(minimum_s, maximum_s + 1):
        measured = {
            degree: coefficient
            for sample_s, degree, coefficient in independent
            if sample_s == s
        }
        expected = q3_coefficients(s)
        if measured != expected:
            raise AssertionError(
                f"q=3 primitive transcription mismatch at s={s}"
            )
    return rows


def build_certificate(
    minimum_s: int = 4, maximum_s: int = 16
) -> dict[str, object]:
    endpoint_rows = audit_q3_endpoint_table()
    independent_endpoint_count = audit_independent_q3_endpoints()
    symbolic_rows = audit_symbolic_q3_layers()
    primitive_rows = audit_primitive_q3_rows(minimum_s, maximum_s)
    payload = json.dumps(
        [
            endpoint_rows,
            independent_endpoint_count,
            symbolic_rows,
            primitive_rows,
        ],
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return {
        "schema": "amra.opg1757.fourth_attack_q3.v1",
        "status": "PASS",
        "theorem_status": "PROVED",
        "proved_layer": (
            "B_(2s-8)=0 at s=4 and is coefficientwise strictly "
            "positive for every integer s>=5"
        ),
        "exact_formula": (
            "B_(2s-8)=(2s-8)!*s^(2s-14)*beta^(4s-16)"
            "*sum_(r=0)^6 s^r*P_r(s)*beta^r"
        ),
        "endpoint_formulas": endpoint_rows,
        "endpoint_count": len(endpoint_rows),
        "denominator_aware_endpoint_values": sum(
            row[4] for row in endpoint_rows
        ),
        "independent_endpoint_values": independent_endpoint_count,
        "endpoint_s_range": [
            Q3_ENDPOINT_SAMPLE_START,
            max(
                Q3_ENDPOINT_SAMPLE_START + row[4] - 1
                for row in endpoint_rows
            ),
        ],
        "normalized_layers": symbolic_rows,
        "overlap_orders": [0, 1, 2, 3],
        "excess_4_species": [
            "one 6-edge",
            "one 5-edge plus one 3-edge",
            "two 4-edges",
            "one 4-edge plus two 3-edges",
            "four 3-edges",
        ],
        "primitive_s_range": [minimum_s, maximum_s],
        "primitive_rows": len(primitive_rows),
        "scope_firewall": (
            "This proves only q=3 for the complete-split pooled layer. "
            "It does not prove arbitrary fixed q, all B_n, or arbitrary "
            "host OPG-1757."
        ),
        "sha256": hashlib.sha256(payload).hexdigest(),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--minimum-s", type=int, default=4)
    parser.add_argument("--maximum-s", type=int, default=16)
    args = parser.parse_args()
    print(
        json.dumps(
            build_certificate(args.minimum_s, args.maximum_s),
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
