#!/usr/bin/env python3
"""Symbolic Bell-jet certificate for the all-rank MD2 cancellation."""

from __future__ import annotations

import json

import sympy as sp


W, A, R, Y = sp.symbols(
    "W a r y",
    integer=True,
    positive=True,
)
X = (1 - W) / 2


def phase_derivative(order: int):
    return (
        sp.factorial(order - 1)
        / 2**order
        * (
            -(1 - X) ** (1 - order)
            + (-1) ** order * X ** (1 - order)
        )
    )


SIGMA = sp.factor(-1 / phase_derivative(2))
PHASE = {
    index: sp.factor(
        phase_derivative(index + 2) / sp.factorial(index + 2)
    )
    for index in range(1, 6)
}


def factorial_ratio(n1, rank=R):
    """Return (2*rank)!/n1! for a small nonnegative difference."""
    difference = int(sp.expand(2 * rank - n1))
    return sp.prod(2 * rank - offset for offset in range(difference))


def double_factorial_ratio(half_degree, rank=R):
    """Return (2h-1)!!/(6*rank-1)!! for a small h-3*rank."""
    difference = int(sp.expand(half_degree - 3 * rank))
    if difference < 0:
        return 1 / sp.prod(
            6 * rank - (2 * offset + 1)
            for offset in range(-difference)
        )
    return sp.prod(
        6 * rank + (2 * offset + 1)
        for offset in range(difference)
    )


def main_integral_jets():
    """Enumerate every main saddle/Bell configuration of defect <= 4."""
    amplitude = (1 - Y) / Y * (1 - Y / 2) ** (-A)
    amplitudes = [
        sp.factor(
            sp.diff(amplitude, Y, order).subs(Y, 2 * X)
            / sp.factorial(order)
        )
        for order in range(6)
    ]
    baseline_amplitude = amplitudes[0]

    configurations = []
    total_ratio = sp.S.Zero
    for amplitude_order in range(6):
        for number_p2 in range(3):
            for number_p3 in range(3):
                for number_p4 in range(2):
                    for number_p5 in range(2):
                        defect = (
                            (
                                0
                                if amplitude_order == 0
                                else amplitude_order - 1
                            )
                            + 2 * number_p2
                            + 2 * number_p3
                            + 4 * number_p4
                            + 4 * number_p5
                        )
                        if defect > 4:
                            continue

                        phase_rank = 2 * R - amplitude_order
                        number_p1 = (
                            phase_rank
                            - 2 * number_p2
                            - 3 * number_p3
                            - 4 * number_p4
                            - 5 * number_p5
                        )
                        number_of_parts = (
                            number_p1
                            + number_p2
                            + number_p3
                            + number_p4
                            + number_p5
                        )
                        half_degree = sp.expand(R + number_of_parts)
                        ratio = (
                            amplitudes[amplitude_order]
                            / baseline_amplitude
                            * PHASE[1] ** (number_p1 - 2 * R)
                            * PHASE[2] ** number_p2
                            * PHASE[3] ** number_p3
                            * PHASE[4] ** number_p4
                            * PHASE[5] ** number_p5
                            * factorial_ratio(number_p1)
                            * double_factorial_ratio(half_degree)
                            * SIGMA ** (half_degree - 3 * R)
                        )
                        total_ratio += ratio
                        configurations.append(
                            [
                                amplitude_order,
                                number_p2,
                                number_p3,
                                number_p4,
                                number_p5,
                                defect,
                            ]
                        )

    ratio_series = sp.series(total_ratio, W, 0, 5).removeO().expand()

    # After removing W^(-3r) and K_r, the baseline phase factor is
    # ((1+W^2)^2/(1-W^2))^r.
    baseline_series = sp.series(
        ((1 + W**2) ** 2 / (1 - W**2)) ** R,
        W,
        0,
        5,
    ).removeO()
    combined = sp.expand(ratio_series * baseline_series)
    integral_jets = [
        sp.factor(sp.cancel(combined.coeff(W, degree)))
        for degree in range(5)
    ]
    return configurations, integral_jets


def exceptional_integral_jets():
    """Enumerate the exceptional internal correction through defect two."""
    internal_rank = R - 1
    amplitude = (1 - Y / 2) ** (-3)
    amplitudes = [
        sp.factor(
            sp.diff(amplitude, Y, order).subs(Y, 2 * X)
            / sp.factorial(order)
        )
        for order in range(3)
    ]
    baseline_amplitude = amplitudes[0]

    total_ratio = sp.S.Zero
    configurations = []
    for amplitude_order in range(3):
        for number_p2 in range(2):
            for number_p3 in range(2):
                defect = (
                    amplitude_order
                    + 2 * number_p2
                    + 2 * number_p3
                )
                if defect > 2:
                    continue
                phase_rank = 2 * internal_rank - amplitude_order
                number_p1 = (
                    phase_rank - 2 * number_p2 - 3 * number_p3
                )
                number_of_parts = number_p1 + number_p2 + number_p3
                half_degree = sp.expand(
                    internal_rank + number_of_parts
                )
                ratio = (
                    amplitudes[amplitude_order]
                    / baseline_amplitude
                    * PHASE[1] ** (number_p1 - 2 * internal_rank)
                    * PHASE[2] ** number_p2
                    * PHASE[3] ** number_p3
                    * factorial_ratio(number_p1, internal_rank)
                    * double_factorial_ratio(
                        half_degree,
                        internal_rank,
                    )
                    * SIGMA ** (half_degree - 3 * internal_rank)
                )
                total_ratio += ratio
                configurations.append(
                    [
                        amplitude_order,
                        number_p2,
                        number_p3,
                        defect,
                    ]
                )

    ratio_series = sp.series(total_ratio, W, 0, 3).removeO()
    baseline_series = sp.series(
        ((1 + W**2) ** 2 / (1 - W**2)) ** internal_rank,
        W,
        0,
        3,
    ).removeO()
    combined = sp.expand(ratio_series * baseline_series)
    return configurations, [
        sp.factor(sp.cancel(combined.coeff(W, degree)))
        for degree in range(3)
    ]


def claimed_main_jets():
    c0 = -1 / (6 * R - 1)
    c1 = sp.S.Zero
    c2 = (
        3
        * R
        * (6 * R + 10 * A**2 - 10 * A - 1)
        / (10 * (6 * R - 5) * (6 * R - 1))
    )

    # The integral part of c3 is followed by the only Gamma term that
    # can occur within pole defect three.
    integral_c3 = (
        6
        * R
        * A
        * (A - 1)
        * (2 * R * A - 4 * R - 2 * A + 5)
        / ((6 * R - 7) * (6 * R - 5) * (6 * R - 1))
    )
    gamma_one_at_zero = sp.Rational(1, 12) + A / 2 - A**2 / 2
    preceding_rank_ratio = (
        6
        * R
        / ((6 * R - 1) * (6 * R - 5) * (6 * R - 7))
    )
    c3 = sp.factor(
        integral_c3 + gamma_one_at_zero * preceding_rank_ratio
    )
    return [sp.factor(value) for value in (c0, c1, c2, c3)]


def second_shift_difference(expression):
    return sp.factor(
        expression.subs(A, 4)
        - 2 * expression.subs(A, 2)
        + expression.subs(A, 0)
    )


def audit() -> dict[str, object]:
    configurations, integral_jets = main_integral_jets()
    main_jets = claimed_main_jets()

    # c0,c1,c2 come entirely from the integral.  For c3 remove the
    # explicitly displayed rank-(r-1) Gamma contribution.
    gamma_one_at_zero = sp.Rational(1, 12) + A / 2 - A**2 / 2
    preceding_rank_ratio = (
        6
        * R
        / ((6 * R - 1) * (6 * R - 5) * (6 * R - 7))
    )
    expected_integral = list(main_jets)
    expected_integral[3] = sp.factor(
        main_jets[3] - gamma_one_at_zero * preceding_rank_ratio
    )
    if any(
        sp.cancel(actual - expected) != 0
        for actual, expected in zip(integral_jets[:4], expected_integral)
    ):
        raise AssertionError("Bell-configuration jet extraction failed")

    # At defect four, Gamma rank one enters through its linear W jet.
    gamma_one_linear = A**2 - A + sp.Rational(1, 3)
    main_jets.append(
        sp.factor(
            integral_jets[4] + gamma_one_linear * preceding_rank_ratio
        )
    )
    main_second_difference = [
        second_shift_difference(value) for value in main_jets
    ]
    expected_main_difference = [
        0,
        0,
        24 * R / ((6 * R - 5) * (6 * R - 1)),
        24
        * R
        * (12 * R - 11)
        / ((6 * R - 7) * (6 * R - 5) * (6 * R - 1)),
        -216
        * R
        * (R - 1)
        * (R - 2)
        / (
            5
            * (6 * R - 7)
            * (6 * R - 5)
            * (6 * R - 1)
        ),
    ]
    if any(
        sp.cancel(actual - expected) != 0
        for actual, expected in zip(
            main_second_difference, expected_main_difference
        )
    ):
        raise AssertionError("main second-shift difference failed")

    # For exceptional rank r-1:
    # W^(3r-3) C*_(r-1) = K*_(r-1)(1+s1 W+s2 W^2+...).
    exceptional_configurations, exceptional_jets = (
        exceptional_integral_jets()
    )
    exceptional_first_ratio = 18 * (R - 1) / (6 * R - 7)
    exceptional_second_ratio = (
        -3
        * (R - 1)
        * (6 * R - 77)
        / (10 * (6 * R - 7))
    )
    expected_exceptional_jets = [
        1,
        exceptional_first_ratio,
        exceptional_second_ratio,
    ]
    if any(
        sp.cancel(actual - expected)
        for actual, expected in zip(
            exceptional_jets,
            expected_exceptional_jets,
        )
    ):
        raise AssertionError("exceptional Bell jets failed")

    four_kstar_over_kr = (
        -24 * R / ((6 * R - 5) * (6 * R - 1))
    )
    exceptional_difference = [
        0,
        0,
        four_kstar_over_kr,
        sp.factor(
            four_kstar_over_kr * (exceptional_first_ratio - 1)
        ),
        sp.factor(
            four_kstar_over_kr
            * (exceptional_second_ratio - exceptional_first_ratio)
        ),
    ]
    total_difference = [
        sp.factor(main + exceptional)
        for main, exceptional in zip(
            main_second_difference, exceptional_difference
        )
    ]
    leading_epsilon_over_kr = (
        -36
        * R
        * (R - 1)
        / ((6 * R - 7) * (6 * R - 5) * (6 * R - 1))
    )
    if total_difference[:4] != [0, 0, 0, 0]:
        raise AssertionError("MD2 top four Laurent jets do not cancel")
    if sp.cancel(total_difference[4] - leading_epsilon_over_kr):
        raise AssertionError("epsilon leading Laurent layer failed")

    # Since K_(r-1)c0_(r-1)/K_r is preceding_rank_ratio, the last
    # identity is exactly e_r=-6(r-1)c_(r-1).
    if sp.cancel(
        leading_epsilon_over_kr
        + 6 * (R - 1) * preceding_rank_ratio
    ):
        raise AssertionError("epsilon/c relation failed")

    return {
        "schema": "amra.opg1757.md2-laurent-identity.v2",
        "scope": (
            "Symbolic all-r Bell-jet identity. Configurations outside the "
            "listed finite set have pole defect at least five."
        ),
        "main_bell_configurations_amplitude_p2_p3_p4_p5_defect": (
            configurations
        ),
        "exceptional_bell_configurations_amplitude_p2_p3_defect": (
            exceptional_configurations
        ),
        "main_jets_after_common_Kr": [str(value) for value in main_jets],
        "main_second_shift_difference": [
            str(value) for value in main_second_difference
        ],
        "exceptional_contribution": [
            str(value) for value in exceptional_difference
        ],
        "total_top_five_laurent_jets": [
            str(value) for value in total_difference
        ],
        "epsilon_leading_identity": "e_r = -6*(r-1)*c_(r-1)",
        "conclusion": (
            "pole((F_2,r-2F_1,r+F_0,r)/sqrt(1-2x), x=1/2) "
            "= 3r-4 with e_r=-6(r-1)c_(r-1) for every r>=2"
        ),
        "status": "symbolic_all_rank_md2_identity_passed",
    }


def main() -> None:
    print(json.dumps(audit(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
