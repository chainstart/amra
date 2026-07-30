#!/usr/bin/env python3
"""All-orders symbolic certificate for the second subleading symbol.

This extends the parameterized Cauchy-saddle calculation by one
inverse-s order.  The variable x remains symbolic throughout; no
finite-loss interpolation is used to establish the identities.
"""

from __future__ import annotations

import json

import sympy as sp

from verify_ordinary_subleading_saddle_certificate import (
    W,
    X,
    exceptional_amplitude_coefficient,
    gaussian_moment,
    phase_derivative,
    polynomial_add,
    polynomial_multiply,
    polynomial_scale,
    primary_amplitude_coefficient,
)


MAXIMUM_RANK = 4


def phase_exponential_polynomials():
    """Return E_0,...,E_8 for the saddle exponential."""

    phase = {
        order: phase_derivative(order)
        for order in range(2, 11)
    }
    terms = [{} for _ in range(2 * MAXIMUM_RANK + 1)]
    for power in range(1, 2 * MAXIMUM_RANK + 1):
        terms[power] = {
            power + 2: (
                phase[power + 2]
                / sp.factorial(power + 2)
            )
        }

    result = [{} for _ in range(2 * MAXIMUM_RANK + 1)]
    result[0] = {0: sp.S.One}
    for degree in range(1, 2 * MAXIMUM_RANK + 1):
        total = {}
        for power in range(1, degree + 1):
            total = polynomial_add(
                total,
                polynomial_scale(
                    polynomial_multiply(
                        terms[power],
                        result[degree - power],
                    ),
                    power,
                ),
            )
        result[degree] = polynomial_scale(
            total, sp.Rational(1, degree)
        )
    return result


PHASE_EXPONENTIAL = phase_exponential_polynomials()


def gamma_exponential(argument_data, maximum_rank):
    """Gamma-prefactor correction through the requested rank."""

    logarithm = [None]
    for order in range(1, maximum_rank + 1):
        value = sum(
            sign
            * sp.bernoulli(order + 1, shift)
            / scale**order
            for sign, scale, shift in argument_data
        )
        logarithm.append(
            sp.factor(
                (-1) ** (order + 1)
                * value
                / (order * (order + 1))
            )
        )

    result = [sp.S.One]
    for degree in range(1, maximum_rank + 1):
        result.append(
            sp.factor(
                sum(
                    order
                    * logarithm[order]
                    * result[degree - order]
                    for order in range(1, degree + 1)
                )
                / degree
            )
        )
    return result


def saddle_correction(amplitude, gamma_arguments, maximum_rank):
    """Relative saddle coefficients through maximum_rank."""

    integral = []
    for rank in range(maximum_rank + 1):
        integral.append(
            sp.factor(
                sum(
                    amplitude(order)
                    * gaussian_moment(
                        PHASE_EXPONENTIAL[
                            2 * rank - order
                        ],
                        order,
                    )
                    for order in range(2 * rank + 1)
                )
            )
        )
    relative_integral = [
        sp.factor(value / integral[0])
        for value in integral
    ]
    gamma = gamma_exponential(
        gamma_arguments, maximum_rank
    )
    return [
        sp.factor(
            sum(
                gamma[index]
                * relative_integral[rank - index]
                for index in range(rank + 1)
            )
        )
        for rank in range(maximum_rank + 1)
    ]


def primary_profile(shift):
    arguments = [
        (1, X, 1),
        (1, 1, 1 - shift),
        (-1, 1 - X, 1 - shift),
    ]
    correction = saddle_correction(
        lambda order: primary_amplitude_coefficient(
            shift, order
        ),
        arguments,
        MAXIMUM_RANK,
    )
    return [
        sp.factor(sp.sqrt(W) * value)
        for value in correction
    ]


def exceptional_profile():
    arguments = [
        (1, X, 1),
        (1, 1, -3),
        (-1, 1 - X, -2),
    ]
    correction = saddle_correction(
        exceptional_amplitude_coefficient,
        arguments,
        MAXIMUM_RANK - 1,
    )
    return [
        sp.factor(8 * X / sp.sqrt(W) * value)
        for value in correction
    ]


def all_profiles():
    primary = {
        shift: primary_profile(shift)
        for shift in (0, 2, 4)
    }
    exceptional = exceptional_profile()
    return [
        primary[0],
        primary[2],
        [
            primary[4][0],
            sp.factor(primary[4][1] + exceptional[0]),
            sp.factor(primary[4][2] + exceptional[1]),
            sp.factor(primary[4][3] + exceptional[2]),
            sp.factor(primary[4][4] + exceptional[3]),
        ],
    ]


def claimed_fourth_profile_symbols():
    """The T_h(x) coefficients of s^-4."""

    numerators = [
        -X
        * (
            146176 * X**11
            - 663552 * X**10
            + 1220352 * X**9
            - 774144 * X**8
            - 736992 * X**7
            + 2750976 * X**6
            - 8160912 * X**5
            + 13685760 * X**4
            + 47385675 * X**3
            - 112674240 * X**2
            + 40091760 * X
            + 17729280
        ),
        X
        * (
            690451712 * X**11
            - 3711086592 * X**10
            + 8894124288 * X**9
            - 12380967936 * X**8
            + 10858590432 * X**7
            - 6111072000 * X**6
            + 2540586384 * X**5
            - 1519300800 * X**4
            + 1006618725 * X**3
            - 199208160 * X**2
            - 73347120 * X
            + 4976640
        ),
        -X
        * (
            38115777280 * X**11
            - 189099147264 * X**10
            + 412563816192 * X**9
            - 516716734464 * X**8
            + 407929881888 * X**7
            - 212168180736 * X**6
            + 75677948784 * X**5
            - 19289301120 * X**4
            + 3340767915 * X**3
            - 487969920 * X**2
            + 184051440 * X
            - 23950080
        ),
    ]
    return [
        numerator
        / (sp.Integer(155520) * W ** sp.Rational(23, 2))
        for numerator in numerators
    ]


def determinant_kernels(profiles):
    t, x = sp.symbols("t x")
    ranks = [
        None,
        [profiles[h][1] for h in range(3)],
        [profiles[h][2] for h in range(3)],
        [profiles[h][3] for h in range(3)],
        [profiles[h][4] for h in range(3)],
    ]

    def profile_term(profile_index, rank, argument):
        if rank == 0:
            return sp.sqrt(1 - 2 * argument)
        return (
            t**rank
            * ranks[rank][profile_index].subs(X, argument)
        )

    def kernel(rank):
        return sp.factor(
            sum(
                profile_term(1, left, t * x)
                * profile_term(1, rank - left, t * (1 - x))
                - profile_term(0, left, t * x)
                * profile_term(2, rank - left, t * (1 - x))
                for left in range(rank + 1)
            )
        )

    return t, x, kernel(2), kernel(3), kernel(4)


def second_subleading_polynomial(depth):
    return (
        286 * depth**6
        + 3546 * depth**5
        + 12721 * depth**4
        - 7812 * depth**3
        - 86231 * depth**2
        + 40338 * depth
        + 209160
    ) / sp.Integer(5184)


def audit():
    profiles = all_profiles()
    claimed_t = claimed_fourth_profile_symbols()
    fourth_profile_checks = []
    for profile_index in range(3):
        difference = sp.simplify(
            profiles[profile_index][4]
            - claimed_t[profile_index]
        )
        assert difference == 0
        fourth_profile_checks.append(True)

    t, x, g2, g3, g4 = determinant_kernels(profiles)
    h4 = sp.factor(
        g4.subs(x, sp.Rational(1, 2))
        + sp.diff(g3, x, 2).subs(
            x, sp.Rational(1, 2)
        )
        / 8
        + sp.diff(g2, x, 4).subs(
            x, sp.Rational(1, 2)
        )
        / 128
    )
    expected_h4 = (
        t**5
        * (
            2389 * t**7
            - 14334 * t**6
            + 34245 * t**5
            - 40008 * t**4
            + 22152 * t**3
            - 5400 * t**2
            + 3672 * t
            + 144
        )
        / (36 * (1 - t) ** 7)
    )
    assert sp.simplify(h4 - expected_h4) == 0

    h2 = 2 * t**4 / (1 - t)
    h3 = (
        -t**4
        * (
            43 * t**4
            - 129 * t**3
            + 108 * t**2
            - 6 * t
            + 6
        )
        / (3 * (1 - t) ** 4)
    )
    coefficient_series = sp.factor(
        (h2 + h3 + h4) / (2 * t**4)
    )
    expected_series = (
        t**2
        * (
            2389 * t**6
            - 13818 * t**5
            + 31221 * t**4
            - 32952 * t**3
            + 14112 * t**2
            - 1116 * t
            + 3024
        )
        / (72 * (1 - t) ** 7)
    )
    assert sp.simplify(
        coefficient_series - expected_series
    ) == 0

    depth = sp.symbols("d")
    base = t**2 / (1 - t)
    generated = sp.S.Zero
    differentiated = base
    coefficients = (
        209160,
        40338,
        -86231,
        -7812,
        12721,
        3546,
        286,
    )
    for degree, coefficient in enumerate(coefficients):
        if degree:
            differentiated = sp.factor(
                t * sp.diff(differentiated, t)
            )
        generated += (
            sp.Rational(coefficient, 5184)
            * differentiated
        )
    assert sp.simplify(
        coefficient_series - generated
    ) == 0

    return {
        "schema": (
            "amra.opg1757."
            "ordinary-second-subleading-all-orders.v1"
        ),
        "status": "all_orders_symbolic_certificate_passed",
        "finite_loss_interpolation": False,
        "maximum_inverse_s_rank": MAXIMUM_RANK,
        "fourth_profile_symbol_identities": len(
            fourth_profile_checks
        ),
        "central_binomial_h4_identity": True,
        "all_depth_generating_function_identity": True,
        "valid_depths": "d>=2",
        "second_subleading_polynomial": str(
            second_subleading_polynomial(depth)
        ),
    }


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2, sort_keys=True))
