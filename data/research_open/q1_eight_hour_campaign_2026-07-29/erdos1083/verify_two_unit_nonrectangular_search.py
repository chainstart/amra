"""Exact quartic two-unit and one-shear container search for Round 32."""

from __future__ import annotations

from fractions import Fraction
from functools import lru_cache
from itertools import product
from math import prod

import sympy as sp

from verify_growing_degree_escape_search import (
    Element,
    Polynomial,
    dense_unit_polynomials,
    field_add,
    field_mul,
    field_neg,
    field_scale,
    one_element,
    theta_element,
)


R = -3069


@lru_cache(maxsize=None)
def multiplication_matrix(element: Element, polynomial: Polynomial) -> sp.Matrix:
    degree = len(element)
    theta = theta_element(degree)
    columns = []
    power = one_element(degree)
    for _ in range(degree):
        columns.append(field_mul(element, power, polynomial))
        power = field_mul(power, theta, polynomial)
    return sp.Matrix(
        degree,
        degree,
        lambda row, column: columns[column][row],
    )


@lru_cache(maxsize=None)
def element_norm(element: Element, polynomial: Polynomial) -> int:
    return int(multiplication_matrix(element, polynomial).det())


@lru_cache(maxsize=None)
def element_inverse(element: Element, polynomial: Polynomial) -> Element:
    matrix = multiplication_matrix(element, polynomial)
    if abs(int(matrix.det())) != 1:
        raise ValueError("element is not an integral unit")
    solution = matrix.inv() * sp.Matrix(one_element(len(element)))
    return tuple(int(value) for value in solution)


@lru_cache(maxsize=None)
def element_pow(
    element: Element, exponent: int, polynomial: Polynomial
) -> Element:
    if exponent < 0:
        element = element_inverse(element, polynomial)
        exponent = -exponent
    result = one_element(len(element))
    factor = element
    while exponent:
        if exponent & 1:
            result = field_mul(result, factor, polynomial)
        factor = field_mul(factor, factor, polynomial)
        exponent >>= 1
    return result


@lru_cache(maxsize=None)
def unit_word(
    first: Element,
    second: Element,
    exponents: tuple[int, int],
    polynomial: Polynomial,
) -> Element:
    left = element_pow(first, exponents[0], polynomial)
    right = element_pow(second, exponents[1], polynomial)
    return field_mul(left, right, polynomial)


def bounded_word_independent(
    first: Element,
    second: Element,
    polynomial: Polynomial,
    radius: int = 2,
) -> bool:
    words = {
        unit_word(first, second, (a, b), polynomial)
        for a in range(-radius, radius + 1)
        for b in range(-radius, radius + 1)
    }
    return len(words) == (2 * radius + 1) ** 2


def small_second_units(
    polynomial: Polynomial,
    coefficient_bound: int = 1,
    maximum: int = 2,
) -> tuple[Element, ...]:
    degree = len(polynomial) - 1
    theta = theta_element(degree)
    candidates = []
    for element in product(
        range(-coefficient_bound, coefficient_bound + 1), repeat=degree
    ):
        if element == (0,) * degree:
            continue
        if abs(element_norm(element, polynomial)) != 1:
            continue
        # This excludes every multiplicative relation
        # theta^a*element^b=1 with |a|,|b|<=6.  It is an exact finite
        # independence certificate, not a claim of global independence.
        if not bounded_word_independent(theta, element, polynomial, radius=6):
            continue
        candidates.append(tuple(element))
    candidates.sort(key=lambda item: (sum(abs(value) for value in item), item))
    return tuple(candidates[:maximum])


@lru_cache(maxsize=None)
def word_parameter_shifts(
    parameter: Element, polynomial: Polynomial
) -> tuple[Element, Element]:
    inverse = element_inverse(parameter, polynomial)
    constant_three = field_scale(one_element(len(parameter)), 3)
    u = field_add(
        field_add(parameter, field_scale(inverse, R)), constant_three
    )
    c = field_add(parameter, field_scale(inverse, -R))
    return u, c


def elementary_shears(degree: int) -> tuple[tuple[int, int, int] | None, ...]:
    return (None,) + tuple(
        (target, source, sign)
        for target in range(degree)
        for source in range(degree)
        if target != source
        for sign in (-1, 1)
    )


def apply_shear(
    vector: Element, shear: tuple[int, int, int] | None
) -> Element:
    if shear is None:
        return vector
    target, source, sign = shear
    result = list(vector)
    result[target] += sign * result[source]
    return tuple(result)


def exponent_rank_two(exponents: tuple[tuple[int, int], ...]) -> bool:
    return any(
        left[0] * right[1] - left[1] * right[0] != 0
        for index, left in enumerate(exponents)
        for right in exponents[index + 1 :]
    )


def score_word_subset(
    polynomial: Polynomial,
    first: Element,
    second: Element,
    exponent_subset: tuple[tuple[int, int], ...],
    use_elementary_shears: bool = True,
) -> dict:
    if not exponent_rank_two(exponent_subset):
        raise ValueError("the selected words must span exponent rank two")
    parameters = tuple(
        (
            exponents,
            unit_word(first, second, exponents, polynomial),
        )
        for exponents in exponent_subset
    )
    raw_points = set()
    for _, parameter in parameters:
        u, c = word_parameter_shifts(parameter, polynomial)
        raw_points.add((u, c))
        raw_points.add((u, field_neg(c)))

    best = None
    shear_family = (
        elementary_shears(len(first))
        if use_elementary_shears
        else (None,)
    )
    for shear in shear_family:
        points = tuple(
            (apply_shear(u, shear), apply_shear(c, shear))
            for u, c in raw_points
        )
        maxima = [
            max(
                max(abs(u[index]), abs(c[index]))
                for u, c in points
            )
            for index in range(len(first))
        ]
        sides = tuple(2 * maximum + 1 for maximum in maxima)
        p_size = prod(sides)
        n = 2 * p_size
        extra = 0
        for u, c in points:
            overlap_p_u = prod(
                side - abs(value) for side, value in zip(sides, u)
            )
            overlap_p_c = prod(
                side - abs(value) for side, value in zip(sides, c)
            )
            extra += 2 * overlap_p_u * overlap_p_c
        average = 1 + Fraction(extra, n * n)
        target_ratio = float(average - 1) / float(n ** Fraction(2, 5))
        record = {
            "polynomial": polynomial,
            "first_unit": first,
            "second_unit": second,
            "exponent_subset": exponent_subset,
            "distinct_curve_points": len(points),
            "shear": shear,
            "side_lengths": sides,
            "n": n,
            "H_lower_bound": n * n + extra,
            "average_lower_bound": average,
            "target_ratio_float": target_ratio,
        }
        key = (target_ratio, average, -n)
        if best is None or key > best[0]:
            best = (key, record)
    return best[1]


def optimize_two_unit_pair(
    polynomial: Polynomial,
    second_unit: Element,
    word_radius: int = 1,
    shear_finalists_per_objective: int = 32,
) -> dict:
    first = theta_element(len(polynomial) - 1)
    word_pool = tuple(
        (a, b)
        for a in range(-word_radius, word_radius + 1)
        for b in range(-word_radius, word_radius + 1)
    )
    rectangular_records = []
    evaluated = 0
    for mask in range(1, 1 << len(word_pool)):
        subset = tuple(
            word_pool[index]
            for index in range(len(word_pool))
            if mask & (1 << index)
        )
        if not exponent_rank_two(subset):
            continue
        record = score_word_subset(
            polynomial,
            first,
            second_unit,
            subset,
            use_elementary_shears=False,
        )
        evaluated += 1
        rectangular_records.append(record)

    target_finalists = sorted(
        rectangular_records,
        key=lambda record: (
            record["target_ratio_float"],
            record["average_lower_bound"],
            -record["n"],
        ),
        reverse=True,
    )[:shear_finalists_per_objective]
    average_finalists = sorted(
        rectangular_records,
        key=lambda record: (
            record["average_lower_bound"],
            record["target_ratio_float"],
            -record["n"],
        ),
        reverse=True,
    )[:shear_finalists_per_objective]
    finalist_subsets = {
        record["exponent_subset"]
        for record in target_finalists + average_finalists
    }
    refined = [
        score_word_subset(
            polynomial,
            first,
            second_unit,
            subset,
            use_elementary_shears=True,
        )
        for subset in finalist_subsets
    ]
    rectangular_by_subset = {
        record["exponent_subset"]: record for record in rectangular_records
    }
    for record in refined:
        rectangular = rectangular_by_subset[record["exponent_subset"]]
        record["rectangular_n"] = rectangular["n"]
        record["rectangular_average"] = rectangular["average_lower_bound"]
        record["rectangular_target_ratio"] = rectangular["target_ratio_float"]
    best_target = max(
        refined,
        key=lambda record: (
            record["target_ratio_float"],
            record["average_lower_bound"],
            -record["n"],
        ),
    )
    best_average = max(
        refined,
        key=lambda record: (
            record["average_lower_bound"],
            record["target_ratio_float"],
            -record["n"],
        ),
    )
    return {
        "evaluated_rank_two_subsets": evaluated,
        "shear_refined_subsets": len(refined),
        "best_target": best_target,
        "best_average": best_average,
    }


@lru_cache(maxsize=None)
def quartic_two_unit_search(
    coefficient_bound: int = 2,
    units_per_field: int = 2,
    word_radius: int = 1,
) -> dict:
    field_records = []
    pair_records = []
    skipped_no_unit = 0
    for polynomial in dense_unit_polynomials(4, coefficient_bound):
        units = small_second_units(
            polynomial, coefficient_bound=1, maximum=units_per_field
        )
        if not units:
            skipped_no_unit += 1
            continue
        current = []
        for second_unit in units:
            optimized = optimize_two_unit_pair(
                polynomial, second_unit, word_radius
            )
            record = {
                "polynomial": polynomial,
                "second_unit": second_unit,
                **optimized,
            }
            current.append(record)
            pair_records.append(record)
        field_records.append(
            {
                "polynomial": polynomial,
                "unit_count_used": len(units),
                "best_target": max(
                    (item["best_target"] for item in current),
                    key=lambda item: item["target_ratio_float"],
                ),
            }
        )
    return {
        "coefficient_bound": coefficient_bound,
        "word_radius": word_radius,
        "accepted_fields": len(dense_unit_polynomials(4, coefficient_bound)),
        "searched_fields": len(field_records),
        "skipped_no_unit": skipped_no_unit,
        "unit_pairs": len(pair_records),
        "rank_two_subsets": sum(
            item["evaluated_rank_two_subsets"] for item in pair_records
        ),
        "shear_refined_subsets": sum(
            item["shear_refined_subsets"] for item in pair_records
        ),
        "overall_best_target": max(
            (item["best_target"] for item in pair_records),
            key=lambda item: item["target_ratio_float"],
        ),
        "overall_best_average": max(
            (item["best_average"] for item in pair_records),
            key=lambda item: item["average_lower_bound"],
        ),
        "field_records": tuple(field_records),
    }


if __name__ == "__main__":
    result = quartic_two_unit_search()
    print(
        "fields", result["searched_fields"],
        "unit pairs", result["unit_pairs"],
        "rank-two subsets", result["rank_two_subsets"],
    )
    for label in ("overall_best_target", "overall_best_average"):
        best = result[label]
        print(
            label,
            "f=", best["polynomial"],
            "unit2=", best["second_unit"],
            "words=", best["exponent_subset"],
            "shear=", best["shear"],
            "n=", best["n"],
            "average=", best["average_lower_bound"],
            "target ratio=", best["target_ratio_float"],
            "rectangular ratio=", best["rectangular_target_ratio"],
        )
