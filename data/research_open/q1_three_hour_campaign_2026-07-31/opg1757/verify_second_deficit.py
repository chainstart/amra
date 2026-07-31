#!/usr/bin/env python3
"""Exact certificate for the OPG-1757 layer B_(2s-7).

The chain coefficient at beta degree 2j+e is encoded by a complete weighted
hyperforest with j hyperedges and total excess

    e = sum_E (|E|-2).

This script:

* enumerates the excess-0/1/2/3 hyperforest component endpoints;
* certifies their displayed formulas after clearing the denominator supplied
  by the exceptional-profile Abel lemma;
* applies the exact overlap-derivative pooled formula;
* verifies all five coefficients of B_(2s-7);
* supplies the omitted symbolic algebra from the first attack.

All arithmetic is exact.  The certificate does not assume that a normalized
endpoint is a polynomial.  For excess e and c components, it uses the proved
denominator-aware bound

    denominator | s**e,    numerator degree <= 2*c + 3*e - 2,

and checks the required 2*c+3*e-1 distinct values.  A direct-position
implementation independently supplies the same 180 values, including the
previously missing s=16 endpoints at excess three.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from collections import Counter, defaultdict
from functools import lru_cache
from fractions import Fraction
from pathlib import Path
from typing import Iterator

import sympy as sp

from verify_pooled_top_face import (
    integer_power,
    primitive_pooled_rows,
    stirling2,
)


S = sp.symbols("s", integer=True, positive=True)
U = sp.symbols("u", integer=True, nonnegative=True)
Profile = tuple[int, ...]


def weak_compositions(total: int, parts: int) -> Iterator[tuple[int, ...]]:
    if parts == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for tail in weak_compositions(total - first, parts - 1):
            yield (first, *tail)


def multinomial(total: int, cells: tuple[int, ...]) -> int:
    value = math.factorial(total)
    for cell in cells:
        value //= math.factorial(cell)
    return value


@lru_cache(maxsize=None)
def contract_selections(
    profile: Profile, selection_size: int
) -> tuple[tuple[int, Profile], ...]:
    """Apply one complete r-hyperedge contraction, aggregated by weights."""

    if selection_size < 2 or selection_size > len(profile):
        return ()
    types = sorted(Counter(profile).items())
    result: list[tuple[int, Profile]] = []

    def visit(
        index: int,
        remaining_to_select: int,
        multiplicity: int,
        unselected: tuple[int, ...],
        selected_weight: int,
    ) -> None:
        if index == len(types):
            if remaining_to_select == 0:
                destination = tuple(sorted((*unselected, selected_weight)))
                result.append((multiplicity, destination))
            return
        weight, count = types[index]
        for chosen in range(min(count, remaining_to_select) + 1):
            visit(
                index + 1,
                remaining_to_select - chosen,
                multiplicity
                * math.comb(count, chosen)
                * weight**chosen,
                unselected + (weight,) * (count - chosen),
                selected_weight + chosen * weight,
            )

    visit(0, selection_size, 1, (), 0)
    return tuple(result)


@lru_cache(maxsize=None)
def profile_forest_weight(profile: Profile, components: int) -> int:
    """Weighted complete-graph forests with exactly c components."""

    if components < 1 or components > len(profile):
        return 0
    types = sorted(Counter(profile).items())
    component_sums = [0] * components
    component_sizes = [0] * components
    component_products = [1] * components
    total = 0

    def visit(type_index: int, multiplicity: int) -> None:
        nonlocal total
        if type_index == len(types):
            if any(size == 0 for size in component_sizes):
                return
            contribution = multiplicity
            for weight_sum, size, product in zip(
                component_sums,
                component_sizes,
                component_products,
            ):
                if size > 1:
                    contribution *= weight_sum ** (size - 2) * product
            total += contribution
            return

        weight, count = types[type_index]
        for distribution in weak_compositions(count, components):
            old_state = list(
                zip(component_sums, component_sizes, component_products)
            )
            for index, cell in enumerate(distribution):
                component_sums[index] += weight * cell
                component_sizes[index] += cell
                component_products[index] *= weight**cell
            visit(
                type_index + 1,
                multiplicity * multinomial(count, distribution),
            )
            for index, (weight_sum, size, product) in enumerate(old_state):
                component_sums[index] = weight_sum
                component_sizes[index] = size
                component_products[index] = product

    visit(0, 1)
    divisor = math.factorial(components)
    if total % divisor:
        raise AssertionError("temporary component labels did not divide out")
    return total // divisor


@lru_cache(maxsize=None)
def hyperforest_component_weight(
    s: int, h: int, excess: int, components: int
) -> int:
    """Weight of complete hyperforests at fixed excess and component count.

    Nonbinary hyperedges are generated as unordered sets by the exponential
    of contraction operators.  An ordered list of m contractions is divided
    by m!, while all remaining hyperedges are ordinary binary forest edges.
    """

    initial = tuple(sorted((2,) * h + (1,) * (s - 2 * h)))
    if excess == 0:
        return profile_forest_weight(initial, components)

    layer: dict[tuple[Profile, int], int] = {(initial, 0): 1}
    answer = Fraction(0)
    for nonbinary_count in range(1, excess + 1):
        next_layer: defaultdict[tuple[Profile, int], int] = defaultdict(int)
        for (profile, used_excess), coefficient in layer.items():
            for added_excess in range(1, excess - used_excess + 1):
                selection_size = added_excess + 2
                for multiplicity, destination in contract_selections(
                    profile, selection_size
                ):
                    next_layer[
                        (destination, used_excess + added_excess)
                    ] += coefficient * multiplicity
        layer = dict(next_layer)
        ordered_weight = sum(
            coefficient * profile_forest_weight(profile, components)
            for (profile, used_excess), coefficient in layer.items()
            if used_excess == excess
        )
        answer += Fraction(
            ordered_weight, math.factorial(nonbinary_count)
        )

    if answer.denominator != 1:
        raise AssertionError("unordered hyperforest weight is fractional")
    return answer.numerator


def component_degree_bound(excess: int, components: int) -> int:
    """Degree of the displayed, a posteriori polynomial table entry."""

    return 2 * components + 2 * excess - 2


def cleared_component_degree_bound(excess: int, components: int) -> int:
    """Degree after multiplying the normalized endpoint by s**excess."""

    return 2 * components + 3 * excess - 2


def rational_certificate_point_count(
    excess: int, components: int
) -> int:
    """Values needed after the denominator-aware Abel reduction."""

    return cleared_component_degree_bound(excess, components) + 1


def normalized_component_value(
    s: int, h: int, excess: int, components: int
) -> Fraction:
    raw = hyperforest_component_weight(s, h, excess, components)
    exponent = s - h - 2 * components - excess
    value = Fraction(raw, 2**h)
    if exponent >= 0:
        value /= s**exponent
    else:
        value *= s ** (-exponent)
    return value


def _component_polynomials() -> dict[tuple[int, int, int], sp.Expr]:
    """Closed normalized endpoint table H_{h,e,c}."""

    table: dict[tuple[int, int, int], sp.Expr] = {}
    for h in range(3):
        table[(h, 0, 1)] = sp.Integer(1)

    table.update(
        {
            (0, 0, 2): (S - 1) * (S + 6) / 2,
            (1, 0, 2): (S - 2) * (S + 6) / 2,
            (2, 0, 2): (S**2 + 3 * S - 20) / 2,
            (0, 0, 3): (S - 2)
            * (S - 1)
            * (S**2 + 13 * S + 60)
            / 8,
            (1, 0, 3): (S - 3)
            * (S - 2)
            * (S**2 + 13 * S + 60)
            / 8,
            (2, 0, 3): (S - 4)
            * (S**3 + 10 * S**2 + 17 * S - 210)
            / 8,
            (0, 0, 4): (S - 3)
            * (S - 2)
            * (S - 1)
            * (S**3 + 21 * S**2 + 202 * S + 840)
            / 48,
            (1, 0, 4): (S - 4)
            * (S - 3)
            * (S - 2)
            * (S**3 + 21 * S**2 + 202 * S + 840)
            / 48,
            (2, 0, 4): (S - 5)
            * (S - 4)
            * (
                S**4
                + 18 * S**3
                + 133 * S**2
                + 138 * S
                - 3024
            )
            / 48,
            (0, 1, 1): (S - 2) * (S - 1) / 2,
            (1, 1, 1): (S - 3) * (S - 2) / 2,
            (2, 1, 1): (S - 4) * (S - 3) / 2,
            (0, 1, 2): (S - 3)
            * (S - 2)
            * (S - 1)
            * (3 * S + 20)
            / 12,
            (1, 1, 2): (S - 4)
            * (S - 3)
            * (S - 2)
            * (3 * S + 20)
            / 12,
            (2, 1, 2): (S - 5)
            * (S - 4)
            * (3 * S**2 + 11 * S - 66)
            / 12,
            (0, 1, 3): (S - 4)
            * (S - 3)
            * (S - 2)
            * (S - 1)
            * (3 * S**2 + 43 * S + 210)
            / 48,
            (1, 1, 3): (S - 5)
            * (S - 4)
            * (S - 3)
            * (S - 2)
            * (3 * S**2 + 43 * S + 210)
            / 48,
            (2, 1, 3): (S - 6)
            * (S - 5)
            * (S - 4)
            * (3 * S**3 + 34 * S**2 + 69 * S - 728)
            / 48,
            (0, 2, 1): (S - 3)
            * (S - 2)
            * (S - 1)
            * (3 * S - 8)
            / 24,
            (1, 2, 1): (S - 4)
            * (S - 3)
            * (S - 2)
            * (3 * S - 11)
            / 24,
            (2, 2, 1): (S - 5)
            * (S - 4)
            * (S - 3)
            * (3 * S - 14)
            / 24,
            (0, 2, 2): (S - 4)
            * (S - 3)
            * (S - 2)
            * (S - 1)
            * (3 * S**2 + 11 * S - 80)
            / 48,
            (1, 2, 2): (S - 5)
            * (S - 4)
            * (S - 3)
            * (S - 2)
            * (3 * S**2 + 8 * S - 102)
            / 48,
            (2, 2, 2): (S - 6)
            * (S - 5)
            * (S - 4)
            * (3 * S**3 - 4 * S**2 - 145 * S + 406)
            / 48,
            (0, 3, 1): (S - 4) ** 2
            * (S - 3) ** 2
            * (S - 2)
            * (S - 1)
            / 48,
            (1, 3, 1): (S - 5) ** 2
            * (S - 4) ** 2
            * (S - 3)
            * (S - 2)
            / 48,
            (2, 3, 1): (S - 6) ** 2
            * (S - 5) ** 2
            * (S - 4)
            * (S - 3)
            / 48,
        }
    )
    return {key: sp.cancel(value) for key, value in table.items()}


COMPONENT_POLYNOMIALS = _component_polynomials()


def component_entries() -> list[tuple[int, int, int]]:
    return sorted(COMPONENT_POLYNOMIALS)


def audit_component_polynomial_table() -> list[list[object]]:
    """Clear-denominator identity certificate for every endpoint formula.

    SECOND_ATTACK.md proves that s**e times a normalized endpoint is a
    polynomial of degree at most 2*c+3*e-2.  Equality at the returned number
    of distinct positive s-values therefore proves the displayed identity.
    No polynomiality of the normalized endpoint is assumed here.
    """

    rows: list[list[object]] = []
    for h, excess, components in component_entries():
        displayed_degree_bound = component_degree_bound(
            excess, components
        )
        cleared_degree_bound = cleared_component_degree_bound(
            excess, components
        )
        sample_start = 7
        sample_count = rational_certificate_point_count(
            excess, components
        )
        sample_sizes = range(sample_start, sample_start + sample_count)
        expected = COMPONENT_POLYNOMIALS[(h, excess, components)]
        if sp.degree(expected, S) > displayed_degree_bound:
            raise AssertionError(
                "displayed component polynomial exceeds its stated degree"
            )
        for sample_s in sample_sizes:
            measured = sp.Rational(
                normalized_component_value(
                    sample_s, h, excess, components
                )
            )
            if sp.cancel(expected.subs(S, sample_s) - measured) != 0:
                raise AssertionError(
                    "denominator-aware component mismatch at "
                    f"{(sample_s, h, excess, components)}"
                )
        rows.append(
            [
                h,
                excess,
                components,
                displayed_degree_bound,
                cleared_degree_bound,
                sample_count,
                str(sp.factor(expected)),
            ]
        )
    return rows


def audit_independent_rational_certificate() -> int:
    """Run the independent direct-position 180-value certificate."""

    from audit_second_raw_enum import audit_rational_certificate_points

    checked = audit_rational_certificate_points()
    if checked != 180:
        raise AssertionError(
            f"independent denominator certificate had {checked} values"
        )
    return checked


def fixed_deficit_endpoint_entries(
    deficit: int,
) -> list[tuple[int, int, int]]:
    """Finite endpoint set needed for B_(2s-5-deficit)."""

    if deficit < 0:
        raise ValueError("deficit must be nonnegative")
    maximum_excess = min(2 * deficit, deficit + 1)
    return [
        (h, excess, components)
        for h in range(3)
        for excess in range(maximum_excess + 1)
        for components in range(1, deficit + 3 - excess)
    ]


def fixed_deficit_endpoint_certificate_points(deficit: int) -> int:
    """Total Abel endpoint values in the fixed-deficit certificate."""

    entries = fixed_deficit_endpoint_entries(deficit)
    measured = sum(
        rational_certificate_point_count(excess, components)
        for _, excess, components in entries
    )
    expected = (
        12
        if deficit == 0
        else (
            (deficit + 2)
            * (deficit + 3)
            * (5 * deficit + 8)
            // 2
        )
    )
    if measured != expected:
        raise AssertionError("fixed-deficit point-count identity failed")
    return measured


def fixed_deficit_coefficient_degree_bound(
    deficit: int, offset: int
) -> int:
    """Degree after clearing the coefficient denominator s**offset.

    If n=2s-5-deficit and

        C_(q,r) = [beta^(2n+r)]B_n /
                  (n!*s^(2s-8-2q+r)),

    then s**r*C_(q,r) has degree at most 2*q+r+2.
    """

    if deficit < 0 or offset < 0 or offset > 2 * deficit:
        raise ValueError("offset must lie between 0 and 2*deficit")
    return 2 * deficit + offset + 2


def fixed_deficit_coefficient_certificate_points(
    deficit: int, offset: int
) -> int:
    """Values sufficient to determine one fixed-deficit coefficient."""

    return (
        fixed_deficit_coefficient_degree_bound(deficit, offset) + 1
    )


def fixed_deficit_boundary_roots(deficit: int) -> tuple[int, ...]:
    """Forced roots of the cleared fixed-deficit coefficient.

    For n=2*s-5-deficit, the algebraically continued master formula
    vanishes when n<0, while the already proved pooled support theorem
    gives B_0=B_1=0.  Hence every cleared numerator R_(q,r) has the
    roots 4,...,floor((q+6)/2).
    """

    if deficit < 0:
        raise ValueError("deficit must be nonnegative")
    largest_root = (deficit + 6) // 2
    return tuple(range(4, largest_root + 1))


def fixed_deficit_reduced_coefficient_certificate_points(
    deficit: int, offset: int
) -> int:
    """Points needed after dividing the proved boundary factor."""

    return (
        fixed_deficit_coefficient_certificate_points(deficit, offset)
        - len(fixed_deficit_boundary_roots(deficit))
    )


def falling(value: sp.Expr, order: int) -> sp.Expr:
    result = sp.Integer(1)
    for index in range(order):
        result *= value - index
    return sp.expand(result)


def normalized_layer_polynomial(offset: int) -> sp.Expr:
    """Return [beta^(2n+r)]B_n/(n!*s^(2s-12+r)), n=2s-7."""

    if offset < 0 or offset > 3:
        raise ValueError("species formula is needed only for offsets 0..3")
    total = sp.Integer(0)
    for overlap in range(offset // 2 + 1):
        remaining = offset - 2 * overlap
        for left_excess in range(remaining + 1):
            for right_excess in range(remaining - left_excess + 1):
                lambda_degree = (
                    remaining - left_excess - right_excess
                )
                lambda_exponent = 3 - overlap
                if lambda_degree > lambda_exponent:
                    continue
                prefactor = sp.Rational(
                    math.comb(lambda_exponent, lambda_degree),
                    math.factorial(overlap),
                )
                component_sum = (
                    5 - overlap - left_excess - right_excess
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
                        positive_left in COMPONENT_POLYNOMIALS
                        and positive_right in COMPONENT_POLYNOMIALS
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
                            * COMPONENT_POLYNOMIALS[positive_left]
                            * COMPONENT_POLYNOMIALS[positive_right]
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
                        negative_left in COMPONENT_POLYNOMIALS
                        and negative_right in COMPONENT_POLYNOMIALS
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
                            * COMPONENT_POLYNOMIALS[negative_left]
                            * COMPONENT_POLYNOMIALS[negative_right]
                        )
                    total += prefactor * (positive - negative)
    return sp.factor(total)


EXPECTED_NORMALIZED_LAYERS = (
    2 * (S - 4) * (S**3 + 12 * S**2 + 20 * S - 225),
    sp.Rational(8, 3)
    * (S - 4)
    * (3 * S**3 + 20 * S**2 - 28 * S - 225),
    4 * (S - 4) * (4 * S**3 + 6 * S**2 - 85 * S + 72),
    8 * (S - 4) * (2 * S - 5) * (S**2 - S - 8),
    sp.Rational(2, 3)
    * (S - 4)
    * (S - 3)
    * (2 * S - 7)
    * (6 * S - 11),
)


def audit_symbolic_layer_formulas() -> list[list[object]]:
    rows: list[list[object]] = []
    for offset in range(4):
        measured = normalized_layer_polynomial(offset)
        expected = sp.factor(EXPECTED_NORMALIZED_LAYERS[offset])
        if sp.cancel(measured - expected) != 0:
            raise AssertionError(f"layer formula mismatch at offset {offset}")
        shifted = sp.Poly(sp.expand(expected.subs(S, U + 5)), U)
        if any(coefficient <= 0 for coefficient in shifted.all_coeffs()):
            raise AssertionError("shifted layer polynomial is not positive")
        rows.append(
            [
                offset,
                str(expected),
                [str(value) for value in reversed(shifted.all_coeffs())],
            ]
        )

    # The fifth coefficient comes from the first-attack Stirling top face.
    top = sp.factor(EXPECTED_NORMALIZED_LAYERS[4])
    shifted_top = sp.Poly(sp.expand(top.subs(S, U + 5)), U)
    if any(coefficient <= 0 for coefficient in shifted_top.all_coeffs()):
        raise AssertionError("shifted top coefficient is not positive")
    for s in range(5, 25):
        depth = 2 * s - 7
        stirling_value = 4 * (
            stirling2(2 * s - 5, depth)
            - stirling2(2 * s - 6, depth)
        )
        if stirling_value != int(top.subs(S, s)):
            raise AssertionError("top Stirling specialization mismatch")
    rows.append(
        [
            4,
            str(top),
            [str(value) for value in reversed(shifted_top.all_coeffs())],
        ]
    )
    return rows


def second_deficit_coefficients(s: int) -> dict[int, int]:
    """The complete five coefficients of B_(2s-7)."""

    depth = 2 * s - 7
    result: dict[int, int] = {}
    for offset, polynomial in enumerate(EXPECTED_NORMALIZED_LAYERS):
        value = (
            math.factorial(depth)
            * integer_power(s, 2 * s - 12 + offset)
            * int(polynomial.subs(S, s))
        )
        if value.denominator != 1:
            raise AssertionError("second-deficit coefficient is fractional")
        result[4 * s - 14 + offset] = value.numerator
    return {degree: value for degree, value in result.items() if value}


def previous_attack_algebra_certificate() -> dict[str, str]:
    """Fill the previously abbreviated component-table simplification."""

    binary = sp.Integer(0)
    for left_components in range(1, 4):
        right_components = 4 - left_components
        binary += 4 * (
            COMPONENT_POLYNOMIALS[(1, 0, left_components)]
            * COMPONENT_POLYNOMIALS[(1, 0, right_components)]
            - COMPONENT_POLYNOMIALS[(0, 0, left_components)]
            * COMPONENT_POLYNOMIALS[(2, 0, right_components)]
        )
    binary = sp.factor(binary)

    ternary = sp.Integer(0)
    for left_excess, right_excess in ((0, 1), (1, 0)):
        component_sum = 3
        for left_components in range(1, component_sum):
            right_components = component_sum - left_components
            ternary += 4 * (
                COMPONENT_POLYNOMIALS[
                    (1, left_excess, left_components)
                ]
                * COMPONENT_POLYNOMIALS[
                    (1, right_excess, right_components)
                ]
                - COMPONENT_POLYNOMIALS[
                    (0, left_excess, left_components)
                ]
                * COMPONENT_POLYNOMIALS[
                    (2, right_excess, right_components)
                ]
            )
    ternary = sp.factor(ternary)

    expected_binary = 4 * (S**2 + 4 * S - 24)
    expected_ternary = -8 * (5 * S - 16)
    if sp.cancel(binary - expected_binary) != 0:
        raise AssertionError("previous binary simplification mismatch")
    if sp.cancel(ternary - expected_ternary) != 0:
        raise AssertionError("previous ternary simplification mismatch")
    return {
        "normalized_C": str(binary),
        "normalized_Q": str(ternary),
        "middle_sum": str(
            sp.factor(2 * expected_binary + expected_ternary)
        ),
    }


def audit_chain_species(
    minimum_s: int = 5, maximum_s: int = 9
) -> int:
    """Compare j!*H_{e,c} with primitive nilpotent-chain coefficients."""

    research_open = Path(__file__).resolve().parents[2]
    primitive_dir = (
        research_open / "q1_eight_hour_campaign_2026-07-29" / "opg1757"
    )
    sys.path.insert(0, str(primitive_dir))
    try:
        from general_s_disjoint_low_degree import truncated_profile_chain
    finally:
        sys.path.pop(0)

    checked = 0
    for s in range(minimum_s, maximum_s + 1):
        max_beta = 2 * s + 3
        for h in range(3):
            profile = tuple(sorted((2,) * h + (1,) * (s - 2 * h)))
            chain = truncated_profile_chain(profile, max_beta)
            for _, excess, components in (
                entry for entry in component_entries() if entry[0] == h
            ):
                order = s - h - components - excess
                degree = 2 * order + excess
                if order < 0 or degree > max_beta:
                    continue
                expected = math.factorial(order) * hyperforest_component_weight(
                    s, h, excess, components
                )
                measured = chain[order][degree]
                if measured != expected:
                    raise AssertionError(
                        f"chain/species mismatch at "
                        f"{(s,h,excess,components)}: "
                        f"{measured} != {expected}"
                    )
                checked += 1
    return checked


def audit_primitive_second_deficit(
    minimum_s: int, maximum_s: int
) -> list[list[int]]:
    rows: list[list[int]] = []
    for s in range(minimum_s, maximum_s + 1):
        depth = 2 * s - 7
        primitive = {
            degree: coefficient
            for (row_depth, degree), coefficient in (
                primitive_pooled_rows(s)
            ).items()
            if row_depth == depth
        }
        expected = second_deficit_coefficients(s)
        if primitive != expected:
            raise AssertionError(
                f"B_(2s-7) mismatch at s={s}: {primitive} != {expected}"
            )
        rows.extend(
            [s, depth, degree, coefficient]
            for degree, coefficient in sorted(expected.items())
        )
    return rows


def build_certificate(
    minimum_s: int = 4, maximum_s: int = 16
) -> dict[str, object]:
    component_rows = audit_component_polynomial_table()
    independent_component_points = (
        audit_independent_rational_certificate()
    )
    symbolic_rows = audit_symbolic_layer_formulas()
    previous = previous_attack_algebra_certificate()
    chain_checks = audit_chain_species()
    primitive_rows = audit_primitive_second_deficit(
        minimum_s, maximum_s
    )
    payload = json.dumps(
        [
            component_rows,
            independent_component_points,
            symbolic_rows,
            previous,
            chain_checks,
            primitive_rows,
        ],
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return {
        "schema": "amra.opg1757.second_depth_deficit.v2",
        "status": "PASS",
        "theorem_status": "PROVED",
        "proved_layer": (
            "B_(2s-7) has five coefficients "
            "(2s-7)!*s^(2s-12+r)*P_r(s), r=0..4"
        ),
        "species": {
            "excess_0": "ordinary binary forests",
            "excess_1": "one ternary hyperedge",
            "excess_2": "one quaternary or two ternary hyperedges",
            "excess_3": (
                "one 5-edge, one 4-edge plus one 3-edge, "
                "or three 3-edges"
            ),
            "overlap": (
                "one active-page overlap contributes for offsets 2 and 3"
            ),
        },
        "component_polynomials": len(component_rows),
        "denominator_aware_component_points": sum(
            row[5] for row in component_rows
        ),
        "independent_denominator_aware_component_points": (
            independent_component_points
        ),
        "largest_component_certificate_s": 16,
        "fixed_deficit_q2_endpoint_count": len(
            fixed_deficit_endpoint_entries(2)
        ),
        "fixed_deficit_q2_point_count": (
            fixed_deficit_endpoint_certificate_points(2)
        ),
        "chain_species_checks": chain_checks,
        "primitive_s_range": [minimum_s, maximum_s],
        "primitive_rows": len(primitive_rows),
        "previous_attack_algebra": previous,
        "normalized_layers": symbolic_rows,
        "scope_firewall": (
            "This proves one complete-split pooled layer.  It does not "
            "prove all B_n or arbitrary-host OPG-1757."
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
