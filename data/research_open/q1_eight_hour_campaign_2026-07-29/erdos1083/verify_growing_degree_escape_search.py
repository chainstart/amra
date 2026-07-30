"""Exact growing-degree unit-orbit search for Round 31."""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations
from itertools import product as cartesian_product
from math import prod

import sympy as sp


R = -3069
Y_SQUAREFREE = 1365
Element = tuple[int, ...]
Polynomial = tuple[int, ...]  # low-to-high, monic


def field_add(left: Element, right: Element) -> Element:
    return tuple(a + b for a, b in zip(left, right))


def field_scale(element: Element, scalar: int) -> Element:
    return tuple(scalar * value for value in element)


def field_neg(element: Element) -> Element:
    return field_scale(element, -1)


def field_mul(left: Element, right: Element, polynomial: Polynomial) -> Element:
    """Multiply in Z[theta]=Z[x]/(f), for monic f."""
    degree = len(polynomial) - 1
    work = [0] * (2 * degree - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            work[i + j] += a * b
    for power in range(2 * degree - 2, degree - 1, -1):
        coefficient = work[power]
        if coefficient:
            for index in range(degree):
                work[power - degree + index] -= coefficient * polynomial[index]
    return tuple(work[:degree])


def theta_element(degree: int) -> Element:
    result = [0] * degree
    result[1] = 1
    return tuple(result)


def one_element(degree: int) -> Element:
    return (1,) + (0,) * (degree - 1)


def theta_inverse(polynomial: Polynomial) -> Element:
    """Use f(theta)=0 and constant coefficient +/-1."""
    degree = len(polynomial) - 1
    constant = polynomial[0]
    if abs(constant) != 1:
        raise ValueError("theta is not certified as an algebraic unit")
    # theta^-1=-(theta^(d-1)+a_(d-1)theta^(d-2)+...+a_1)/a_0.
    return tuple(-polynomial[index + 1] // constant for index in range(degree))


def field_pow(base: Element, exponent: int, polynomial: Polynomial) -> Element:
    if exponent < 0:
        raise ValueError("field_pow expects a nonnegative exponent")
    result = one_element(len(base))
    factor = base
    power = exponent
    while power:
        if power & 1:
            result = field_mul(result, factor, polynomial)
        factor = field_mul(factor, factor, polynomial)
        power >>= 1
    return result


def theta_power(exponent: int, polynomial: Polynomial) -> Element:
    degree = len(polynomial) - 1
    base = theta_element(degree) if exponent >= 0 else theta_inverse(polynomial)
    return field_pow(base, abs(exponent), polynomial)


def parameter_shifts(exponent: int, polynomial: Polynomial) -> tuple[Element, Element]:
    """Coordinates of 2u and 2c in the integral power basis.

    The translation GAP uses the half-power basis theta^i/2, so these are
    exactly the integer coordinate shifts of u and c.
    """
    degree = len(polynomial) - 1
    parameter = theta_power(exponent, polynomial)
    inverse = theta_power(-exponent, polynomial)
    constant_three = field_scale(one_element(degree), 3)
    u = field_add(field_add(parameter, field_scale(inverse, R)), constant_three)
    c = field_add(parameter, field_scale(inverse, -R))
    return u, c


def polynomial_expression(polynomial: Polynomial, symbol) -> object:
    return sum(
        coefficient * symbol**power
        for power, coefficient in enumerate(polynomial)
    )


def sparse_unit_polynomials(degree: int) -> tuple[Polynomial, ...]:
    """Small exact model: x^d+a*x^j+/-1, j in {1,d-1}, |a|<=3."""
    symbol = sp.symbols("x")
    candidates = set()
    for position in {1, degree - 1}:
        for coefficient in (-3, -2, -1, 1, 2, 3):
            for constant in (-1, 1):
                values = [0] * (degree + 1)
                values[degree] = 1
                values[position] += coefficient
                values[0] += constant
                candidates.add(tuple(values))

    accepted = []
    for polynomial in sorted(candidates):
        expression = polynomial_expression(polynomial, symbol)
        rational_poly = sp.Poly(expression, symbol)
        if not rational_poly.is_irreducible:
            continue
        if not rational_poly.intervals():
            continue
        extension_poly = sp.Poly(
            expression, symbol, extension=sp.sqrt(Y_SQUAREFREE)
        )
        if not extension_poly.is_irreducible:
            continue
        accepted.append(polynomial)
    return tuple(accepted)


def dense_unit_polynomials(
    degree: int, coefficient_bound: int = 2
) -> tuple[Polynomial, ...]:
    """All monic unit polynomials with bounded interior coefficients."""
    symbol = sp.symbols("x")
    accepted = []
    for constant in (-1, 1):
        for interior in cartesian_product(
            range(-coefficient_bound, coefficient_bound + 1),
            repeat=degree - 1,
        ):
            polynomial = (constant,) + tuple(interior) + (1,)
            expression = polynomial_expression(polynomial, symbol)
            rational_poly = sp.Poly(expression, symbol)
            if not rational_poly.is_irreducible or not rational_poly.intervals():
                continue
            if not sp.Poly(
                expression, symbol, extension=sp.sqrt(Y_SQUAREFREE)
            ).is_irreducible:
                continue
            accepted.append(polynomial)
    return tuple(accepted)


def additive_box_score(
    polynomial: Polynomial, exponents: tuple[int, ...]
) -> dict:
    """Exact lower H for the smallest doubled box supporting the shifts."""
    if not exponents:
        raise ValueError("need at least one parameter")
    degree = len(polynomial) - 1
    curve_points = set()
    raw_parameters = []
    for exponent in exponents:
        u, c = parameter_shifts(exponent, polynomial)
        raw_parameters.append((exponent, u, c))
        curve_points.add((u, c))
        curve_points.add((u, field_neg(c)))

    maxima = [0] * degree
    for u, c in curve_points:
        for index in range(degree):
            maxima[index] = max(maxima[index], abs(u[index]), abs(c[index]))
    sides = tuple(2 * maximum + 1 for maximum in maxima)
    p_size = prod(sides)
    n = 2 * p_size

    extra = 0
    point_records = []
    for u, c in sorted(curve_points):
        overlap_p_u = prod(
            side - abs(coordinate) for side, coordinate in zip(sides, u)
        )
        overlap_p_c = prod(
            side - abs(coordinate) for side, coordinate in zip(sides, c)
        )
        overlap_a_u = 2 * overlap_p_u
        overlap_a_v = overlap_p_c
        contribution = overlap_a_u * overlap_a_v
        extra += contribution
        point_records.append((u, c, contribution))
    total = n * n + extra
    average = Fraction(total, n * n)
    gain = average - 1
    return {
        "polynomial": polynomial,
        "degree": degree,
        "exponents": exponents,
        "raw_parameters": tuple(raw_parameters),
        "distinct_curve_points": len(curve_points),
        "side_lengths": sides,
        "p_size": p_size,
        "n": n,
        "H_lower_bound": total,
        "average_lower_bound": average,
        "nonbaseline_gain": gain,
        "point_records": tuple(point_records),
        "target_ratio_float": float(gain) / float(n ** Fraction(2, 5)),
    }


def optimize_exponent_subsets(
    polynomial: Polynomial, exponent_radius: int = 4
) -> dict:
    pool = tuple(range(-exponent_radius, exponent_radius + 1))
    best_average = None
    best_target = None
    best_target_multi = None
    evaluated = 0
    for size in range(1, len(pool) + 1):
        for exponents in combinations(pool, size):
            result = additive_box_score(polynomial, exponents)
            evaluated += 1
            average_key = (
                result["average_lower_bound"],
                result["target_ratio_float"],
                -result["n"],
            )
            target_key = (
                result["target_ratio_float"],
                result["average_lower_bound"],
                -result["n"],
            )
            if best_average is None or average_key > best_average[0]:
                best_average = (average_key, result)
            if best_target is None or target_key > best_target[0]:
                best_target = (target_key, result)
            if len(exponents) >= 2 and (
                best_target_multi is None or target_key > best_target_multi[0]
            ):
                best_target_multi = (target_key, result)
    return {
        "evaluated_subsets": evaluated,
        "best": best_average[1],
        "best_target": best_target[1],
        "best_target_multi": best_target_multi[1],
    }


def growing_degree_search(
    minimum_degree: int = 3,
    maximum_degree: int = 8,
    exponent_radius: int = 4,
) -> dict:
    records = []
    degree_summary = {}
    for degree in range(minimum_degree, maximum_degree + 1):
        polynomials = sparse_unit_polynomials(degree)
        degree_records = []
        degree_target_records = []
        degree_multi_records = []
        for polynomial in polynomials:
            optimized = optimize_exponent_subsets(polynomial, exponent_radius)
            record = optimized["best"]
            record["evaluated_subsets"] = optimized["evaluated_subsets"]
            target_record = optimized["best_target"]
            degree_records.append(record)
            degree_target_records.append(target_record)
            degree_multi_records.append(optimized["best_target_multi"])
            records.append(record)
        best = max(
            degree_records,
            key=lambda item: (
                item["average_lower_bound"],
                item["target_ratio_float"],
            ),
        )
        degree_summary[degree] = {
            "polynomial_count": len(polynomials),
            "best": best,
            "best_target": max(
                degree_target_records,
                key=lambda item: item["target_ratio_float"],
            ),
            "best_target_multi": max(
                degree_multi_records,
                key=lambda item: item["target_ratio_float"],
            ),
        }
    overall = max(
        records,
        key=lambda item: (
            item["average_lower_bound"],
            item["target_ratio_float"],
        ),
    )
    return {
        "degree_range": (minimum_degree, maximum_degree),
        "exponent_radius": exponent_radius,
        "degree_summary": degree_summary,
        "overall_best": overall,
        "overall_best_target": max(
            (
                summary["best_target"]
                for summary in degree_summary.values()
            ),
            key=lambda item: item["target_ratio_float"],
        ),
        "overall_best_target_multi": max(
            (
                summary["best_target_multi"]
                for summary in degree_summary.values()
            ),
            key=lambda item: item["target_ratio_float"],
        ),
        "total_polynomials": len(records),
        "total_subsets": sum(item["evaluated_subsets"] for item in records),
    }


def exhaustive_cubic_quartic_search(
    coefficient_bound: int = 2, exponent_radius: int = 4
) -> dict:
    """Exhaust every bounded-coefficient cubic and quartic in the model."""
    summary = {}
    all_records = []
    for degree in (3, 4):
        polynomials = dense_unit_polynomials(degree, coefficient_bound)
        records = []
        target_records = []
        multi_records = []
        for polynomial in polynomials:
            optimized = optimize_exponent_subsets(polynomial, exponent_radius)
            record = optimized["best"]
            record["evaluated_subsets"] = optimized["evaluated_subsets"]
            records.append(record)
            all_records.append(record)
            target_records.append(optimized["best_target"])
            multi_records.append(optimized["best_target_multi"])
        summary[degree] = {
            "polynomial_count": len(polynomials),
            "best": max(
                records,
                key=lambda item: (
                    item["average_lower_bound"],
                    item["target_ratio_float"],
                ),
            ),
            "best_target": max(
                target_records,
                key=lambda item: item["target_ratio_float"],
            ),
            "best_target_multi": max(
                multi_records,
                key=lambda item: item["target_ratio_float"],
            ),
        }
    return {
        "coefficient_bound": coefficient_bound,
        "exponent_radius": exponent_radius,
        "degree_summary": summary,
        "total_polynomials": len(all_records),
        "total_subsets": sum(item["evaluated_subsets"] for item in all_records),
        "overall_best": max(
            all_records,
            key=lambda item: (
                item["average_lower_bound"],
                item["target_ratio_float"],
            ),
        ),
        "overall_best_target": max(
            (
                summary["best_target"]
                for summary in summary.values()
            ),
            key=lambda item: item["target_ratio_float"],
        ),
        "overall_best_target_multi": max(
            (
                degree_record["best_target_multi"]
                for degree_record in summary.values()
            ),
            key=lambda item: item["target_ratio_float"],
        ),
    }


if __name__ == "__main__":
    result = growing_degree_search()
    print(
        "degrees", result["degree_range"],
        "polynomials", result["total_polynomials"],
        "subsets", result["total_subsets"],
    )
    for degree, summary in result["degree_summary"].items():
        best = summary["best"]
        print(
            degree,
            "polynomials=", summary["polynomial_count"],
            "average=", best["average_lower_bound"],
            "n=", best["n"],
            "exponents=", best["exponents"],
            "f=", best["polynomial"],
            "target ratio=", best["target_ratio_float"],
        )
        target = summary["best_target"]
        print(
            "target-best", degree,
            "ratio=", target["target_ratio_float"],
            "average=", target["average_lower_bound"],
            "n=", target["n"],
            "exponents=", target["exponents"],
            "f=", target["polynomial"],
        )
        multi = summary["best_target_multi"]
        print(
            "multi-target-best", degree,
            "ratio=", multi["target_ratio_float"],
            "average=", multi["average_lower_bound"],
            "n=", multi["n"],
            "exponents=", multi["exponents"],
            "f=", multi["polynomial"],
        )
    dense = exhaustive_cubic_quartic_search()
    print(
        "dense cubic/quartic",
        "polynomials", dense["total_polynomials"],
        "subsets", dense["total_subsets"],
    )
    for degree, summary in dense["degree_summary"].items():
        best = summary["best"]
        print(
            "dense", degree,
            "polynomials=", summary["polynomial_count"],
            "average=", best["average_lower_bound"],
            "n=", best["n"],
            "exponents=", best["exponents"],
            "f=", best["polynomial"],
            "target ratio=", best["target_ratio_float"],
        )
        target = summary["best_target"]
        print(
            "dense-target-best", degree,
            "ratio=", target["target_ratio_float"],
            "average=", target["average_lower_bound"],
            "n=", target["n"],
            "exponents=", target["exponents"],
            "f=", target["polynomial"],
        )
        multi = summary["best_target_multi"]
        print(
            "dense-multi-target-best", degree,
            "ratio=", multi["target_ratio_float"],
            "average=", multi["average_lower_bound"],
            "n=", multi["n"],
            "exponents=", multi["exponents"],
            "f=", multi["polynomial"],
        )
