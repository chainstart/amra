#!/usr/bin/env python3
"""Audit the general-k low-beta defect formulas and leading-F evidence."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
from collections import Counter, defaultdict
from functools import lru_cache
from pathlib import Path

import sympy as sp

from five_page_union_formula import (
    k3_coefficients,
    k4_coefficients,
    k5_coefficients,
)
from seven_page_union_formula import k7_coefficients
from six_page_union_formula import k6_coefficients


K, S, H = sp.symbols("k s h", integer=True, positive=True)


def choose2(value: sp.Expr) -> sp.Expr:
    return value * (value - 1) / 2


def choose3(value: sp.Expr) -> sp.Expr:
    return value * (value - 1) * (value - 2) / 6


def integer_choose(top: int, lower: int) -> int:
    return math.prod(top - offset for offset in range(lower)) // math.factorial(
        lower
    )


def defect_expressions() -> dict[str, sp.Expr]:
    ones = S - 2 * H
    q = choose2(ones) + 4 * H * ones + 16 * choose2(H)
    t = 2 * choose2(ones) + 12 * H * ones + 64 * choose2(H)
    u = 10 * choose2(ones) + 92 * H * ones + 640 * choose2(H)
    v = choose2(ones) + 8 * H * ones + 64 * choose2(H)
    w = (
        choose3(ones)
        + 4 * H * choose2(ones)
        + 16 * choose2(H) * ones
    )
    edge_e2 = ((K * S) ** 2 - K * (S + 2 * H)) / 2
    c4 = choose2(K) * q
    r5 = choose2(K) * (K * S * q - 2 * t)
    r6 = (
        choose2(K) * (edge_e2 * q - 2 * K * S * t + u)
        - 2 * choose3(K) * v
        + (6 * choose3(K) - 2 * choose2(K)) * w
    )
    return {
        "q": sp.expand(q),
        "t": sp.expand(t),
        "u": sp.expand(u),
        "v": sp.expand(v),
        "w": sp.expand(w),
        "edge_e2": sp.expand(edge_e2),
        "c4": sp.expand(c4),
        "r5": sp.expand(r5),
        "r6": sp.expand(r6),
    }


def second_difference(expression: sp.Expr) -> sp.Expr:
    return sp.expand(
        expression.subs(H, 0)
        + expression.subs(H, 2)
        - 2 * expression.subs(H, 1)
    )


def reduced_coefficients() -> tuple[sp.Expr, sp.Expr, sp.Expr]:
    expressions = defect_expressions()
    c4 = expressions["c4"]
    r5 = expressions["r5"]
    r6 = expressions["r6"]
    edge_e2 = expressions["edge_e2"]
    d4 = second_difference(c4)
    d5 = second_difference(r5) + K * S * d4
    d6 = (
        second_difference(r6)
        + K * S * second_difference(r5)
        + c4.subs(H, 0) * edge_e2.subs(H, 2)
        + c4.subs(H, 2) * edge_e2.subs(H, 0)
        - 2 * c4.subs(H, 1) * edge_e2.subs(H, 1)
    )
    exponent = 2 * S - 2 * K - 2
    n4 = sp.factor(d4)
    n5 = sp.factor(sp.expand(d5 - exponent * K * n4))
    n6 = sp.factor(
        sp.expand(
            d6
            - exponent * K * n5
            - exponent * (exponent - 1) * K**2 * n4 / 2
        )
    )
    return n4, n5, n6


def is_forest(
    core_count: int,
    page_count: int,
    selected_edges: tuple[tuple[int, int, int], ...],
) -> bool:
    parent = list(range(core_count + page_count))

    def find(vertex: int) -> int:
        while parent[vertex] != vertex:
            parent[vertex] = parent[parent[vertex]]
            vertex = parent[vertex]
        return vertex

    for core, page, _ in selected_edges:
        left = find(core)
        right = find(core_count + page)
        if left == right:
            return False
        parent[left] = right
    return True


def brute_low_forest_coefficients(
    s: int,
    page_count: int,
    two_blocks: int,
    maximum_degree: int = 6,
) -> list[int]:
    weights = [2] * two_blocks + [1] * (s - 2 * two_blocks)
    edges = [
        (core, page, weight)
        for core, weight in enumerate(weights)
        for page in range(page_count)
    ]
    coefficients = [1]
    for degree in range(1, maximum_degree + 1):
        total = 0
        for selected in itertools.combinations(edges, degree):
            if is_forest(len(weights), page_count, selected):
                total += math.prod(edge[2] for edge in selected)
        coefficients.append(total)
    return coefficients


def predicted_low_forest_coefficients(
    s: int, page_count: int, two_blocks: int
) -> list[int]:
    weights = [2] * two_blocks + [1] * (s - 2 * two_blocks)
    edge_weights = [
        weight for weight in weights for _ in range(page_count)
    ]
    elementary = [1]
    row = [1] + [0] * 6
    for weight in edge_weights:
        for degree in range(6, 0, -1):
            row[degree] += weight * row[degree - 1]
    elementary.extend(row[1:])
    expressions = defect_expressions()
    substitutions = {S: s, K: page_count, H: two_blocks}
    return (
        elementary[:4]
        + [
            elementary[4] - int(expressions["c4"].subs(substitutions)),
            elementary[5] - int(expressions["r5"].subs(substitutions)),
            elementary[6] - int(expressions["r6"].subs(substitutions)),
        ]
    )


def complete_graph_forest_coefficients(
    weights: list[int], maximum_degree: int
) -> list[int]:
    edges = [
        (left, right, weights[left] * weights[right])
        for left in range(len(weights))
        for right in range(left + 1, len(weights))
    ]
    coefficients: list[int] = []
    for degree in range(maximum_degree + 1):
        total = 0
        for selected in itertools.combinations(edges, degree):
            parent = list(range(len(weights)))

            def find(vertex: int) -> int:
                while parent[vertex] != vertex:
                    parent[vertex] = parent[parent[vertex]]
                    vertex = parent[vertex]
                return vertex

            valid = True
            for left, right, _ in selected:
                left_root = find(left)
                right_root = find(right)
                if left_root == right_root:
                    valid = False
                    break
                parent[left_root] = right_root
            if valid:
                total += math.prod(edge[2] for edge in selected)
        coefficients.append(total)
    return coefficients


def weighted_tree_component(twos: int, ones: int) -> int:
    size = twos + ones
    if size == 1:
        return 1
    return 2**twos * (2 * twos + ones) ** (size - 2)


@lru_cache(maxsize=None)
def complete_graph_forest_dp(
    twos: int, ones: int, maximum_degree: int
) -> tuple[int, ...]:
    if twos + ones == 0:
        return (1, *([0] * maximum_degree))
    coefficients = [0] * (maximum_degree + 1)
    if ones:
        for component_twos in range(twos + 1):
            for other_ones in range(ones):
                degree = component_twos + other_ones
                if degree > maximum_degree:
                    continue
                multiplier = (
                    math.comb(twos, component_twos)
                    * math.comb(ones - 1, other_ones)
                    * weighted_tree_component(
                        component_twos, other_ones + 1
                    )
                )
                remainder = complete_graph_forest_dp(
                    twos - component_twos,
                    ones - other_ones - 1,
                    maximum_degree - degree,
                )
                for remainder_degree, value in enumerate(remainder):
                    coefficients[degree + remainder_degree] += (
                        multiplier * value
                    )
    else:
        for other_twos in range(twos):
            degree = other_twos
            if degree > maximum_degree:
                continue
            multiplier = math.comb(twos - 1, other_twos) * (
                weighted_tree_component(other_twos + 1, 0)
            )
            remainder = complete_graph_forest_dp(
                twos - other_twos - 1,
                0,
                maximum_degree - degree,
            )
            for remainder_degree, value in enumerate(remainder):
                coefficients[degree + remainder_degree] += multiplier * value
    return tuple(coefficients)


def leading_f_from_complete_graph(page_count: int, s: int) -> int:
    forest_rows = [
        complete_graph_forest_dp(
            h,
            s - 2 * h,
            page_count,
        )
        for h in range(3)
    ]
    determinant = sum(
        forest_rows[1][left] * forest_rows[1][page_count - left]
        - forest_rows[0][left] * forest_rows[2][page_count - left]
        for left in range(page_count + 1)
    )
    numerator = math.factorial(page_count) * determinant
    denominator = 2 * page_count * (page_count - 1)
    if numerator % denominator:
        raise AssertionError("complete-graph leading coefficient not integral")
    return numerator // denominator


def forward_differences(values: list[int]) -> list[int]:
    coefficients: list[int] = []
    current = values
    while current:
        coefficients.append(current[0])
        current = [
            current[index + 1] - current[index]
            for index in range(len(current) - 1)
        ]
    return coefficients


def saved_kernel_coefficients(page_count: int, s: int) -> list[int]:
    return [
        int(value)
        for value in {
            2: [1, 0, 0],
            3: k3_coefficients(s),
            4: k4_coefficients(s),
            5: k5_coefficients(s),
            6: k6_coefficients(s),
            7: k7_coefficients(s),
        }[page_count][:3]
    ]


def symbolic_kernel_coefficients(page_count: int) -> list[sp.Expr]:
    return list(
        {
            2: [sp.S.One],
            3: k3_coefficients(S),
            4: k4_coefficients(S),
            5: k5_coefficients(S),
            6: k6_coefficients(S),
            7: k7_coefficients(S),
        }[page_count]
    )


def powered_linear_coefficient(
    base: sp.Expr, exponent: sp.Expr, degree: int
) -> sp.Expr:
    if degree < 0:
        return sp.S.Zero
    return sp.expand_func(sp.binomial(exponent, degree)) * base**degree


def f_coefficient(page_count: int, degree: int) -> sp.Expr:
    total = sp.S.Zero
    for actual_pages in range(2, page_count + 1):
        kernel = symbolic_kernel_coefficients(actual_pages)
        multiplier = (
            (-1) ** (page_count - actual_pages)
            * math.comb(page_count - 2, actual_pages - 2)
        )
        for lambda_degree in range(2 * (page_count - actual_pages) + 1):
            for kernel_degree, kernel_coefficient in enumerate(kernel):
                remaining = degree - lambda_degree - kernel_degree
                if remaining < 0:
                    continue
                total += (
                    multiplier
                    * powered_linear_coefficient(
                        S,
                        2 * (page_count - actual_pages),
                        lambda_degree,
                    )
                    * powered_linear_coefficient(
                        actual_pages,
                        2 * S - 2 * actual_pages - 2,
                        remaining,
                    )
                    * kernel_coefficient
                )
    return sp.factor(sp.expand(sp.expand_func(total)))


@lru_cache(maxsize=None)
def page_partition_choices(
    profile: tuple[int, ...],
) -> tuple[tuple[int, int, tuple[int, ...]], ...]:
    counts = sorted(Counter(profile).items())
    rows: list[tuple[int, int, tuple[int, ...]]] = []

    def visit(
        index: int,
        selected_counts: tuple[int, ...],
        remaining: list[int],
        multiplicity: int,
    ) -> None:
        if index == len(counts):
            selected = sum(selected_counts)
            if selected < 2:
                destination = profile
            else:
                merged_size = sum(
                    size * chosen
                    for (size, _), chosen in zip(counts, selected_counts)
                )
                destination = tuple(sorted((*remaining, merged_size)))
            rows.append((selected, multiplicity, destination))
            return
        size, count = counts[index]
        for chosen in range(count + 1):
            visit(
                index + 1,
                (*selected_counts, chosen),
                remaining + [size] * (count - chosen),
                multiplicity
                * math.comb(count, chosen)
                * size**chosen,
            )

    visit(0, (), [], 1)
    return tuple(rows)


def truncated_page_profile_polynomial(
    s: int, page_count: int, two_blocks: int, maximum_degree: int = 7
) -> list[int]:
    vector: dict[tuple[tuple[int, ...], int], int] = {
        ((1,) * page_count, 0): 1
    }
    for weight in [2] * two_blocks + [1] * (s - 2 * two_blocks):
        following: defaultdict[tuple[tuple[int, ...], int], int] = defaultdict(
            int
        )
        for (profile, old_degree), coefficient in vector.items():
            for degree, multiplicity, destination in page_partition_choices(
                profile
            ):
                if old_degree + degree <= maximum_degree:
                    following[(destination, old_degree + degree)] += (
                        coefficient * multiplicity * weight**degree
                    )
        vector = dict(following)
    return [
        sum(
            coefficient
            for (_, degree), coefficient in vector.items()
            if degree == target
        )
        for target in range(maximum_degree + 1)
    ]


def reduced_beta7_numerator(s: int, page_count: int) -> int:
    maximum_degree = 7
    profiles = [
        truncated_page_profile_polynomial(
            s, page_count, two_blocks, maximum_degree
        )
        for two_blocks in range(3)
    ]
    determinant = [
        sum(
            profiles[1][left] * profiles[1][degree - left]
            - profiles[0][left] * profiles[2][degree - left]
            for left in range(degree + 1)
        )
        for degree in range(maximum_degree + 1)
    ]
    exponent = 2 * s - 2 * page_count - 2
    reduced: list[int] = []
    for degree in range(4, maximum_degree + 1):
        value = determinant[degree]
        for power in range(1, degree - 3):
            value -= (
                integer_choose(exponent, power)
                * page_count**power
                * reduced[degree - 4 - power]
            )
        reduced.append(value)
    return reduced[3]


def reduced_beta_numerator_from_profiles(
    profiles: list[list[int]],
    s: int,
    page_count: int,
    target_degree: int,
) -> int:
    determinant = [
        sum(
            profiles[1][left] * profiles[1][degree - left]
            - profiles[0][left] * profiles[2][degree - left]
            for left in range(degree + 1)
        )
        for degree in range(target_degree + 1)
    ]
    exponent = 2 * s - 2 * page_count - 2
    reduced: list[int] = []
    for degree in range(4, target_degree + 1):
        value = determinant[degree]
        for power in range(1, degree - 3):
            value -= (
                integer_choose(exponent, power)
                * page_count**power
                * reduced[degree - 4 - power]
            )
        reduced.append(value)
    return reduced[-1]


def reduced_beta_numerator(
    s: int, page_count: int, target_degree: int
) -> int:
    profiles = [
        truncated_page_profile_polynomial(
            s, page_count, two_blocks, target_degree
        )
        for two_blocks in range(3)
    ]
    return reduced_beta_numerator_from_profiles(
        profiles, s, page_count, target_degree
    )


def expected_beta3_numerator(s: int, page_count: int) -> int:
    first = (
        3 * page_count**3
        + 11 * page_count**2
        - 11 * page_count
        - 105
    )
    second = (
        2 * page_count**4
        + 13 * page_count**3
        + 18 * page_count**2
        - 96 * page_count
        - 300
    )
    numerator = (
        4
        * page_count
        * (page_count - 1)
        * (page_count - 2)
        * (first * s + (page_count - 3) * second)
    )
    if numerator % 3:
        raise AssertionError("beta^3 numerator formula is not integral")
    return numerator // 3


def expected_beta4_numerator(s: int, page_count: int) -> int:
    k = page_count
    polynomial = (
        4 * k**7
        + 12 * k**6
        + 12 * k**5 * s
        - 73 * k**5
        + 46 * k**4 * s
        - 507 * k**4
        + 3 * k**3 * s**2
        - 105 * k**3 * s
        + 54 * k**3
        + 12 * k**2 * s**2
        - 1036 * k**2 * s
        + 6672 * k**2
        - 6 * k * s**2
        - 531 * k * s
        + 5868 * k
        - 135 * s**2
        + 7110 * s
        - 37800
    )
    numerator = k * (k - 1) * (k - 2) * polynomial
    if numerator % 3:
        raise AssertionError("beta^4 numerator formula is not integral")
    return numerator // 3


def build_audit() -> dict[str, object]:
    n4, n5, n6 = reduced_coefficients()
    expected = (
        2 * K * (K - 1),
        4 * K * (K - 1) * (K - 2) * (K + 3),
        2
        * K
        * (K - 1)
        * (K - 2)
        * (
            (K + 3) * S
            + 2 * K**3
            + 7 * K**2
            - 9 * K
            - 60
        ),
    )
    if any(
        sp.expand(actual - target) != 0
        for actual, target in zip((n4, n5, n6), expected)
    ):
        raise AssertionError("general reduced low coefficient failed")

    brute_rows: list[list[object]] = []
    for page_count in range(2, 5):
        for s in range(4, 7):
            for two_blocks in range(3):
                if 2 * two_blocks > s:
                    continue
                brute = brute_low_forest_coefficients(
                    s, page_count, two_blocks
                )
                predicted = predicted_low_forest_coefficients(
                    s, page_count, two_blocks
                )
                if brute != predicted:
                    raise AssertionError("cycle-defect classification failed")
                brute_rows.append(
                    [page_count, s, two_blocks, [str(value) for value in brute]]
                )

    kernel_rows: list[list[object]] = []
    for page_count in range(2, 8):
        for s in (page_count + 3, page_count + 4):
            expected_kernel = [
                1,
                2 * (page_count - 2) * (page_count + 3),
                (page_count - 2)
                * (
                    (page_count + 3) * s
                    + 2 * page_count**3
                    + 7 * page_count**2
                    - 9 * page_count
                    - 60
                ),
            ]
            saved = saved_kernel_coefficients(page_count, s)
            if saved != expected_kernel:
                raise AssertionError("saved K_k low coefficient failed")
            kernel_rows.append([page_count, s, [str(value) for value in saved]])

    f_rows: list[list[object]] = []
    for page_count in range(2, 8):
        first_degree = 2 * (page_count - 2)
        lower = [f_coefficient(page_count, degree) for degree in range(first_degree)]
        if any(value != 0 for value in lower):
            raise AssertionError("F_k lower support cancellation failed")
        leading = f_coefficient(page_count, first_degree)
        if sp.Poly(leading, S).degree() != first_degree:
            raise AssertionError("F_k leading coefficient degree failed")
        if sp.Poly(leading, S).LC() != 1:
            raise AssertionError("F_k leading coefficient is not monic")
        f_rows.append([page_count, first_degree, str(leading)])

    core_rows: list[list[object]] = []
    for page_count in range(2, 6):
        s = page_count + 3
        forest_rows = [
            complete_graph_forest_coefficients(
                [2] * h + [1] * (s - 2 * h),
                page_count,
            )
            for h in range(3)
        ]
        determinant_coefficient = sum(
            forest_rows[1][left] * forest_rows[1][page_count - left]
            - forest_rows[0][left] * forest_rows[2][page_count - left]
            for left in range(page_count + 1)
        )
        extracted = (
            math.factorial(page_count)
            * determinant_coefficient
            // (2 * page_count * (page_count - 1))
        )
        expected_leading = int(
            f_coefficient(page_count, 2 * (page_count - 2)).subs(S, s)
        )
        if extracted != expected_leading:
            raise AssertionError("minimal-mask complete-graph formula failed")
        core_rows.append(
            [page_count, s, str(determinant_coefficient), str(extracted)]
        )

    beta3_rows: list[list[object]] = []
    for page_count in range(9):
        for s in range(4, 12):
            actual = reduced_beta7_numerator(s, page_count)
            expected_value = expected_beta3_numerator(s, page_count)
            if actual != expected_value:
                raise AssertionError("general beta^3 K_k grid identity failed")
            beta3_rows.append([page_count, s, str(actual)])

    beta4_rows: list[list[object]] = []
    for page_count in range(11):
        for s in range(4, 13):
            actual = reduced_beta_numerator(s, page_count, 8)
            expected_value = expected_beta4_numerator(s, page_count)
            if actual != expected_value:
                raise AssertionError("general beta^4 K_k grid identity failed")
            beta4_rows.append([page_count, s, str(actual)])

    beta4_brute_rows: list[list[object]] = []
    for page_count, s in ((2, 4), (3, 4), (3, 5), (4, 4)):
        brute_profiles = [
            brute_low_forest_coefficients(
                s, page_count, two_blocks, maximum_degree=8
            )
            for two_blocks in range(3)
        ]
        actual = reduced_beta_numerator_from_profiles(
            brute_profiles, s, page_count, 8
        )
        expected_value = expected_beta4_numerator(s, page_count)
        if actual != expected_value:
            raise AssertionError("independent beta^4 edge-subset check failed")
        beta4_brute_rows.append([page_count, s, str(actual)])

    beta4_saved_rows: list[list[object]] = []
    for page_count in range(3, 8):
        for s in (max(page_count, 4), page_count + 3):
            saved = int(symbolic_kernel_coefficients(page_count)[4].subs(S, s))
            numerator = expected_beta4_numerator(s, page_count)
            expected_value = numerator // (2 * page_count * (page_count - 1))
            if saved != expected_value:
                raise AssertionError("saved beta^4 K_k crosscheck failed")
            beta4_saved_rows.append([page_count, s, str(saved)])

    leading_newton_rows: list[list[object]] = []
    for page_count in range(2, 13):
        base_s = max(page_count, 4)
        polynomial_degree = 2 * page_count - 4
        values = [
            leading_f_from_complete_graph(page_count, base_s + offset)
            for offset in range(polynomial_degree + 1)
        ]
        newton_coefficients = forward_differences(values)
        if any(value < 0 for value in newton_coefficients):
            raise AssertionError("allowed F-leading Newton coefficient failed")
        if newton_coefficients[-1] != math.factorial(polynomial_degree):
            raise AssertionError("F-leading monic endpoint failed")
        leading_newton_rows.append(
            [
                page_count,
                base_s,
                [str(value) for value in newton_coefficients],
            ]
        )
    invalid_k3_s3 = int(f_coefficient(3, 2).subs(S, 3))
    if invalid_k3_s3 != -6:
        raise AssertionError("the excluded k=3,s=3 diagnostic changed")

    payload = json.dumps(
        [
            brute_rows,
            kernel_rows,
            f_rows,
            core_rows,
            beta3_rows,
            beta4_rows,
            beta4_brute_rows,
            beta4_saved_rows,
            leading_newton_rows,
        ],
        separators=(",", ":"),
    ).encode("utf-8")
    return {
        "schema": "amra.complete_split.general_k_low_coefficients.v1",
        "theorem": {
            "K_beta0": "1",
            "K_beta1": "2*(k-2)*(k+3)",
            "K_beta2": (
                "(k-2)*((k+3)*s+2*k^3+7*k^2-9*k-60)"
            ),
            "K_beta3": (
                "2*(k-2)/3*((3*k^3+11*k^2-11*k-105)*s"
                "+(k-3)*(2*k^4+13*k^3+18*k^2-96*k-300))"
            ),
            "K_beta4": (
                "(k-2)/6*(4*k^7+12*k^6+12*k^5*s-73*k^5"
                "+46*k^4*s-507*k^4+3*k^3*s^2-105*k^3*s"
                "+54*k^3+12*k^2*s^2-1036*k^2*s+6672*k^2"
                "-6*k*s^2-531*k*s+5868*k-135*s^2+7110*s"
                "-37800)"
            ),
            "positivity_form_k_m_plus_3": (
                "K_beta2=(m+1)*(m*s+6*s+2*m^3+25*m^2+87*m+30), "
                "m=k-3>=0; k=2 is zero."
            ),
        },
        "brute_cycle_classification_rows": brute_rows,
        "saved_kernel_crosscheck_rows": kernel_rows,
        "finite_F_support_crosscheck_rows": f_rows,
        "minimal_mask_complete_graph_rows": core_rows,
        "beta3_exact_interpolation_rows": beta3_rows,
        "beta3_interpolation_proof": (
            "A beta^7 pair of page-core forests mentions at most seven "
            "page labels and seven core labels, so its count has exact "
            "binomial-basis degree at most 7 in each population. The "
            "three deconvolution steps give degree at most 8 in k and 7 "
            "in s for the reduced numerator. The exact 9-by-8 grid "
            "therefore proves the displayed identity, not merely tests it."
        ),
        "beta4_exact_interpolation_rows": beta4_rows,
        "beta4_interpolation_proof": (
            "A beta^8 pair of page-core forests mentions at most eight "
            "page labels and eight core labels, so the raw determinant "
            "has exact binomial-basis degree at most 8 in each population. "
            "Using the already proved degrees of reduced numerators "
            "n4,n5,n6,n7, the fourth deconvolution step has degree at "
            "most 10 in k and 8 in s. The exact 11-by-9 grid therefore "
            "determines the displayed beta^4 identity. Its actual "
            "degrees are 10 and 2."
        ),
        "beta4_independent_edge_subset_rows": beta4_brute_rows,
        "beta4_saved_formula_crosscheck_rows": beta4_saved_rows,
        "F_leading_newton_rows_k2_to_k12": leading_newton_rows,
        "F_leading_excluded_k3_s3": str(invalid_k3_s3),
        "F_leading_scope": (
            "All Newton coefficients about s0=max(k,4) are nonnegative "
            "for k=2..12. This is finite evidence, not the still-missing "
            "general positive injection. The only negative base value "
            "encountered is k=s=3, outside the disjoint-core-edge domain "
            "s>=4."
        ),
        "general_F_support_proof": (
            "At pooled Newton order n=j+q-overlap, each of the j+q "
            "nilpotent page steps has beta degree at least 2. Hence "
            "d>=2(j+q)=2(n+overlap)>=2n. For B_k this gives d>=2k, "
            "and after the universal beta^4 factor, F_k starts no earlier "
            "than beta^(2(k-2)). Fresh-label minimal-mask objects make "
            "the first coefficient monic of s-degree 2(k-2), so it is "
            "not the zero polynomial."
        ),
        "sha256_payload": hashlib.sha256(payload).hexdigest(),
        "status": "proved",
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    audit = build_audit()
    rendered = json.dumps(audit, indent=2, sort_keys=True)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + "\n", encoding="utf-8")
        print(f"wrote {args.output}")
    else:
        print(rendered)


if __name__ == "__main__":
    main()
