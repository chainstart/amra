#!/usr/bin/env python3
"""Exact audit for the all-orders diagonal component theorem."""

from __future__ import annotations

import argparse
import json
import math
from fractions import Fraction
from functools import lru_cache

import sympy as sp


RVAR = sp.symbols("R")
XVAR = sp.symbols("x")


def convolution(
    left: tuple[Fraction, ...],
    right: tuple[Fraction, ...],
    maximum_degree: int,
) -> tuple[Fraction, ...]:
    return tuple(
        sum(
            (left[index] * right[degree - index]
             for index in range(degree + 1)),
            Fraction(0),
        )
        for degree in range(maximum_degree + 1)
    )


def product_series(
    low: int,
    high: int,
    maximum_degree: int,
) -> tuple[Fraction, ...]:
    result = [Fraction(1)] + [Fraction(0)] * maximum_degree
    for value in range(low, high + 1):
        for degree in range(maximum_degree, 0, -1):
            result[degree] -= value * result[degree - 1]
    return tuple(result)


class ComponentSeries:
    def __init__(self, maximum_degree: int):
        self.maximum_degree = maximum_degree

    @lru_cache(maxsize=None)
    def f0(self, r: int) -> tuple[Fraction, ...]:
        result = [Fraction(0)] * (self.maximum_degree + 1)
        c = r + 1
        for index in range(c):
            scalar = Fraction(
                (-1) ** index * (c + index),
                2**index
                * math.factorial(index)
                * math.factorial(c - index - 1),
            )
            product = product_series(
                1, c + index - 1, self.maximum_degree
            )
            for degree in range(self.maximum_degree + 1):
                result[degree] += scalar * product[degree]
        g = Fraction(1, 2**r * math.factorial(r))
        return tuple(value / g for value in result)

    @lru_cache(maxsize=None)
    def adjacent(self, r: int) -> tuple[Fraction, ...]:
        result = [Fraction(0)] * (self.maximum_degree + 1)
        c = r + 1
        for index in range(c):
            scalar = Fraction(
                (-1) ** index * (c + index + 2),
                2**index
                * math.factorial(index)
                * math.factorial(c - index - 1),
            )
            product = product_series(
                3, c + index + 1, self.maximum_degree
            )
            for degree in range(self.maximum_degree + 1):
                result[degree] += scalar * product[degree]
        g = Fraction(1, 2**r * math.factorial(r))
        return tuple(value / g for value in result)

    @lru_cache(maxsize=None)
    def f1(self, r: int) -> tuple[Fraction, ...]:
        # 2(1-r*u/(1-u)).
        multiplier = (Fraction(1),) + tuple(
            -Fraction(r) for _ in range(self.maximum_degree)
        )
        return tuple(
            2 * value
            for value in convolution(
                self.f0(r), multiplier, self.maximum_degree
            )
        )

    @lru_cache(maxsize=None)
    def f2(self, r: int) -> tuple[Fraction, ...]:
        inverse_1 = tuple(
            Fraction(1) for _ in range(self.maximum_degree + 1)
        )
        inverse_2 = tuple(
            Fraction(2**degree)
            for degree in range(self.maximum_degree + 1)
        )
        inverse_3 = tuple(
            Fraction(3**degree)
            for degree in range(self.maximum_degree + 1)
        )
        denominator = convolution(
            convolution(
                inverse_1, inverse_2, self.maximum_degree
            ),
            inverse_3,
            self.maximum_degree,
        )
        numerator = (
            Fraction(1),
            -Fraction(2 * r + 3),
            Fraction((r + 1) * (r + 2)),
        ) + tuple(
            Fraction(0) for _ in range(self.maximum_degree - 2)
        )
        first = convolution(
            convolution(
                numerator, denominator, self.maximum_degree
            ),
            self.f0(r),
            self.maximum_degree,
        )
        adjacent_over_n_minus_three = (
            Fraction(0),
        ) + convolution(
            inverse_3, self.adjacent(r), self.maximum_degree
        )[:-1]
        return tuple(
            4 * first[degree]
            - 4 * adjacent_over_n_minus_three[degree]
            for degree in range(self.maximum_degree + 1)
        )


def interpolate_component(
    series: ComponentSeries,
    function_name: str,
    degree: int,
) -> sp.Poly:
    function = getattr(series, function_name)
    points = []
    for r in range(degree + 4):
        value = function(r)[degree]
        points.append(
            (r, sp.Rational(value.numerator, value.denominator))
        )
    polynomial = sp.Poly(sp.interpolate(points, RVAR), RVAR)
    for r in range(degree + 4, degree + 8):
        value = function(r)[degree]
        assert polynomial.eval(r) == sp.Rational(
            value.numerator, value.denominator
        )
    assert polynomial.degree() <= degree
    return polynomial


def symbol_formulas() -> dict[str, tuple[sp.Expr, sp.Expr]]:
    leading = {
        "f0": (1 - 2 * XVAR) ** sp.Rational(-5, 2),
        "f1": (
            2 * (1 - XVAR)
            * (1 - 2 * XVAR) ** sp.Rational(-5, 2)
        ),
        "f2": (
            4 * (1 - XVAR) ** 2
            * (1 - 2 * XVAR) ** sp.Rational(-5, 2)
        ),
    }
    subleading = {
        "f0": (
            XVAR**2
            * (
                -sp.Rational(47, 2)
                + 24 * XVAR
                - sp.Rational(2, 3) * XVAR**2
            )
            * (1 - 2 * XVAR) ** sp.Rational(-11, 2)
        ),
        "f1": (
            XVAR**2
            * (
                -49
                + 107 * XVAR
                - sp.Rational(220, 3) * XVAR**2
                + sp.Rational(52, 3) * XVAR**3
            )
            * (1 - 2 * XVAR) ** sp.Rational(-11, 2)
        ),
        "f2": (
            XVAR**2
            * (
                -114
                + 428 * XVAR
                - sp.Rational(2018, 3) * XVAR**2
                + sp.Rational(1648, 3) * XVAR**3
                - sp.Rational(584, 3) * XVAR**4
            )
            * (1 - 2 * XVAR) ** sp.Rational(-11, 2)
        ),
    }
    return {
        name: (leading[name], subleading[name])
        for name in leading
    }


def determinant_coefficient(
    series: ComponentSeries,
    total_excess: int,
    degree: int,
) -> Fraction:
    result = Fraction(0)
    for r in range(total_excess + 1):
        s = total_excess - r
        first = convolution(
            series.f1(r), series.f1(s), series.maximum_degree
        )[degree]
        second = convolution(
            series.f0(r), series.f2(s), series.maximum_degree
        )[degree]
        result += (
            Fraction(math.comb(total_excess, r), 2**total_excess)
            * (first - second)
        )
    return result


def audit(maximum_degree: int = 7) -> dict[str, object]:
    if maximum_degree < 2:
        raise ValueError("maximum_degree must be at least two")
    series = ComponentSeries(maximum_degree)
    formulas = symbol_formulas()

    component_checks = []
    for function_name in ("f0", "f1", "f2"):
        leading, subleading = formulas[function_name]
        for degree in range(maximum_degree + 1):
            polynomial = interpolate_component(
                series, function_name, degree
            )
            expected_leading = sp.series(
                leading, XVAR, 0, maximum_degree + 1
            ).removeO().expand().coeff(XVAR, degree)
            assert polynomial.coeff_monomial(
                RVAR**degree
            ) == expected_leading
            if degree >= 1:
                expected_subleading = sp.series(
                    subleading, XVAR, 0, maximum_degree + 1
                ).removeO().expand().coeff(XVAR, degree)
                assert polynomial.coeff_monomial(
                    RVAR ** (degree - 1)
                ) == expected_subleading
            component_checks.append((function_name, degree))

    determinant_polynomials = {}
    for degree in range(maximum_degree + 1):
        points = []
        for total_excess in range(2 * maximum_degree + 8):
            value = determinant_coefficient(
                series, total_excess, degree
            )
            points.append(
                (
                    total_excess,
                    sp.Rational(value.numerator, value.denominator),
                )
            )
        polynomial = sp.Poly(sp.interpolate(points, RVAR), RVAR)
        if degree < 2:
            assert polynomial.is_zero
        else:
            assert polynomial.degree() == degree - 1
            assert polynomial.LC() == sp.Rational(
                2 * degree * (degree * degree - 1), 3
            )
        determinant_polynomials[degree] = str(
            sp.factor(polynomial.as_expr())
        )

    assert determinant_polynomials[2] == "4*R"
    assert determinant_polynomials[3] == "16*R*(R - 1)"
    assert determinant_polynomials[4] == "8*R*(R - 1)*(5*R - 22)"
    assert determinant_polynomials[5] == (
        "10*R*(R - 2)*(R - 1)*(8*R - 85)"
    )

    return {
        "schema": "amra.opg1757.diagonal-component.v1",
        "scope": (
            "Finite symbolic audit of an all-orders heat-operator "
            "theorem; checked orders are not the proof of the all-d "
            "claim."
        ),
        "maximum_checked_order": maximum_degree,
        "component_polynomial_checks": len(component_checks),
        "determinant_polynomials": determinant_polynomials,
        "all_orders_leading_coefficient": "(2/3)*d*(d^2-1)",
        "uniform_growing_depth_positivity": "open_gap",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--maximum-degree", type=int, default=7)
    args = parser.parse_args()
    print(
        json.dumps(
            audit(args.maximum_degree),
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
