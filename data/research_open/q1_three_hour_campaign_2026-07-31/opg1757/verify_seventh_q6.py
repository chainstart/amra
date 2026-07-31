#!/usr/bin/env python3
"""Exact symbolic certificate for the OPG-1757 q=6 pooled layer.

The target is ``B_(2*s-11)``.  The endpoint table is inherited from q=5
except for the 24 boundary triples ``(h,e,8-e)``.  Those entries are
reconstructed with the denominator-aware Abel degree bound, using an exact
anchored-component recurrence that is substantially faster than temporarily
labelling all forest components.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from collections import defaultdict
from fractions import Fraction
from functools import lru_cache

import sympy as sp

from verify_sixth_q5 import Q5_ENDPOINT_POLYNOMIALS
from verify_second_deficit import (
    S,
    U,
    cleared_component_degree_bound,
    contract_selections,
    falling,
    profile_forest_weight,
    rational_certificate_point_count,
)


Q6_DEFICIT = 6
Q6_ENDPOINT_SAMPLE_START = 11


@lru_cache(maxsize=None)
def uniform_forest_weight(vertices: int, components: int) -> int:
    """Unweighted labelled forests, anchored at the least vertex."""

    if vertices == 0:
        return int(components == 0)
    if components < 1 or components > vertices:
        return 0
    total = 0
    for component_size in range(1, vertices - components + 2):
        tree_weight = (
            1
            if component_size == 1
            else component_size ** (component_size - 2)
        )
        total += (
            math.comb(vertices - 1, component_size - 1)
            * tree_weight
            * uniform_forest_weight(
                vertices - component_size, components - 1
            )
        )
    return total


@lru_cache(maxsize=None)
def _exceptional_forest_weight(
    exceptional: tuple[int, ...], units: int, components: int
) -> int:
    """Weighted forests by the component containing exceptional block 0."""

    if not exceptional:
        return uniform_forest_weight(units, components)
    if components < 1 or components > len(exceptional) + units:
        return 0

    anchor = exceptional[0]
    others = exceptional[1:]
    total = 0
    for mask in range(1 << len(others)):
        selected = tuple(
            others[index]
            for index in range(len(others))
            if mask & (1 << index)
        )
        remaining = tuple(
            others[index]
            for index in range(len(others))
            if not mask & (1 << index)
        )
        exceptional_count = 1 + len(selected)
        weight_sum = anchor + sum(selected)
        weight_product = anchor * math.prod(selected)
        for selected_units in range(units + 1):
            component_size = exceptional_count + selected_units
            tree_weight = (
                1
                if component_size == 1
                else (weight_sum + selected_units)
                ** (component_size - 2)
                * weight_product
            )
            total += (
                math.comb(units, selected_units)
                * tree_weight
                * _exceptional_forest_weight(
                    remaining,
                    units - selected_units,
                    components - 1,
                )
            )
    return total


@lru_cache(maxsize=None)
def fast_profile_forest_weight(
    profile: tuple[int, ...], components: int
) -> int:
    """Exact weighted forest sum with canonical component anchoring."""

    exceptional = tuple(weight for weight in profile if weight != 1)
    units = len(profile) - len(exceptional)
    return _exceptional_forest_weight(exceptional, units, components)


@lru_cache(maxsize=None)
def fast_hyperforest_component_weight(
    s: int, h: int, excess: int, components: int
) -> int:
    """Exact hyperforest endpoint using the fast forest recurrence."""

    initial = tuple(sorted((2,) * h + (1,) * (s - 2 * h)))
    if excess == 0:
        return fast_profile_forest_weight(initial, components)

    layer: dict[tuple[tuple[int, ...], int], int] = {(initial, 0): 1}
    answer = Fraction(0)
    for nonbinary_count in range(1, excess + 1):
        next_layer: defaultdict[
            tuple[tuple[int, ...], int], int
        ] = defaultdict(int)
        for (profile, used_excess), coefficient in layer.items():
            for added_excess in range(1, excess - used_excess + 1):
                for multiplicity, destination in contract_selections(
                    profile, added_excess + 2
                ):
                    next_layer[
                        (destination, used_excess + added_excess)
                    ] += coefficient * multiplicity
        layer = dict(next_layer)
        ordered_weight = sum(
            coefficient
            * fast_profile_forest_weight(profile, components)
            for (profile, used_excess), coefficient in layer.items()
            if used_excess == excess
        )
        answer += Fraction(
            ordered_weight, math.factorial(nonbinary_count)
        )

    if answer.denominator != 1:
        raise AssertionError("unordered hyperforest weight is fractional")
    return answer.numerator


def fast_normalized_component_value(
    s: int, h: int, excess: int, components: int
) -> Fraction:
    raw = fast_hyperforest_component_weight(s, h, excess, components)
    exponent = s - h - 2 * components - excess
    value = Fraction(raw, 2**h)
    if exponent >= 0:
        value /= s**exponent
    else:
        value *= s ** (-exponent)
    return value


def audit_fast_forest_recurrence() -> int:
    """Compare the new recurrence with the original partition recurrence."""

    profiles = (
        (1, 1, 1, 1),
        (1, 1, 1, 2),
        (1, 1, 2, 2),
        (1, 1, 2, 3),
        (1, 2, 2, 3),
        (2, 2, 3, 4),
    )
    checked = 0
    for profile in profiles:
        profile = tuple(sorted(profile))
        for components in range(1, len(profile) + 1):
            expected = profile_forest_weight(profile, components)
            measured = fast_profile_forest_weight(profile, components)
            if measured != expected:
                raise AssertionError(
                    "fast forest recurrence mismatch at "
                    f"{(profile, components)}"
                )
            checked += 1
    return checked


def _q6_endpoint_polynomials() -> dict[tuple[int, int, int], sp.Expr]:
    """The 84 inherited endpoints plus 24 exact q=6 boundary entries."""

    table = dict(Q5_ENDPOINT_POLYNOMIALS)
    for excess in range(8):
        components = 8 - excess
        degree_bound = cleared_component_degree_bound(
            excess, components
        )
        sample_count = degree_bound + 1
        for h in range(3):
            points = []
            for sample_s in range(
                Q6_ENDPOINT_SAMPLE_START,
                Q6_ENDPOINT_SAMPLE_START + sample_count,
            ):
                cleared_value = (
                    sp.Rational(
                        fast_normalized_component_value(
                            sample_s, h, excess, components
                        )
                    )
                    * sample_s**excess
                )
                points.append((sample_s, cleared_value))
            cleared = sp.interpolate(points, S)
            if sp.degree(cleared, S) > degree_bound:
                raise AssertionError("q=6 endpoint interpolation overflow")
            table[(h, excess, components)] = sp.factor(
                sp.cancel(cleared / S**excess)
            )

    expected_entries = {
        (h, excess, components)
        for h in range(3)
        for excess in range(8)
        for components in range(1, 9 - excess)
    }
    if set(table) != expected_entries:
        raise AssertionError("q=6 endpoint table is incomplete")
    return table


Q6_ENDPOINT_POLYNOMIALS = _q6_endpoint_polynomials()


def q6_endpoint_entries() -> list[tuple[int, int, int]]:
    return sorted(Q6_ENDPOINT_POLYNOMIALS)


def audit_q6_endpoint_table() -> list[list[object]]:
    """Certify all 108 formulas with exactly 1,368 endpoint values."""

    rows: list[list[object]] = []
    for h, excess, components in q6_endpoint_entries():
        expected = Q6_ENDPOINT_POLYNOMIALS[(h, excess, components)]
        cleared = sp.cancel(S**excess * expected)
        numerator, denominator = sp.fraction(cleared)
        if sp.degree(denominator, S) > 0:
            raise AssertionError("q=6 endpoint retained an s denominator")
        degree_bound = cleared_component_degree_bound(
            excess, components
        )
        if sp.degree(numerator, S) > degree_bound:
            raise AssertionError("q=6 endpoint exceeds Abel degree bound")
        sample_count = rational_certificate_point_count(
            excess, components
        )
        for sample_s in range(
            Q6_ENDPOINT_SAMPLE_START,
            Q6_ENDPOINT_SAMPLE_START + sample_count,
        ):
            measured = sp.Rational(
                fast_normalized_component_value(
                    sample_s, h, excess, components
                )
            )
            if sp.cancel(expected.subs(S, sample_s) - measured) != 0:
                raise AssertionError(
                    "q=6 endpoint mismatch at "
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
    if len(rows) != 108 or sum(row[4] for row in rows) != 1368:
        raise AssertionError(
            "q=6 count firewall failed: full table must be 108/1368"
        )
    return rows


@lru_cache(maxsize=None)
def normalized_q6_layer(offset: int) -> sp.Expr:
    """Return [beta^(2*n+r)]B_n/(n!*s^(2*s-20+r))."""

    if offset < 0 or offset > 12:
        raise ValueError("q=6 offset must lie in 0..12")
    total = sp.Integer(0)
    for overlap in range(offset // 2 + 1):
        remaining = offset - 2 * overlap
        lambda_exponent = 7 - overlap
        for left_excess in range(remaining + 1):
            for right_excess in range(remaining - left_excess + 1):
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
                    9
                    - overlap
                    - left_excess
                    - right_excess
                )
                for left_components in range(1, component_sum):
                    right_components = component_sum - left_components
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
                        positive_left in Q6_ENDPOINT_POLYNOMIALS
                        and positive_right in Q6_ENDPOINT_POLYNOMIALS
                    ):
                        positive = (
                            4
                            * falling(
                                S
                                - 1
                                - left_components
                                - left_excess,
                                overlap,
                            )
                            * falling(
                                S
                                - 1
                                - right_components
                                - right_excess,
                                overlap,
                            )
                            * Q6_ENDPOINT_POLYNOMIALS[positive_left]
                            * Q6_ENDPOINT_POLYNOMIALS[positive_right]
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
                        negative_left in Q6_ENDPOINT_POLYNOMIALS
                        and negative_right in Q6_ENDPOINT_POLYNOMIALS
                    ):
                        negative = (
                            4
                            * falling(
                                S - left_components - left_excess,
                                overlap,
                            )
                            * falling(
                                S
                                - 2
                                - right_components
                                - right_excess,
                                overlap,
                            )
                            * Q6_ENDPOINT_POLYNOMIALS[negative_left]
                            * Q6_ENDPOINT_POLYNOMIALS[negative_right]
                        )
                    total += prefactor * (positive - negative)
    return sp.factor(sp.cancel(total))


EXPECTED_Q6_NORMALIZED_LAYERS = (
    sp.Rational(1, 180)
    * (S - 6)
    * (S - 5)
    * (S - 4)
    * (
        S**9
        + 39 * S**8
        + 667 * S**7
        + 5064 * S**6
        - 10918 * S**5
        - 512106 * S**4
        - 2462113 * S**3
        + 15195399 * S**2
        + 108066951 * S
        - 385491960
    ),
    sp.Rational(1, 45)
    * (S - 6)
    * (S - 5)
    * (S - 4)
    * (
        3 * S**9
        + 97 * S**8
        + 1309 * S**7
        + 5982 * S**6
        - 57396 * S**5
        - 834688 * S**4
        - 1331401 * S**3
        + 27140127 * S**2
        + 71718471 * S
        - 385491960
    ),
    sp.Rational(1, 90)
    * (S - 6)
    * (S - 5)
    * (S - 4)
    * (
        36 * S**9
        + 922 * S**8
        + 8823 * S**7
        + 2697 * S**6
        - 647927 * S**5
        - 3900203 * S**4
        + 12372203 * S**3
        + 136241377 * S**2
        - 161376108 * S
        - 762037920
    ),
    sp.Rational(1, 405)
    * (S - 6)
    * (S - 5)
    * (S - 4)
    * (
        630 * S**9
        + 11925 * S**8
        + 62010 * S**7
        - 515024 * S**6
        - 7196322 * S**5
        - 5179532 * S**4
        + 236824458 * S**3
        + 309695827 * S**2
        - 3320427270 * S
        + 2613794400
    ),
    sp.Rational(1, 180)
    * (S - 6)
    * (S - 5)
    * (S - 4)
    * (
        780 * S**9
        + 9600 * S**8
        - 2795 * S**7
        - 743576 * S**6
        - 3024266 * S**5
        + 23040040 * S**4
        + 113327830 * S**3
        - 480942194 * S**2
        - 518446149 * S
        + 2114358750
    ),
    sp.Rational(2, 315)
    * (S - 6)
    * (S - 5)
    * (S - 4)
    * (
        1428 * S**9
        + 8232 * S**8
        - 88109 * S**7
        - 881706 * S**6
        + 2148874 * S**5
        + 34670526 * S**4
        - 60290564 * S**3
        - 504561798 * S**2
        + 1398747555 * S
        - 575672202
    ),
    sp.Rational(1, 135)
    * (S - 6)
    * (S - 5)
    * (S - 4)
    * (
        1968 * S**9
        - 1368 * S**8
        - 152196 * S**7
        - 177962 * S**6
        + 6502782 * S**5
        + 4420408 * S**4
        - 154686372 * S**3
        + 244336501 * S**2
        + 508123992 * S
        - 1041647256
    ),
    sp.Rational(2, 45)
    * (S - 6)
    * (S - 5)
    * (S - 4)
    * (
        408 * S**9
        - 2884 * S**8
        - 21246 * S**7
        + 148389 * S**6
        + 709230 * S**5
        - 5314587 * S**4
        - 3005613 * S**3
        + 71300470 * S**2
        - 138576132 * S
        + 62098560
    ),
    sp.Rational(1, 180)
    * (S - 6)
    * (S - 5)
    * (S - 4)
    * (2 * S - 11)
    * (
        1560 * S**8
        - 12260 * S**7
        - 48130 * S**6
        + 519793 * S**5
        + 526163 * S**4
        - 11229722 * S**3
        + 21034223 * S**2
        + 14038365 * S
        - 45227700
    ),
    sp.Rational(1, 135)
    * (S - 6)
    * (S - 5)
    * (S - 4)
    * (2 * S - 11)
    * (2 * S - 9)
    * (
        420 * S**7
        - 4020 * S**6
        - 2565 * S**5
        + 119107 * S**4
        - 214808 * S**3
        - 906217 * S**2
        + 3037523 * S
        - 2155500
    ),
    sp.Rational(1, 90)
    * (S - 6)
    * (S - 5)
    * (S - 4)
    * (2 * S - 11)
    * (2 * S - 9)
    * (
        144 * S**7
        - 2264 * S**6
        + 10144 * S**5
        + 11306 * S**4
        - 208341 * S**3
        + 525041 * S**2
        - 290924 * S
        - 271056
    ),
    sp.Rational(1, 45)
    * (S - 6)
    * (S - 5)
    * (S - 4)
    * (2 * S - 11)
    * (2 * S - 9) ** 2
    * (2 * S - 7)
    * (S**2 - S - 8)
    * (6 * S**3 - 77 * S**2 + 307 * S - 358),
    sp.Rational(1, 11340)
    * (S - 6)
    * (S - 5)
    * (S - 4)
    * (S - 3)
    * (2 * S - 11)
    * (2 * S - 9)
    * (2 * S - 7)
    * (
        504 * S**5
        - 10836 * S**4
        + 90342 * S**3
        - 360955 * S**2
        + 677187 * S
        - 457250
    ),
)


def audit_symbolic_q6_layers() -> list[list[object]]:
    """Check all 13 formulas, the three roots, degree drop, and signs."""

    rows: list[list[object]] = []
    boundary_factor = (S - 4) * (S - 5) * (S - 6)
    for offset, expected in enumerate(EXPECTED_Q6_NORMALIZED_LAYERS):
        measured = normalized_q6_layer(offset)
        expected = sp.factor(expected)
        if sp.cancel(measured - expected) != 0:
            raise AssertionError(
                f"q=6 symbolic layer mismatch at offset {offset}"
            )
        numerator, denominator = sp.fraction(sp.cancel(measured))
        if sp.degree(denominator, S) > 0:
            raise AssertionError(
                f"q=6 denominator did not cancel at offset {offset}"
            )
        if sp.rem(numerator, boundary_factor, domain=sp.QQ) != 0:
            raise AssertionError(
                f"q=6 boundary factor failed at offset {offset}"
            )
        cleared_coefficient = sp.expand(S**offset * measured)
        if sp.degree(cleared_coefficient, S) > 12 + offset:
            raise AssertionError(
                f"q=6 top-two degree bound failed at offset {offset}"
            )
        shifted = sp.Poly(sp.expand(expected.subs(S, U + 7)), U)
        increasing_coefficients = list(reversed(shifted.all_coeffs()))
        if any(value <= 0 for value in increasing_coefficients):
            raise AssertionError(
                f"q=6 shifted positivity failed at offset {offset}"
            )
        rows.append(
            [
                offset,
                str(expected),
                [str(value) for value in increasing_coefficients],
            ]
        )
    return rows


def q6_coefficients(s: int) -> dict[int, int]:
    """The complete 13 coefficients of B_(2*s-11), for s>=6."""

    if s < 6:
        raise ValueError("q=6 has nonnegative depth only for s>=6")
    depth = 2 * s - 11
    result: dict[int, int] = {}
    for offset, polynomial in enumerate(
        EXPECTED_Q6_NORMALIZED_LAYERS
    ):
        value = sp.cancel(
            sp.factorial(depth)
            * sp.Integer(s) ** (2 * s - 20 + offset)
            * polynomial.subs(S, s)
        )
        if not value.is_Integer:
            raise AssertionError("q=6 coefficient formula was fractional")
        if value:
            result[4 * s - 22 + offset] = int(value)
    return result


def audit_independent_q6_coefficients() -> int:
    """Run the top-two/boundary-reduced 208-point primitive audit."""

    from audit_seventh_q6_independent import audit_rational_q6_certificate

    rows = audit_rational_q6_certificate(7)
    if len(rows) != 208:
        raise AssertionError("independent q=6 point count changed")
    return len(rows)


def build_certificate() -> dict[str, object]:
    fast_recurrence_checks = audit_fast_forest_recurrence()
    endpoint_rows = audit_q6_endpoint_table()
    symbolic_rows = audit_symbolic_q6_layers()
    independent_points = audit_independent_q6_coefficients()
    payload = json.dumps(
        [
            fast_recurrence_checks,
            endpoint_rows,
            symbolic_rows,
            independent_points,
        ],
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return {
        "schema": "amra.opg1757.seventh_attack_q6.v1",
        "status": "PASS",
        "theorem_status": "PROVED",
        "proved_layer": (
            "B_(2s-11)=0 at s=6 and is coefficientwise strictly "
            "positive for every integer s>=7"
        ),
        "exact_formula": (
            "B_(2s-11)=(2s-11)!*s^(2s-20)*beta^(4s-22)"
            "*sum_(r=0)^12 s^r*P_r(s)*beta^r"
        ),
        "fast_recurrence_comparisons": fast_recurrence_checks,
        "endpoint_formulas": endpoint_rows,
        "endpoint_count": len(endpoint_rows),
        "denominator_aware_endpoint_values": sum(
            row[4] for row in endpoint_rows
        ),
        "endpoint_s_range": [
            Q6_ENDPOINT_SAMPLE_START,
            max(
                Q6_ENDPOINT_SAMPLE_START + row[4] - 1
                for row in endpoint_rows
            ),
        ],
        "count_firewall": "108 endpoints / 1368 values",
        "normalized_layers": symbolic_rows,
        "offset_count": len(symbolic_rows),
        "overlap_orders": [0, 1, 2, 3, 4, 5, 6],
        "coefficient_degree_bound": "deg R_(6,r) <= 12+r",
        "boundary_factor": "(s-4)*(s-5)*(s-6)",
        "quotient_degree_bound": "deg(R/F_6) <= 9+r",
        "independent_coefficient_values": independent_points,
        "independent_coefficient_s_range": [7, 28],
        "boundary": "B_1(6,beta)=0",
        "scope_firewall": (
            "This proves only q=6 for the complete-split pooled layer. "
            "It does not prove arbitrary fixed-q positivity, all B_n, "
            "or arbitrary-host OPG-1757."
        ),
        "sha256": hashlib.sha256(payload).hexdigest(),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--emit-formulas",
        action="store_true",
        help="print the 13 derived normalized formulas only",
    )
    arguments = parser.parse_args()
    if arguments.emit_formulas:
        for offset, value in enumerate(EXPECTED_Q6_NORMALIZED_LAYERS):
            print(offset, sp.sstr(sp.factor(value)), flush=True)
        return
    print(json.dumps(build_certificate(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
