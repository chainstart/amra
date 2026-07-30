#!/usr/bin/env python3
"""Independent component-partition audit of the general-k extremal lemmas."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from fractions import Fraction
from pathlib import Path
from typing import Iterator

from five_page_union_formula import (
    k3_coefficients,
    k4_coefficients,
    k5_coefficients,
)
from seven_page_union_formula import k7_coefficients
from six_page_union_formula import k6_coefficients


def weak_compositions(total: int, length: int) -> Iterator[tuple[int, ...]]:
    if length == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for tail in weak_compositions(total - first, length - 1):
            yield (first, *tail)


def multinomial(parts: tuple[int, ...]) -> int:
    result = math.factorial(sum(parts))
    for part in parts:
        result //= math.factorial(part)
    return result


def component_tree_weight(twos: int, ones: int, pages: int) -> int:
    """Tree sum for one component, with singleton components included."""

    core_blocks = twos + ones
    if core_blocks == 1 and pages == 0:
        return 1
    if core_blocks == 0 and pages == 1:
        return 1
    if core_blocks == 0 or pages == 0:
        return 0
    return (
        pages ** (core_blocks - 1)
        * (2 * twos + ones) ** (pages - 1)
        * 2**twos
    )


def forest_weight_by_component_count(
    s: int, page_count: int, two_blocks: int, component_count: int
) -> int:
    """Sum weights of spanning forests having exactly ``component_count``."""

    ones = s - 2 * two_blocks
    total = 0
    for two_distribution in weak_compositions(two_blocks, component_count):
        two_multiplicity = multinomial(two_distribution)
        for one_distribution in weak_compositions(ones, component_count):
            one_multiplicity = multinomial(one_distribution)
            for page_distribution in weak_compositions(
                page_count, component_count
            ):
                product = 1
                for twos, singles, pages in zip(
                    two_distribution,
                    one_distribution,
                    page_distribution,
                ):
                    product *= component_tree_weight(twos, singles, pages)
                if product:
                    total += (
                        two_multiplicity
                        * one_multiplicity
                        * multinomial(page_distribution)
                        * product
                    )
    if total % math.factorial(component_count):
        raise AssertionError("labelled-component quotient is not integral")
    return total // math.factorial(component_count)


def normalized_top_ratios(
    s: int, page_count: int, two_blocks: int
) -> tuple[Fraction, Fraction, Fraction]:
    """Return leading coefficient and its next two normalized ratios."""

    exponent = s - 2 * two_blocks - page_count + 1
    if exponent < 0:
        raise ValueError("the polynomial normalization needs the stable range")
    tree, two_forest, three_forest = (
        forest_weight_by_component_count(
            s, page_count, two_blocks, component_count
        )
        for component_count in range(1, 4)
    )
    leading = Fraction(tree, page_count**exponent)
    following = (
        Fraction(two_forest, page_count**exponent)
        - Fraction(exponent, page_count) * leading
    )
    third = (
        Fraction(three_forest, page_count**exponent)
        - Fraction(exponent, page_count) * following
        - Fraction(exponent * (exponent - 1), 2 * page_count**2) * leading
    )
    return leading, following / leading, third / leading


def kernel_top_coefficient(page_count: int, s: int) -> int:
    coefficients = {
        2: [1],
        3: k3_coefficients(s),
        4: k4_coefficients(s),
        5: k5_coefficients(s),
        6: k6_coefficients(s),
        7: k7_coefficients(s),
    }[page_count]
    return int(coefficients[-1])


def build_audit() -> dict[str, object]:
    rows: list[list[object]] = []
    for page_count in range(2, 8):
        for s in (page_count + 3, page_count + 4):
            triples = [
                normalized_top_ratios(s, page_count, two_blocks)
                for two_blocks in range(3)
            ]
            leading = [triple[0] for triple in triples]
            r = [triple[1] for triple in triples]
            q = [triple[2] for triple in triples]
            expected_leading = [
                Fraction(
                    2**h
                    * page_count ** (h + page_count - 2)
                    * s ** (page_count - 1)
                )
                for h in range(3)
            ]
            if leading != expected_leading:
                raise AssertionError("leading tree coefficient failed")

            base_two_forest_ratio = Fraction(
                s**2
                - (page_count - 1) * s
                + (page_count - 1) * (page_count + 2),
                s * page_count,
            )
            expected_r = [
                base_two_forest_ratio
                - Fraction(
                    h * (3 * s - 2 * page_count + 2),
                    2 * s * page_count,
                )
                - Fraction(s - 2 * h - page_count + 1, page_count)
                for h in range(3)
            ]
            if r != expected_r:
                raise AssertionError("two-component affine ratio failed")

            q_second_difference = 2 * q[1] - q[0] - q[2]
            expected_q_second_difference = Fraction(
                4 * (page_count - 1) - (s + 2 * page_count - 2) ** 2,
                4 * page_count**2 * s**2,
            )
            if q_second_difference != expected_q_second_difference:
                raise AssertionError("three-component second difference failed")

            determinant_top = leading[1] ** 2 * (
                2 * q[1]
                + r[1] ** 2
                - q[0]
                - q[2]
                - r[0] * r[2]
            )
            expected_determinant_top = (
                4
                * page_count ** (2 * page_count - 4)
                * (page_count - 1)
                * s ** (2 * page_count - 4)
            )
            if determinant_top != expected_determinant_top:
                raise AssertionError("determinant upper endpoint failed")

            expected_kernel_top = (
                2
                * page_count ** (2 * page_count - 5)
                * s ** (2 * page_count - 4)
            )
            if kernel_top_coefficient(page_count, s) != expected_kernel_top:
                raise AssertionError("saved K_k upper endpoint failed")

            rows.append(
                [
                    page_count,
                    s,
                    str(leading[0]),
                    str(r[0]),
                    str(r[1]),
                    str(r[2]),
                    str(q_second_difference),
                    str(determinant_top),
                ]
            )

    cycle_rows: list[list[int]] = []
    for page_count in range(2, 20):
        cycle_sums = []
        for h in range(3):
            sum_squares = 0
            weights = [2] * h + [1] * (20 - 2 * h)
            for left in range(len(weights)):
                for right in range(left + 1, len(weights)):
                    sum_squares += weights[left] ** 2 * weights[right] ** 2
            cycle_sums.append(math.comb(page_count, 2) * sum_squares)
        second_difference = cycle_sums[0] + cycle_sums[2] - 2 * cycle_sums[1]
        if second_difference != 2 * page_count * (page_count - 1):
            raise AssertionError("four-cycle defect count failed")
        cycle_rows.append([page_count, second_difference])

    payload = json.dumps([rows, cycle_rows], separators=(",", ":")).encode(
        "utf-8"
    )
    return {
        "schema": "amra.complete_split.general_k_extremal.v1",
        "scope": (
            "Independent finite regression of the object-level formulas. "
            "The general proof is the component-partition calculation in "
            "GENERAL_K_POSITIVITY_ATTACK.md."
        ),
        "component_partition_rows": rows,
        "cycle_second_difference_rows": cycle_rows,
        "general_lower_endpoint": "2*k*(k-1)*beta^4",
        "general_upper_endpoint": (
            "4*k^(2k-4)*(k-1)*s^(2k-4)*beta^(4k-4)"
        ),
        "general_kernel_degree": "deg_beta K_k=4*(k-2)",
        "sha256_payload": hashlib.sha256(payload).hexdigest(),
        "status": "proved",
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    audit = build_audit()
    rendered = json.dumps(audit, indent=2, sort_keys=True)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + "\n", encoding="utf-8")
        print(f"wrote {args.output}")
    else:
        print(rendered)


if __name__ == "__main__":
    main()
