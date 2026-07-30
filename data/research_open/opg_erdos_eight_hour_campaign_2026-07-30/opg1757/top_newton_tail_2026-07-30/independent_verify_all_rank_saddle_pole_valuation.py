#!/usr/bin/env python3
"""Independent red-team certificate for all-rank saddle pole valuation."""

from __future__ import annotations

import argparse
import json

import sympy as sp


W, a, r, y, t, x = sp.symbols("W a r y t x")
X = (1 - W) / 2


def phase_derivative(order: int):
    return sp.factorial(order - 1) / 2**order * (
        -(1 - X) ** (1 - order)
        + (-1) ** order * X ** (1 - order)
    )


sigma = sp.factor(-1 / phase_derivative(2))
phase_atoms = {
    p: sp.factor(phase_derivative(p + 2) / sp.factorial(p + 2))
    for p in (1, 2, 3)
}


def defect(amplitude_order: int, counts: dict[int, int]) -> int:
    phase_defect = sum(
        ((p - 1) + (1 if p % 2 == 0 else 0)) * multiplicity
        for p, multiplicity in counts.items()
        if p >= 2
    )
    amplitude_defect = (
        0 if amplitude_order == 0 else amplitude_order - 1
    )
    return phase_defect + amplitude_defect


def enumerate_defect_configurations(maximum_defect: int = 3):
    """Enumerate independently, including p>=4 to prove their exclusion."""
    configurations = []
    for amplitude_order in range(0, maximum_defect + 2):
        for n2 in range(0, maximum_defect + 1):
            for n3 in range(0, maximum_defect + 1):
                for n4 in range(0, maximum_defect + 1):
                    counts = {2: n2, 3: n3, 4: n4}
                    value = defect(amplitude_order, counts)
                    if value <= maximum_defect:
                        configurations.append(
                            (amplitude_order, n2, n3, n4, value)
                        )
    expected = [
        (0, 0, 0, 0, 0),
        (1, 0, 0, 0, 0),
        (2, 0, 0, 0, 1),
        (0, 1, 0, 0, 2),
        (0, 0, 1, 0, 2),
        (1, 1, 0, 0, 2),
        (1, 0, 1, 0, 2),
        (3, 0, 0, 0, 2),
        (2, 1, 0, 0, 3),
        (2, 0, 1, 0, 3),
        (4, 0, 0, 0, 3),
    ]
    assert sorted(configurations) == sorted(expected)
    return expected


def falling_ratio(total, lower):
    """Polynomial continuation of total!/lower! for fixed difference."""
    length = int(sp.expand(total - lower))
    return sp.prod(total - offset for offset in range(length))


def gaussian_ratio(half_degree):
    difference = int(sp.expand(half_degree - 3 * r))
    if difference < 0:
        return 1 / sp.prod(
            6 * r - (2 * offset + 1)
            for offset in range(-difference)
        )
    return sp.prod(
        6 * r + (2 * offset + 1)
        for offset in range(difference)
    )


def independent_main_integral_jets():
    """Direct exponential-partition ratios, not the author's recurrence."""
    amplitude = (1 - y) / y * (1 - y / 2) ** (-a)
    derivatives = [
        sp.factor(
            sp.diff(amplitude, y, order).subs(y, 2 * X)
            / sp.factorial(order)
        )
        for order in range(5)
    ]
    baseline = derivatives[0]
    total = 0
    records = []
    for amplitude_order, n2, n3, _, value in (
        enumerate_defect_configurations()
    ):
        n1 = 2 * r - amplitude_order - 2 * n2 - 3 * n3
        parts = n1 + n2 + n3
        half_degree = r + parts
        contribution = (
            derivatives[amplitude_order]
            / baseline
            * phase_atoms[1] ** (n1 - 2 * r)
            * phase_atoms[2] ** n2
            * phase_atoms[3] ** n3
            * falling_ratio(2 * r, n1)
            * gaussian_ratio(half_degree)
            * sigma ** (half_degree - 3 * r)
        )
        total += contribution
        records.append(
            {
                "amplitude_order": amplitude_order,
                "n2": n2,
                "n3": n3,
                "defect": value,
                "n1": str(n1),
                "specialization_r2_zero_if_infeasible": bool(
                    n1.subs(r, 2) < 0
                    and sp.cancel(contribution.subs(r, 2)) == 0
                ),
            }
        )
    ratio_series = sp.series(total, W, 0, 4).removeO().expand()
    # Exact normalized baseline factor:
    # W^(3r) baseline/K_r = ((1+W^2)^2/(1-W^2))^r.
    baseline_series = 1 + 3 * r * W**2 + sp.O(W**4)
    jets = []
    for degree in range(4):
        value = ratio_series.coeff(W, degree)
        if degree >= 2:
            value += 3 * r * ratio_series.coeff(W, degree - 2)
        jets.append(sp.factor(sp.cancel(value)))
    return records, jets


def gamma_one_critical_value():
    """Derive Gamma_1 from the Bernoulli B_2 list at x=1/2."""
    B2 = lambda value: value**2 - value + sp.Rational(1, 6)
    raw = (
        B2(1) / sp.Rational(1, 2)
        + B2(1 - a)
        - B2(1 - a) / sp.Rational(1, 2)
    )
    result = sp.factor(raw / 2)
    expected = sp.Rational(1, 12) + a / 2 - a**2 / 2
    assert sp.cancel(result - expected) == 0
    return result


def main_and_exceptional_cancellation():
    _, integral = independent_main_integral_jets()
    gamma1 = gamma_one_critical_value()
    preceding_rank_ratio = (
        6 * r / ((6 * r - 1) * (6 * r - 5) * (6 * r - 7))
    )
    main = list(integral)
    main[3] = sp.factor(main[3] + gamma1 * preceding_rank_ratio)
    expected = [
        -1 / (6 * r - 1),
        0,
        3
        * r
        * (10 * a**2 - 10 * a + 6 * r - 1)
        / (10 * (6 * r - 5) * (6 * r - 1)),
        r
        * (
            24 * a**3 * r
            - 24 * a**3
            - 72 * a**2 * r
            + 78 * a**2
            + 48 * a * r
            - 54 * a
            + 1
        )
        / (2 * (6 * r - 7) * (6 * r - 5) * (6 * r - 1)),
    ]
    assert all(
        sp.cancel(actual - target) == 0
        for actual, target in zip(main, expected)
    )
    second = [
        sp.factor(value.subs(a, 4) - 2 * value.subs(a, 2) + value.subs(a, 0))
        for value in main
    ]
    exceptional_leading = -24 * r / ((6 * r - 5) * (6 * r - 1))
    exceptional_slope = 18 * (r - 1) / (6 * r - 7)
    exceptional = [
        0,
        0,
        exceptional_leading,
        sp.factor(exceptional_leading * (exceptional_slope - 1)),
    ]
    total = [
        sp.factor(left + right)
        for left, right in zip(second, exceptional)
    ]
    assert total == [0, 0, 0, 0]
    # Independently rederive the K* / K ratio before cancellation.
    raw_ratio = sp.factor(
        -36
        * (2 * r)
        * (2 * r - 1)
        / ((6 * r - 1) * (6 * r - 3) * (6 * r - 5))
    )
    assert sp.cancel(raw_ratio - exceptional_leading) == 0
    return main, second, exceptional, total


def low_rank_second_differences():
    """Use the exact printed first profile rows, not a finite pole script."""
    z = sp.symbols("z")
    common = 6 * (1 - 2 * z) ** sp.Rational(5, 2)
    P0 = -z * (4 * z**2 - 3) / common
    P1 = -z * (52 * z**2 - 48 * z + 9) / common
    P2 = -z * (100 * z**2 - 96 * z + 21) / common
    epsilon0 = sp.Integer(1) - 2 * sp.Integer(1) + sp.Integer(1)
    epsilon1 = sp.factor(P2 - 2 * P1 + P0)
    assert epsilon0 == 0 and epsilon1 == 0
    return epsilon0, epsilon1


def antisymmetric_convolution_audit(maximum_rank: int = 5):
    """Check that antisymmetry needs the complete a+b=n convolution."""
    delta = [x**index + 2 * x + index for index in range(maximum_rank + 1)]
    base = [3 * x**index - x + 2 * index for index in range(maximum_rank + 1)]
    records = []
    for rank in range(maximum_rank + 1):
        expression = sum(
            delta[left].subs(x, t * x)
            * base[rank - left].subs(x, t * (1 - x))
            - base[left].subs(x, t * x)
            * delta[rank - left].subs(x, t * (1 - x))
            for left in range(rank + 1)
        )
        assert sp.expand(expression.subs(x, 1 - x) + expression) == 0
        for derivative in range(0, 8, 2):
            assert sp.simplify(
                sp.diff(expression, x, derivative).subs(
                    x, sp.Rational(1, 2)
                )
            ) == 0
        records.append(rank)
    return records


def derivative_pole_propagation_audit():
    """Finite exact regression for the general +m derivative rule."""
    records = []
    for left_pole in range(0, 5):
        for right_pole in range(0, 5):
            expression = (
                (1 - 2 * t * x) ** (-left_pole)
                * (1 - 2 * t * (1 - x)) ** (-right_pole)
            )
            for order in range(0, 7):
                value = sp.cancel(
                    sp.diff(expression, x, order).subs(
                        x, sp.Rational(1, 2)
                    )
                    * (1 - t) ** (left_pole + right_pole + order)
                )
                assert sp.denom(value).subs(t, 1) != 0
            records.append((left_pole, right_pole))
    return records


def coefficient_extraction_audit(maximum_rank: int = 5):
    """Audit the j>d zero convention in the final polynomial formula."""
    records = []
    for rank in range(maximum_rank + 1):
        pole_power = 3 * rank + 1
        coefficients = [
            sp.Integer(0) if index < rank else sp.Integer(index + 2)
            for index in range(4 * rank + 1)
        ]
        numerator = sum(
            coefficient * t**index
            for index, coefficient in enumerate(coefficients)
        )
        generating = numerator / (1 - t) ** pole_power
        depth_symbol = sp.symbols(f"d_{rank}", integer=True)
        polynomial = sum(
            coefficient
            * sp.binomial(
                depth_symbol - index + pole_power - 1,
                pole_power - 1,
            )
            for index, coefficient in enumerate(coefficients)
        )
        for depth in range(rank, rank + 12):
            direct = sp.series(
                generating, t, 0, depth + 1
            ).removeO().coeff(t, depth)
            assert sp.simplify(polynomial.subs(depth_symbol, depth) - direct) == 0
        records.append(rank)
    return records


def audit():
    configurations, _ = independent_main_integral_jets()
    main, second, exceptional, total = main_and_exceptional_cancellation()
    epsilon0, epsilon1 = low_rank_second_differences()
    return {
        "schema": "amra.opg1757.all-rank-saddle-pole-independent.v1",
        "verdict": "PASS_WITH_LOCALIZATION_PROOF_OBLIGATION",
        "bell_configurations": configurations,
        "gamma_one_critical_value": str(gamma_one_critical_value()),
        "main_jets": [str(value) for value in main],
        "main_second_difference": [str(value) for value in second],
        "exceptional_layers": [str(value) for value in exceptional],
        "total_top_layers": [str(value) for value in total],
        "low_rank_second_differences": [str(epsilon0), str(epsilon1)],
        "antisymmetric_convolution_ranks": antisymmetric_convolution_audit(),
        "derivative_pole_pairs_checked": len(
            derivative_pole_propagation_audit()
        ),
        "coefficient_extraction_ranks": coefficient_extraction_audit(),
        "author_verifier_imported": False,
        "open_proof_obligation": (
            "Expand the all-r endpoint-localization assertion by deriving "
            "the principal parts of every saddle/Gamma term explicitly as "
            "finite combinations of the Lagrange identity."
        ),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    print(json.dumps(audit(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
