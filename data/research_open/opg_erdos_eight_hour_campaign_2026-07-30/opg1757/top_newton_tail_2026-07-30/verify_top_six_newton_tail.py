#!/usr/bin/env python3
"""Exact symbolic audit for the top six base-four Newton layers."""

from __future__ import annotations

import argparse
import json

import sympy as sp


S, J, K, H = sp.symbols(
    "s j k h", integer=True, nonnegative=True
)


def falling(value: sp.Expr, degree: int) -> sp.Expr:
    if degree < 0:
        return sp.S.Zero
    return sp.prod(value - offset for offset in range(degree))


def lagrange_e(
    s: sp.Expr,
    component_parameter: sp.Expr,
    degree: int,
) -> sp.Expr:
    if degree < 0:
        return sp.S.Zero
    return sp.expand(
        sum(
            sp.Rational((-1) ** index, 2**index)
            * falling(component_parameter, index)
            * s ** (degree - index)
            / (
                sp.factorial(index)
                * sp.factorial(degree - index)
            )
            for index in range(degree + 1)
        )
    )


def lagrange_d(
    s: sp.Expr,
    component_parameter: sp.Expr,
    degree: int,
) -> sp.Expr:
    return sp.expand(
        lagrange_e(s, component_parameter, degree)
        - lagrange_e(s, component_parameter, degree - 1)
    )


def profile(profile_index: int, degree: int) -> sp.Expr:
    if profile_index == 0:
        return sp.expand(
            falling(S, degree)
            * lagrange_d(S, S - degree, degree)
        )
    if profile_index == 1:
        return sp.expand(
            falling(S - 2, degree)
            * lagrange_d(S, S - 2 - degree, degree)
        )
    if profile_index != 2:
        raise ValueError(profile_index)
    return sp.expand(
        falling(S - 4, degree)
        * lagrange_d(S, S - 4 - degree, degree)
        + 4
        * falling(S - 4, degree - 1)
        * lagrange_e(S, S - 3 - degree, degree - 1)
    )


def recorded_profile_symbols() -> dict[int, dict[int, sp.Expr]]:
    common = {
        0: sp.Integer(1),
        1: -J,
        2: -J * (4 * H + J - 1) / 2,
        3: -J * (J - 1) * (4 * H + J - 4) / 2,
        4: (
            -J
            * (J - 1)
            * (
                48 * H**2
                + 72 * H * J
                - 480 * H
                + 15 * J**2
                - 179 * J
                + 298
            )
            / 24
        ),
        5: (
            -J
            * (J - 1)
            * (J - 2)
            * (
                144 * H**2
                + 120 * H * J
                - 1896 * H
                + 21 * J**2
                - 487 * J
                + 1368
            )
            / 24
        ),
        6: (
            -J
            * (J - 1)
            * (J - 2)
            * (
                720 * H**2 * J
                - 7920 * H**2
                + 420 * H * J**2
                - 13900 * H * J
                + 49440 * H
                + 63 * J**3
                - 2716 * J**2
                + 18769 * J
                - 33564
            )
            / 48
        ),
    }
    special = {
        7: {
            0: (
                -J * (J - 1) * (J - 2) * (J - 3)
                * (
                    99 * J**3 - 6735 * J**2
                    + 68072 * J - 172304
                ) / 48
            ),
            1: (
                -J * (J - 1) * (J - 2) * (J - 3)
                * (
                    99 * J**3 - 5979 * J**2
                    + 28228 * J + 34304
                ) / 48
            ),
            2: (
                -J * (J - 1) * (J - 2) * (J - 3)
                * (
                    33 * J**3 - 1741 * J**2
                    - 2752 * J + 50544
                ) / 16
            ),
        },
        8: {
            0: (
                -J * (J - 1) * (J - 2) * (J - 3)
                * (J - 4)
                * (
                    19305 * J**3 - 1955250 * J**2
                    + 27822835 * J - 95970722
                ) / 5760
            ),
            1: (
                -J * (J - 1) * (J - 2) * (J - 3)
                * (
                    19305 * J**4 - 1866150 * J**3
                    + 21355435 * J**2 - 42726222 * J
                    - 65967352
                ) / 5760
            ),
            2: (
                -J * (J - 1) * (J - 2) * (J - 3)
                * (
                    19305 * J**4 - 1699830 * J**3
                    + 7974235 * J**2 + 73056018 * J
                    - 286934392
                ) / 5760
            ),
        },
        9: {
            0: (
                -J * (J - 1) * (J - 2) * (J - 3)
                * (J - 4)
                * (
                    32175 * J**4 - 4800510 * J**3
                    + 113664485 * J**2 - 869470078 * J
                    + 2087628000
                ) / 5760
            ),
            1: (
                -J * (J - 1) * (J - 2) * (J - 3)
                * (J - 4)
                * (
                    32175 * J**4 - 4491630 * J**3
                    + 74951525 * J**2 - 235796398 * J
                    - 315271680
                ) / 5760
            ),
            2: (
                -J * (J - 1) * (J - 2) * (J - 3)
                * (J - 4)
                * (
                    32175 * J**4 - 4182750 * J**3
                    + 38234405 * J**2 + 224723042 * J
                    - 1367491680
                ) / 5760
            ),
        },
    }
    result: dict[int, dict[int, sp.Expr]] = {}
    for degree, expression in common.items():
        result[degree] = {
            profile_index: sp.factor(
                expression.subs(H, profile_index)
            )
            for profile_index in range(3)
        }
    result.update(special)
    return result


def binomial_expectation(polynomial: sp.Expr) -> sp.Expr:
    result = sp.S.Zero
    for (power,), coefficient in sp.Poly(
        sp.expand(polynomial), J
    ).terms():
        for falling_degree in range(power + 1):
            result += (
                coefficient
                * sp.functions.combinatorial.numbers.stirling(
                    power, falling_degree, kind=2
                )
                * falling(K, falling_degree)
                / 2**falling_degree
            )
    return sp.factor(result)


def determinant_power_coefficients(
    symbols: dict[int, dict[int, sp.Expr]],
) -> list[sp.Expr]:
    result = []
    for drop in range(4, 10):
        kernel = sp.S.Zero
        for left_drop in range(drop + 1):
            right_drop = drop - left_drop
            for profile_pair, sign in (
                ((1, 1), 1),
                ((0, 2), -1),
            ):
                left = symbols[left_drop][profile_pair[0]]
                right = symbols[right_drop][
                    profile_pair[1]
                ].subs(J, K - J)
                kernel += sign * left * right
        result.append(
            sp.factor(
                binomial_expectation(kernel)
                / (2 * K * (K - 1))
            )
        )
    return result


def elementary_roots(maximum_degree: int = 5) -> dict[int, sp.Expr]:
    Q, INDEX = sp.symbols("q index", integer=True, nonnegative=True)
    powers = {
        power: sp.summation(
            INDEX**power, (INDEX, 4, Q + 3)
        )
        for power in range(1, maximum_degree + 1)
    }
    elementary = {0: sp.Integer(1)}
    for degree in range(1, maximum_degree + 1):
        elementary[degree] = sp.factor(
            sum(
                (-1) ** (power - 1)
                * elementary[degree - power]
                * powers[power]
                for power in range(1, degree + 1)
            )
            / degree
        )
    return {
        degree: expression.subs(Q, sp.symbols("q"))
        for degree, expression in elementary.items()
    }


def newton_tail(power_coefficients: list[sp.Expr]) -> list[sp.Expr]:
    Q = sp.symbols("q")
    elementary = elementary_roots(5)
    total_degree = 2 * K - 4
    result: list[sp.Expr] = []
    for depth, power_coefficient in enumerate(power_coefficients):
        value = power_coefficient
        for earlier_depth in range(depth):
            falling_degree = total_degree - earlier_depth
            coefficient_drop = depth - earlier_depth
            value -= (
                result[earlier_depth]
                * (-1) ** coefficient_drop
                * elementary[coefficient_drop].subs(
                    Q, falling_degree
                )
            )
        result.append(sp.factor(value))
    return result


def direct_newton_row(page_count: int) -> list[int]:
    degree = 2 * page_count - 4
    values = []
    for offset in range(degree + 1):
        vertex_count = 4 + offset
        rows = [
            [
                int(profile(profile_index, edge_count).subs(
                    S, vertex_count
                ))
                for edge_count in range(page_count + 1)
            ]
            for profile_index in range(3)
        ]
        determinant = sum(
            rows[1][left] * rows[1][page_count - left]
            - rows[0][left] * rows[2][page_count - left]
            for left in range(page_count + 1)
        )
        values.append(
            (
                sp.factorial(page_count)
                * determinant
                // (2 * page_count * (page_count - 1))
            )
        )
    row = []
    current = values
    while current:
        row.append(int(current[0]))
        current = [
            current[index + 1] - current[index]
            for index in range(len(current) - 1)
        ]
    return row


def audit(maximum_regression_k: int = 12) -> dict[str, object]:
    symbols = recorded_profile_symbols()

    profile_checks = 0
    for drop in range(10):
        for profile_index in range(3):
            for edge_count in range(0, 2 * drop + 3):
                polynomial = sp.Poly(
                    profile(profile_index, edge_count), S
                )
                power = 2 * edge_count - drop
                actual = (
                    sp.S.Zero
                    if power < 0
                    else polynomial.coeff_monomial(S**power)
                )
                leading = sp.Rational(
                    1,
                    2**edge_count * sp.factorial(edge_count),
                )
                expected = (
                    leading
                    * symbols[drop][profile_index].subs(
                        J, edge_count
                    )
                )
                assert sp.simplify(actual - expected) == 0
                profile_checks += 1

    power_coefficients = determinant_power_coefficients(symbols)
    expected_power = [
        sp.Integer(1),
        K - 2,
        (K - 2) * (K - 21),
        (K - 3) * (K - 2) * (2 * K - 109) / 2,
        (
            (K - 3)
            * (K - 2)
            * (6 * K**2 - 661 * K + 4240)
            / 6
        ),
        (
            (K - 4)
            * (K - 3)
            * (K - 2)
            * (3 * K**2 - 554 * K + 6961)
            / 3
        ),
    ]
    assert all(
        sp.simplify(actual - expected) == 0
        for actual, expected in zip(
            power_coefficients, expected_power
        )
    )

    tail = newton_tail(power_coefficients)
    expected_tail = [
        sp.Integer(1),
        2 * (K - 2) * (K + 2),
        (
            (K - 2)
            * (12 * K**3 + 8 * K**2 - 71 * K - 171)
            / 6
        ),
        (
            (K - 3)
            * (K - 2)
            * (
                4 * K**4 + 4 * K**3 - 25 * K**2
                - 135 * K - 214
            )
            / 3
        ),
        (
            (K - 4)
            * (K - 3)
            * (K - 2)
            * (
                240 * K**5 + 240 * K**4 - 1240 * K**3
                - 12384 * K**2 - 40481 * K - 55515
            )
            / 360
        ),
        (
            (K - 4)
            * (K - 3)
            * (K - 2)
            * (
                48 * K**7 - 208 * K**6 - 280 * K**5
                - 2424 * K**4 - 333 * K**3
                + 33943 * K**2 + 163804 * K + 273030
            )
            / 180
        ),
    ]
    assert all(
        sp.simplify(actual - expected) == 0
        for actual, expected in zip(tail, expected_tail)
    )

    regression_rows = []
    for page_count in range(2, maximum_regression_k + 1):
        row = direct_newton_row(page_count)
        for depth in range(min(6, len(row))):
            index = len(row) - 1 - depth
            expected = (
                expected_tail[depth].subs(K, page_count)
                * sp.factorial(index)
            )
            assert row[index] == expected
        regression_rows.append(
            {
                "k": page_count,
                "tail": row[max(0, len(row) - 6):],
            }
        )

    return {
        "schema": "amra.opg1757.top-six-newton-tail.v1",
        "scope": (
            "Exact Lagrange/profile coefficient identities plus "
            "degree-bounded finite-defect extraction; not a claim "
            "about the middle Newton coefficients."
        ),
        "profile_identity_checks": profile_checks,
        "power_coefficients": [
            str(sp.factor(value)) for value in power_coefficients
        ],
        "normalized_newton_tail": [
            str(sp.factor(value)) for value in tail
        ],
        "regression_rows": regression_rows,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--maximum-regression-k", type=int, default=12
    )
    args = parser.parse_args()
    print(
        json.dumps(
            audit(args.maximum_regression_k),
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
