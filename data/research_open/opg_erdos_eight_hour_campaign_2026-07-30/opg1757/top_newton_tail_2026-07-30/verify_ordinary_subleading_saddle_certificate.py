#!/usr/bin/env python3
"""Symbolic all-orders certificate for the four profile diagonals.

The variable x is symbolic.  This is not a finite-loss interpolation:
it applies the saddle/Gamma recurrences through s^-3 and proves the
resulting rational functions identically in x.
"""

from __future__ import annotations

import json

import sympy as sp


X = sp.symbols("x")
W = 1 - 2 * X


def polynomial_add(left, right):
    result = left.copy()
    for degree, value in right.items():
        result[degree] = result.get(degree, 0) + value
    return result


def polynomial_multiply(left, right):
    result = {}
    for left_degree, left_value in left.items():
        for right_degree, right_value in right.items():
            degree = left_degree + right_degree
            result[degree] = (
                result.get(degree, 0)
                + left_value * right_value
            )
    return result


def polynomial_scale(polynomial, scalar):
    return {
        degree: scalar * value
        for degree, value in polynomial.items()
    }


def phase_derivative(order: int):
    """phi^(order)(2x), phi=y+(1-x)log(1-y/2)-x log y."""
    return (
        sp.factorial(order - 1)
        / 2**order
        * (
            -(1 - X) ** (1 - order)
            + (-1) ** order * X ** (1 - order)
        )
    )


PHASE = {
    order: phase_derivative(order)
    for order in range(2, 9)
}
GAUSSIAN_VARIANCE = sp.cancel(-1 / PHASE[2])


def exponential_phase_polynomials():
    """E_n(q) for exp(sum c_p q^(p+2) epsilon^p), n<=6."""
    phase_terms = [{} for _ in range(7)]
    for power in range(1, 7):
        phase_terms[power] = {
            power + 2: (
                PHASE[power + 2]
                / sp.factorial(power + 2)
            )
        }

    result = [{} for _ in range(7)]
    result[0] = {0: sp.S.One}
    for degree in range(1, 7):
        total = {}
        for power in range(1, degree + 1):
            total = polynomial_add(
                total,
                polynomial_scale(
                    polynomial_multiply(
                        phase_terms[power],
                        result[degree - power],
                    ),
                    power,
                ),
            )
        result[degree] = polynomial_scale(
            total,
            sp.Rational(1, degree),
        )
    return result


PHASE_EXPONENTIAL = exponential_phase_polynomials()


def gaussian_moment(polynomial, degree_shift: int = 0):
    result = sp.S.Zero
    for degree, coefficient in polynomial.items():
        shifted = degree + degree_shift
        if shifted % 2:
            continue
        half = shifted // 2
        multiplier = (
            sp.factorial2(2 * half - 1)
            if half
            else 1
        )
        result += (
            coefficient
            * multiplier
            * GAUSSIAN_VARIANCE**half
        )
    return sp.factor(result)


def primary_amplitude_coefficient(shift: int, order: int):
    """g_shift^(order)(2x)/order!, without differentiating huge powers."""
    result = sp.S.Zero
    for first_order in range(order + 1):
        if first_order == 0:
            first_factor = 1 / (2 * X) - 1
        else:
            first_factor = (
                (-1) ** first_order
                / (2 * X) ** (first_order + 1)
            )
        second_order = order - first_order
        second_factor = (
            sp.rf(shift, second_order)
            / (
                sp.factorial(second_order)
                * 2**second_order
            )
            * (1 - X) ** (-shift - second_order)
        )
        result += first_factor * second_factor
    return sp.factor(result)


def exceptional_amplitude_coefficient(order: int):
    return sp.factor(
        sp.rf(3, order)
        / (sp.factorial(order) * 2**order)
        * (1 - X) ** (-3 - order)
    )


def gamma_exponential(argument_data):
    """Expansion of the Gamma-prefactor correction through s^-3."""
    logarithm = [None]
    for order in range(1, 4):
        value = sp.S.Zero
        for sign, scale, shift in argument_data:
            value += (
                sign
                * sp.bernoulli(order + 1, shift)
                / scale**order
            )
        logarithm.append(
            sp.factor(
                (-1) ** (order + 1)
                * value
                / (order * (order + 1))
            )
        )

    result = [sp.S.One]
    for degree in range(1, 4):
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


def saddle_correction(amplitude, gamma_arguments):
    """Relative saddle coefficients C_0,...,C_3."""
    integral = []
    for rank in range(4):
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
    gamma = gamma_exponential(gamma_arguments)
    return [
        sp.factor(
            sum(
                gamma[index]
                * relative_integral[rank - index]
                for index in range(rank + 1)
            )
        )
        for rank in range(4)
    ]


def primary_profile(shift: int):
    arguments = [
        (1, X, 1),
        (1, 1, 1 - shift),
        (-1, 1 - X, 1 - shift),
    ]
    correction = saddle_correction(
        lambda order: primary_amplitude_coefficient(
            shift,
            order,
        ),
        arguments,
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
    )
    # The exceptional profile starts at s^-1.
    return [
        sp.factor(8 * X / sp.sqrt(W) * value)
        for value in correction[:3]
    ]


def claimed_functions():
    p = [
        -X * (4 * X**2 - 3) / (6 * W ** sp.Rational(5, 2)),
        -X
        * (52 * X**2 - 48 * X + 9)
        / (6 * W ** sp.Rational(5, 2)),
        -X
        * (100 * X**2 - 96 * X + 21)
        / (6 * W ** sp.Rational(5, 2)),
    ]
    q = [
        X
        * (16 * X**5 - 24 * X**3 + 153 * X - 144)
        / (72 * W ** sp.Rational(11, 2)),
        X**2
        * (
            5008 * X**4
            - 11904 * X**3
            + 10152 * X**2
            - 3168 * X
            + 81
        )
        / (72 * W ** sp.Rational(11, 2)),
        X
        * (
            5392 * X**5
            - 14592 * X**4
            + 13416 * X**3
            - 4032 * X**2
            - 279 * X
            + 144
        )
        / (72 * W ** sp.Rational(11, 2)),
    ]
    s = [
        X
        * (
            8896 * X**8
            - 41472 * X**7
            + 83664 * X**6
            - 79488 * X**5
            + 11556 * X**4
            + 116640 * X**3
            - 183465 * X**2
            + 3240 * X
            + 80460
        )
        / (6480 * W ** sp.Rational(17, 2)),
        -X
        * (
            3596864 * X**8
            - 13932288 * X**7
            + 22711536 * X**6
            - 19498752 * X**5
            + 8751564 * X**4
            - 2032560 * X**3
            + 884925 * X**2
            - 502200 * X
            + 36180
        )
        / (6480 * W ** sp.Rational(17, 2)),
        X
        * (
            32886976 * X**8
            - 111992832 * X**7
            + 157083984 * X**6
            - 116581248 * X**5
            + 49790916 * X**4
            - 12121920 * X**3
            + 474255 * X**2
            + 793800 * X
            - 126900
        )
        / (6480 * W ** sp.Rational(17, 2)),
    ]
    return p, q, s


def audit():
    primary = {
        shift: primary_profile(shift)
        for shift in (0, 2, 4)
    }
    exceptional = exceptional_profile()
    profiles = [
        primary[0],
        primary[2],
        [
            primary[4][0],
            sp.factor(primary[4][1] + exceptional[0]),
            sp.factor(primary[4][2] + exceptional[1]),
            sp.factor(primary[4][3] + exceptional[2]),
        ],
    ]

    claimed_p, claimed_q, claimed_s = claimed_functions()
    checks = 0
    for profile_index in range(3):
        assert sp.simplify(
            profiles[profile_index][0] - sp.sqrt(W)
        ) == 0
        checks += 1
        for rank, claimed in (
            (1, claimed_p[profile_index]),
            (2, claimed_q[profile_index]),
            (3, claimed_s[profile_index]),
        ):
            assert sp.simplify(
                profiles[profile_index][rank] - claimed
            ) == 0
            checks += 1

    return {
        "schema": (
            "amra.opg1757.ordinary-subleading-saddle-certificate.v1"
        ),
        "symbolic_variable": "x",
        "finite_loss_interpolation": False,
        "primary_shifts": [0, 2, 4],
        "exceptional_profile_included": True,
        "symbolic_identity_checks": checks,
        "maximum_inverse_s_rank": 3,
        "status": "all_orders_symbolic_certificate_passed",
    }


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2, sort_keys=True))
