#!/usr/bin/env python3
"""Fixed-page formulas for the pooled alpha^2 layers B_2, B_3, B_4.

For a fixed number n of actual page vertices, process the contracted core
blocks instead of the pages.  The state is a partition of the n pages.  A
core block of weight w selecting k current page components has multiplicity
w**k beta**k and merges those components.  For weight-one blocks,

    U_1 = (1+n beta) I + N,   N**n = 0,

so an arbitrary symbolic number of singleton core blocks requires only n
nilpotent terms.  This gives exact formulas with s left symbolic.

The script derives the complete four-page determinant and checks the B_4
formula against the independent t-Newton certificate for s=5,...,12.
It does not claim a coefficientwise-positive all-s decomposition of B_4.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
from collections import defaultdict
from pathlib import Path

import sympy as sp

from complete_split_rayleigh import canonical_partition
from tp2_barrier_search import pooled_t_newton_rows


BETA, S = sp.symbols("beta s", integer=True, positive=True)
Partition = tuple[tuple[int, ...], ...]
Vector = dict[Partition, sp.Expr]


def merge_pages(
    partition: Partition, selected: frozenset[int]
) -> Partition | None:
    selected_blocks: list[int] = []
    for index, block in enumerate(partition):
        count = sum(vertex in selected for vertex in block)
        if count > 1:
            return None
        if count:
            selected_blocks.append(index)
    if len(selected_blocks) <= 1:
        return partition
    merged = tuple(
        vertex
        for index in selected_blocks
        for vertex in partition[index]
    )
    remaining = [
        block
        for index, block in enumerate(partition)
        if index not in selected_blocks
    ]
    return canonical_partition((*remaining, merged))


def core_block_transfer(
    vector: Vector,
    weight: int,
    page_count: int,
    only_merging: bool = False,
) -> Vector:
    """Add one contracted core block of multiplicity ``weight``."""

    result: defaultdict[Partition, sp.Expr] = defaultdict(lambda: sp.S.Zero)
    minimum = 2 if only_merging else 0
    for partition, coefficient in vector.items():
        for size in range(minimum, page_count + 1):
            for selected in itertools.combinations(range(page_count), size):
                destination = merge_pages(partition, frozenset(selected))
                if destination is not None:
                    result[destination] += (
                        coefficient * (weight * BETA) ** size
                    )
    return {
        partition: sp.expand(coefficient)
        for partition, coefficient in result.items()
        if coefficient
    }


def fixed_page_profile_polynomial(
    page_count: int, two_blocks: int
) -> sp.Expr:
    """Forest polynomial for k weight-two and s-2k weight-one blocks."""

    discrete = tuple((page,) for page in range(page_count))
    vector: Vector = {discrete: sp.S.One}
    for _ in range(two_blocks):
        vector = core_block_transfer(vector, 2, page_count)

    singleton_count = S - 2 * two_blocks
    diagonal = 1 + page_count * BETA
    result: defaultdict[Partition, sp.Expr] = defaultdict(lambda: sp.S.Zero)
    current = vector
    for order in range(page_count):
        multiplier = (
            sp.expand_func(sp.binomial(singleton_count, order))
            * diagonal ** (singleton_count - order)
        )
        for partition, coefficient in current.items():
            result[partition] += multiplier * coefficient
        current = core_block_transfer(
            current, 1, page_count, only_merging=True
        )
    if current:
        raise AssertionError("the page-partition nilpotent bound failed")
    return sp.factor(sum(result.values(), sp.S.Zero))


def k3_polynomial() -> sp.Expr:
    return (
        1
        + 12 * BETA
        + (6 * S + 30) * BETA**2
        + 28 * S * BETA**3
        + 6 * S**2 * BETA**4
    )


def k4_polynomial() -> sp.Expr:
    return (
        1
        + 28 * BETA
        + (14 * S + 288) * BETA**2
        + (292 * S + 1264) * BETA**3
        + (75 * S**2 + 1918 * S + 2008) * BETA**4
        + (968 * S**2 + 4064 * S) * BETA**5
        + (160 * S**3 + 3072 * S**2) * BETA**6
        + 1024 * S**3 * BETA**7
        + 128 * S**4 * BETA**8
    )


def derive_four_page_determinant() -> tuple[list[sp.Expr], sp.Expr]:
    profiles = [
        fixed_page_profile_polynomial(4, two_blocks)
        for two_blocks in range(3)
    ]
    determinant = sp.powsimp(
        profiles[1] ** 2 - profiles[0] * profiles[2], force=True
    )
    expected = (
        24
        * BETA**4
        * (1 + 4 * BETA) ** (2 * S - 10)
        * k4_polynomial()
    )
    ratio = sp.cancel(sp.powsimp(determinant / expected, force=True))
    if sp.factor(sp.expand_func(ratio)) != 1:
        raise AssertionError("the four-page determinant formula failed")
    return profiles, expected


def b4_expression_at_s(s: int) -> sp.Expr:
    if s < 4:
        raise ValueError("s must be at least 4")
    if s == 4:
        return sp.S.Zero
    if s == 5:
        return (
            288
            * BETA**8
            * (75 * BETA**2 + 40 * BETA + 7)
        )
    lam = 1 + s * BETA
    bracket = (
        (1 + 4 * BETA) ** (2 * s - 10)
        * k4_polynomial().subs(S, s)
        - 2
        * lam**2
        * (1 + 3 * BETA) ** (2 * s - 8)
        * k3_polynomial().subs(S, s)
        + lam**4 * (1 + 2 * BETA) ** (2 * s - 6)
    )
    return sp.expand(24 * BETA**4 * lam ** (2 * s - 12) * bracket)


def integer_convolution(left: list[int], right: list[int]) -> list[int]:
    result = [0] * (len(left) + len(right) - 1)
    for left_degree, left_value in enumerate(left):
        for right_degree, right_value in enumerate(right):
            result[left_degree + right_degree] += left_value * right_value
    return result


def linear_power(coefficient: int, exponent: int) -> list[int]:
    return [
        math.comb(exponent, degree) * coefficient**degree
        for degree in range(exponent + 1)
    ]


def b4_bracket_coefficients(s: int) -> list[int]:
    """Fast integer coefficients of the signed bracket in the B4 formula."""

    if s < 5:
        raise ValueError("the bracket parametrization starts at s=5")
    lam2 = linear_power(s, 2)
    lam4 = linear_power(s, 4)
    k3 = [1, 12, 6 * s + 30, 28 * s, 6 * s**2]
    k4 = [
        1,
        28,
        14 * s + 288,
        292 * s + 1264,
        75 * s**2 + 1918 * s + 2008,
        968 * s**2 + 4064 * s,
        160 * s**3 + 3072 * s**2,
        1024 * s**3,
        128 * s**4,
    ]
    positive_four = integer_convolution(
        linear_power(4, 2 * s - 10), k4
    )
    negative_three = integer_convolution(
        integer_convolution(lam2, linear_power(3, 2 * s - 8)),
        k3,
    )
    positive_two = integer_convolution(
        lam4, linear_power(2, 2 * s - 6)
    )
    maximum = max(
        len(positive_four), len(negative_three), len(positive_two)
    )
    return [
        int(
            (positive_four[degree] if degree < len(positive_four) else 0)
            - 2
            * (
                negative_three[degree]
                if degree < len(negative_three)
                else 0
            )
            + (positive_two[degree] if degree < len(positive_two) else 0)
        )
        for degree in range(maximum)
    ]


def build_certificate(
    minimum_s: int = 5,
    maximum_s: int = 12,
    maximum_counterexample_s: int = 500,
) -> dict[str, object]:
    profiles, determinant = derive_four_page_determinant()
    rows: list[list[object]] = []
    for s in range(minimum_s, maximum_s + 1):
        expected = sp.Poly(b4_expression_at_s(s), BETA)
        pooled = {
            degree: int(coefficient)
            for order, degree, coefficient in pooled_t_newton_rows(
                s, 4 * s - 8
            )
            if order == 4
        }
        formula = {
            degree: int(expected.coeff_monomial(BETA**degree))
            for degree in range(expected.degree() + 1)
            if expected.coeff_monomial(BETA**degree)
        }
        if pooled != formula:
            raise AssertionError(f"B4 mismatch at s={s}")
        rows.extend(
            [s, degree, str(coefficient)]
            for degree, coefficient in sorted(pooled.items())
        )

    payload = json.dumps(rows, separators=(",", ":")).encode("utf-8")
    summaries: list[list[object]] = []
    digest = hashlib.sha256()
    negative: list[list[object]] = []
    for s in range(5, maximum_counterexample_s + 1):
        coefficients = b4_bracket_coefficients(s)
        for degree, coefficient in enumerate(coefficients):
            digest.update(f"{s},{degree},{coefficient}\n".encode("ascii"))
            if coefficient < 0 and not negative:
                negative.append([s, degree, str(coefficient)])
        support = [
            (degree, coefficient)
            for degree, coefficient in enumerate(coefficients)
            if coefficient
        ]
        summaries.append(
            [
                s,
                support[0][0],
                support[-1][0],
                str(min(coefficient for _, coefficient in support)),
            ]
        )
    return {
        "schema": "amra.complete_split.fixed_page_union.v1",
        "component_tree_formula": (
            "For core-block subset I (a=|I|) and page subset J "
            "(b=|J|), a,b>=1, the connected bipartite tree weight is "
            "beta^(a+b-1)*b^(a-1)*(sum_{i in I}w_i)^(b-1)"
            "*product_{i in I}w_i."
        ),
        "profile_polynomials_four_pages": [str(value) for value in profiles],
        "four_page_determinant": str(determinant),
        "K4": str(k4_polynomial()),
        "B4": {
            "s4": "0",
            "s5": "288*beta^8*(75*beta^2+40*beta+7)",
            "s_ge_6": (
                "24*beta^4*lambda^(2s-12)*("
                "(1+4beta)^(2s-10)*K4"
                "-2lambda^2*(1+3beta)^(2s-8)*K3"
                "+lambda^4*(1+2beta)^(2s-6))"
            ),
            "full_small_s_rows_s_beta_coefficient": rows,
            "all_saved_coefficients_positive": all(
                int(row[2]) > 0 for row in rows
            ),
            "sha256_rows": hashlib.sha256(payload).hexdigest(),
            "proof_status": (
                "The formula is proved for all s. Coefficientwise positivity "
                "is proved here only for s=4,5 and exhaustively verified for "
                "the complete polynomials s=6,...,12; a uniform positive "
                "decomposition of the signed three-exponential bracket "
                "remains open."
            ),
        },
        "B4_bracket_counterexample_search": {
            "s_range": [5, maximum_counterexample_s],
            "complete_beta_polynomial_at_each_s": True,
            "first_negative": negative,
            "all_searched_coefficients_nonnegative": not negative,
            "summaries_s_first_degree_last_degree_minimum": summaries,
            "sha256_all_s_degree_coefficient_lines": digest.hexdigest(),
            "scope_warning": (
                "This is a targeted finite counterexample search for the "
                "exact all-s formula, not a proof for unbounded s."
            ),
        },
        "general_component_recurrence": (
            "Choose the least remaining page q. It is either isolated, or "
            "belongs to a component with nonempty core-block subset I and "
            "page subset J containing q; multiply the component_tree_formula "
            "by the recurrence on the complements. This is subtraction-free "
            "for each H(w), but taking H1^2-H0H2 introduces cross-component "
            "subtractions not controlled termwise."
        ),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--minimum-s", type=int, default=5)
    parser.add_argument("--maximum-s", type=int, default=12)
    parser.add_argument("--maximum-counterexample-s", type=int, default=500)
    parser.add_argument("--output", type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    certificate = build_certificate(
        args.minimum_s,
        args.maximum_s,
        args.maximum_counterexample_s,
    )
    rendered = json.dumps(certificate, indent=2, sort_keys=True)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + "\n", encoding="utf-8")
        print(f"wrote {args.output}")
    else:
        print(rendered)


if __name__ == "__main__":
    main()
