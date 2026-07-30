#!/usr/bin/env python3
"""Independent finite audit of the ordinary subleading symbol.

The source profiles are rebuilt from normalized finite Lagrange sums.
No existing OPG verifier or recorded profile polynomial is imported.
Finite checks cannot certify the manuscript's all-orders resummation;
the returned verdict distinguishes formula evidence from proof status.
"""

from __future__ import annotations

import argparse
import json
import math
from fractions import Fraction
from functools import lru_cache

import sympy as sp


K, J, X, T, Z = sp.symbols("k j x t z")


def truncated_convolution(
    left: tuple[int, ...],
    right: tuple[int, ...],
    maximum_loss: int,
) -> tuple[int, ...]:
    result = [0] * (maximum_loss + 1)
    for left_loss, left_value in enumerate(left):
        for right_loss, right_value in enumerate(right):
            if left_loss + right_loss <= maximum_loss:
                result[left_loss + right_loss] += (
                    left_value * right_value
                )
    return tuple(result)


@lru_cache(maxsize=None)
def normalized_falling(
    shift: int,
    length: int,
    maximum_loss: int,
) -> tuple[int, ...]:
    result = [1] + [0] * maximum_loss
    for offset in range(length):
        root = shift + offset
        for loss in range(maximum_loss, 0, -1):
            result[loss] -= root * result[loss - 1]
    return tuple(result)


@lru_cache(maxsize=None)
def normalized_lagrange_e(
    beta: int,
    edge_count: int,
    maximum_loss: int,
) -> tuple[int, ...]:
    if edge_count < 0:
        return tuple([0] * (maximum_loss + 1))
    result = [0] * (maximum_loss + 1)
    for index in range(edge_count + 1):
        product = normalized_falling(
            beta + edge_count,
            index,
            maximum_loss,
        )
        weight = (
            math.comb(edge_count, index)
            * 2 ** (edge_count - index)
            * (-1) ** index
        )
        for loss in range(maximum_loss + 1):
            result[loss] += weight * product[loss]
    return tuple(result)


@lru_cache(maxsize=None)
def normalized_profile(
    profile_index: int,
    edge_count: int,
    maximum_loss: int,
) -> tuple[int, ...]:
    shift = (0, 2, 4)[profile_index]
    current = normalized_lagrange_e(
        shift,
        edge_count,
        maximum_loss,
    )
    previous = normalized_lagrange_e(
        shift + 1,
        edge_count - 1,
        maximum_loss,
    )
    consecutive = tuple(
        current[loss]
        - (
            2 * edge_count * previous[loss - 1]
            if loss >= 1
            else 0
        )
        for loss in range(maximum_loss + 1)
    )
    result = list(
        truncated_convolution(
            normalized_falling(
                shift,
                edge_count,
                maximum_loss,
            ),
            consecutive,
            maximum_loss,
        )
    )
    if profile_index == 2 and edge_count >= 1:
        exceptional = truncated_convolution(
            normalized_falling(
                4,
                edge_count - 1,
                maximum_loss,
            ),
            normalized_lagrange_e(
                4,
                edge_count - 1,
                maximum_loss,
            ),
            maximum_loss,
        )
        for loss in range(2, maximum_loss + 1):
            result[loss] += (
                8 * edge_count * exceptional[loss - 2]
            )
    return tuple(result)


def profile_polynomial(
    profile_index: int,
    loss: int,
    maximum_loss: int,
) -> sp.Poly:
    values = [
        (
            edge_count,
            normalized_profile(
                profile_index,
                edge_count,
                maximum_loss,
            )[loss],
        )
        for edge_count in range(loss + 2)
    ]
    polynomial = sp.Poly(
        sp.interpolate(values[: loss + 1], J),
        J,
    )
    assert polynomial.degree() <= loss
    assert polynomial.eval(loss + 1) == values[-1][1]
    return polynomial


def source_rank_sequences(maximum_loss: int):
    sequences = {
        profile_index: {rank: [] for rank in range(4)}
        for profile_index in range(3)
    }
    for profile_index in range(3):
        for loss in range(maximum_loss + 1):
            polynomial = profile_polynomial(
                profile_index,
                loss,
                maximum_loss,
            )
            for rank in range(4):
                sequences[profile_index][rank].append(
                    (
                        polynomial.coeff_monomial(
                            J ** (loss - rank)
                        )
                        if loss >= rank
                        else sp.S.Zero
                    )
                )
    return sequences


def claimed_functions():
    w = 1 - 2 * Z
    a = sp.sqrt(w)
    p = [
        -Z * (4 * Z**2 - 3) / (6 * w ** sp.Rational(5, 2)),
        -Z
        * (52 * Z**2 - 48 * Z + 9)
        / (6 * w ** sp.Rational(5, 2)),
        -Z
        * (100 * Z**2 - 96 * Z + 21)
        / (6 * w ** sp.Rational(5, 2)),
    ]
    q = [
        Z
        * (16 * Z**5 - 24 * Z**3 + 153 * Z - 144)
        / (72 * w ** sp.Rational(11, 2)),
        Z**2
        * (
            5008 * Z**4
            - 11904 * Z**3
            + 10152 * Z**2
            - 3168 * Z
            + 81
        )
        / (72 * w ** sp.Rational(11, 2)),
        Z
        * (
            5392 * Z**5
            - 14592 * Z**4
            + 13416 * Z**3
            - 4032 * Z**2
            - 279 * Z
            + 144
        )
        / (72 * w ** sp.Rational(11, 2)),
    ]
    s = [
        Z
        * (
            8896 * Z**8
            - 41472 * Z**7
            + 83664 * Z**6
            - 79488 * Z**5
            + 11556 * Z**4
            + 116640 * Z**3
            - 183465 * Z**2
            + 3240 * Z
            + 80460
        )
        / (6480 * w ** sp.Rational(17, 2)),
        -Z
        * (
            3596864 * Z**8
            - 13932288 * Z**7
            + 22711536 * Z**6
            - 19498752 * Z**5
            + 8751564 * Z**4
            - 2032560 * Z**3
            + 884925 * Z**2
            - 502200 * Z
            + 36180
        )
        / (6480 * w ** sp.Rational(17, 2)),
        Z
        * (
            32886976 * Z**8
            - 111992832 * Z**7
            + 157083984 * Z**6
            - 116581248 * Z**5
            + 49790916 * Z**4
            - 12121920 * Z**3
            + 474255 * Z**2
            + 793800 * Z
            - 126900
        )
        / (6480 * w ** sp.Rational(17, 2)),
    ]
    return a, p, q, s


def central_moment_audit(maximum_k: int = 64) -> int:
    checks = 0
    for page_count in range(1, maximum_k + 1):
        denominator = 2**page_count
        moments = []
        for order in range(2, 5):
            value = sum(
                Fraction(
                    math.comb(page_count, successes)
                    * (2 * successes - page_count) ** order,
                    denominator * (2 * page_count) ** order,
                )
                for successes in range(page_count + 1)
            )
            moments.append(value)
        assert moments[0] == Fraction(1, 4 * page_count)
        assert moments[1] == 0
        assert moments[2] == (
            Fraction(3, 16 * page_count**2)
            - Fraction(1, 8 * page_count**3)
        )
        checks += 3
    return checks


def ordinary_coefficient(
    page_count: int,
    depth: int,
    maximum_loss: int,
) -> Fraction:
    total_loss = depth + 4
    numerator = 0
    for left in range(page_count + 1):
        right = page_count - left
        kernel = 0
        for loss in range(total_loss + 1):
            other = total_loss - loss
            kernel += (
                normalized_profile(1, left, maximum_loss)[loss]
                * normalized_profile(1, right, maximum_loss)[other]
                - normalized_profile(0, left, maximum_loss)[loss]
                * normalized_profile(2, right, maximum_loss)[other]
            )
        numerator += math.comb(page_count, left) * kernel
    return Fraction(
        numerator,
        2**page_count * 2 * page_count * (page_count - 1),
    )


def audit(maximum_loss: int = 16, maximum_depth: int = 12):
    if maximum_loss < maximum_depth + 4:
        raise ValueError("maximum_loss must be at least maximum_depth+4")

    sequences = source_rank_sequences(maximum_loss)
    a, p, q, s = claimed_functions()
    functions = {0: [a, a, a], 1: p, 2: q, 3: s}
    profile_checks = 0
    for rank in range(4):
        for profile_index in range(3):
            series = sp.series(
                functions[rank][profile_index],
                Z,
                0,
                maximum_loss - rank + 1,
            ).removeO().expand()
            for loss in range(rank, maximum_loss + 1):
                actual = sequences[profile_index][rank][loss]
                expected = series.coeff(Z, loss - rank)
                assert actual == expected
                profile_checks += 1

    u = T * X
    v = T * (1 - X)
    substitute = lambda expression, value: expression.subs(Z, value)
    g1 = T * (
        (substitute(p[1], u) - substitute(p[0], u))
        * substitute(a, v)
        + substitute(a, u)
        * (substitute(p[1], v) - substitute(p[2], v))
    )
    assert sp.simplify(g1 + g1.subs(X, 1 - X)) == 0

    g2 = T**2 * (
        (substitute(q[1], u) - substitute(q[0], u))
        * substitute(a, v)
        + substitute(a, u)
        * (substitute(q[1], v) - substitute(q[2], v))
        + substitute(p[1], u) * substitute(p[1], v)
        - substitute(p[0], u) * substitute(p[2], v)
    )
    g3 = T**3 * (
        (substitute(s[1], u) - substitute(s[0], u))
        * substitute(a, v)
        + substitute(a, u)
        * (substitute(s[1], v) - substitute(s[2], v))
        + substitute(p[1], u) * substitute(q[1], v)
        + substitute(q[1], u) * substitute(p[1], v)
        - substitute(p[0], u) * substitute(q[2], v)
        - substitute(q[0], u) * substitute(p[2], v)
    )
    h2 = sp.factor(g2.subs(X, sp.Rational(1, 2)))
    h3 = sp.factor(
        g3.subs(X, sp.Rational(1, 2))
        + sp.diff(g2, X, 2).subs(
            X, sp.Rational(1, 2)
        )
        / 8
    )
    expected_h2 = 2 * T**4 / (1 - T)
    expected_h3 = (
        -T**4
        * (
            43 * T**4
            - 129 * T**3
            + 108 * T**2
            - 6 * T
            + 6
        )
        / (3 * (1 - T) ** 4)
    )
    assert sp.simplify(h2 - expected_h2) == 0
    assert sp.simplify(h3 - expected_h3) == 0

    h3_series = sp.series(
        h3,
        T,
        0,
        maximum_loss + 1,
    ).removeO().expand()
    h3_coefficient_checks = 0
    for total_loss in range(5, maximum_loss + 1):
        expected = -sp.Rational(
            22 * total_loss**3
            - 117 * total_loss**2
            + 41 * total_loss
            + 78,
            18,
        )
        assert h3_series.coeff(T, total_loss) == expected
        h3_coefficient_checks += 1

    subleading_checks = 0
    rows = []
    for depth in range(1, maximum_depth + 1):
        start = max(2, (depth + 5) // 2)
        points = []
        for page_count in range(start, start + depth + 3):
            value = ordinary_coefficient(
                page_count,
                depth,
                maximum_loss,
            )
            points.append(
                (
                    page_count,
                    sp.Rational(
                        value.numerator,
                        value.denominator,
                    ),
                )
            )
        polynomial = sp.Poly(
            sp.interpolate(points[: depth + 1], K),
            K,
        )
        for page_count, value in points[depth + 1 :]:
            assert polynomial.eval(page_count) == value
        actual = polynomial.coeff_monomial(K ** (depth - 1))
        expected = -sp.Rational(
            22 * depth**3
            + 147 * depth**2
            + 161 * depth
            - 258,
            36,
        )
        assert actual == expected
        subleading_checks += 1
        rows.append(
            {"depth": depth, "subleading": str(actual)}
        )

    subleading_generating = sp.factor(
        -sp.Rational(1, 36)
        * (
            22 * Z * (1 + 4 * Z + Z**2) / (1 - Z) ** 4
            + 147 * Z * (1 + Z) / (1 - Z) ** 3
            + 161 * Z / (1 - Z) ** 2
            - 258 * Z / (1 - Z)
        )
    )
    expected_generating = (
        -Z
        * (43 * Z**3 - 123 * Z**2 + 90 * Z + 12)
        / (6 * (1 - Z) ** 4)
    )
    assert sp.simplify(
        subleading_generating - expected_generating
    ) == 0

    moment_checks = central_moment_audit()
    return {
        "schema": "amra.opg1757.independent-ordinary-subleading.v1",
        "imports_existing_opg_verifier": False,
        "maximum_loss": maximum_loss,
        "profile_checks": profile_checks,
        "g1_exactly_antisymmetric": True,
        "central_moment_checks": moment_checks,
        "H2": str(h2),
        "H3": str(h3),
        "h3_coefficient_checks": h3_coefficient_checks,
        "maximum_depth": maximum_depth,
        "subleading_polynomial_checks": subleading_checks,
        "subleading_generating_function": str(
            subleading_generating
        ),
        "rows": rows,
        "formula_verdict": "PASS",
        "all_orders_proof_verdict": (
            "PASS_WITH_SYMBOLIC_SADDLE_CERTIFICATE"
        ),
        "reason": (
            "Finite source checks agree; the separate symbolic saddle "
            "certificate now proves P_h,Q_h,S_h at all losses."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--maximum-loss", type=int, default=16)
    parser.add_argument("--maximum-depth", type=int, default=12)
    args = parser.parse_args()
    print(
        json.dumps(
            audit(args.maximum_loss, args.maximum_depth),
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
