#!/usr/bin/env python3
"""Independent checks for the OPG-1757 all-depth top-face theorem.

The theorem is algebraic.  This verifier checks its two inputs by different
routes:

1. it directly evaluates the positive component-set-partition formula for
   forests with one, two, and three components;
2. it compares the resulting Stirling formula with the inherited primitive
   nilpotent-page transfer, without using fixed-page kernel interpolation.

Finite checks are audits of the displayed identities, not substitutes for
their all-parameter proofs.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from fractions import Fraction
from itertools import combinations
from pathlib import Path
from typing import Iterator


def weak_compositions(total: int, parts: int) -> Iterator[tuple[int, ...]]:
    """Yield weak compositions of ``total`` into ``parts`` slots."""

    if parts == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for tail in weak_compositions(total - first, parts - 1):
            yield (first, *tail)


def multinomial(total: int, cells: tuple[int, ...]) -> int:
    """Return the exact multinomial coefficient."""

    result = math.factorial(total)
    for cell in cells:
        result //= math.factorial(cell)
    return result


def component_tree_weight(a: int, b: int, pages: int) -> int:
    """Weight of one component in the component-set-partition formula."""

    core_blocks = a + b
    if core_blocks == 1 and pages == 0:
        return 1
    if core_blocks == 0 and pages == 1:
        return 1
    if core_blocks >= 1 and pages >= 1:
        return (
            pages ** (core_blocks - 1)
            * (2 * a + b) ** (pages - 1)
            * 2**a
        )
    return 0


def component_weight(s: int, h: int, pages: int, components: int) -> int:
    """Evaluate W_{h,c} from the exact positive component formula."""

    total = 0
    for doubled in weak_compositions(h, components):
        doubled_choices = multinomial(h, doubled)
        for singletons in weak_compositions(s - 2 * h, components):
            singleton_choices = multinomial(s - 2 * h, singletons)
            for page_cells in weak_compositions(pages, components):
                page_choices = multinomial(pages, page_cells)
                product = 1
                for a, b, j in zip(doubled, singletons, page_cells):
                    product *= component_tree_weight(a, b, j)
                total += (
                    doubled_choices
                    * singleton_choices
                    * page_choices
                    * product
                )
    divisor = math.factorial(components)
    if total % divisor:
        raise AssertionError("temporary component labels did not divide out")
    return total // divisor


def complete_component_tree_weight(a: int, b: int) -> int:
    """Weighted tree sum on one complete-graph component."""

    block_count = a + b
    if block_count == 1:
        return 1
    if block_count >= 2:
        return 2**a * (2 * a + b) ** (block_count - 2)
    return 0


def complete_component_weight(s: int, h: int, components: int) -> int:
    """Weight of profile-h complete-graph forests with c components."""

    total = 0
    for doubled in weak_compositions(h, components):
        doubled_choices = multinomial(h, doubled)
        for singletons in weak_compositions(s - 2 * h, components):
            singleton_choices = multinomial(s - 2 * h, singletons)
            product = 1
            for a, b in zip(doubled, singletons):
                product *= complete_component_tree_weight(a, b)
            total += doubled_choices * singleton_choices * product
    divisor = math.factorial(components)
    if total % divisor:
        raise AssertionError("complete-graph component labels did not divide")
    return total // divisor


def generic_complete_tree_weight(weights: tuple[int, ...]) -> int:
    """Weighted Cayley tree sum for edge weights w_i*w_j."""

    if len(weights) <= 1:
        return 1
    return sum(weights) ** (len(weights) - 2) * math.prod(weights)


def generic_two_component_weight(weights: tuple[int, ...]) -> int:
    """Two-component complete-graph forest sum, counted without labels."""

    if len(weights) < 2:
        return 0
    total = 0
    # Put vertex zero in the first component to choose one orientation of
    # every unordered bipartition.
    for mask in range(1 << (len(weights) - 1)):
        first = [weights[0]]
        second: list[int] = []
        for index, weight in enumerate(weights[1:]):
            (first if mask & (1 << index) else second).append(weight)
        if not second:
            continue
        total += generic_complete_tree_weight(
            tuple(first)
        ) * generic_complete_tree_weight(tuple(second))
    return total


def ternary_hyperforest_endpoint(
    s: int, h: int, components: int
) -> int:
    """Endpoint of forests with one ternary merge and ordinary binary merges."""

    weights = tuple([2] * h + [1] * (s - 2 * h))
    total = 0
    for triple in combinations(range(len(weights)), 3):
        selected = set(triple)
        hyperedge_weight = math.prod(weights[index] for index in triple)
        contracted = tuple(
            [
                weight
                for index, weight in enumerate(weights)
                if index not in selected
            ]
            + [sum(weights[index] for index in triple)]
        )
        forest_weight = (
            generic_complete_tree_weight(contracted)
            if components == 1
            else generic_two_component_weight(contracted)
        )
        total += hyperedge_weight * forest_weight
    return total


def integer_power(base: int, exponent: int) -> Fraction:
    """Exact integer power, allowing the two small negative exponents used here."""

    if exponent >= 0:
        return Fraction(base**exponent)
    return Fraction(1, base ** (-exponent))


def second_deepest_endpoint_data(s: int) -> tuple[int, int]:
    """Return the binary-forest determinant C and ternary correction Q."""

    phi = {
        h: [complete_component_weight(s, h, c) for c in (1, 2, 3)]
        for h in range(3)
    }
    psi = {
        h: [ternary_hyperforest_endpoint(s, h, c) for c in (1, 2)]
        for h in range(3)
    }

    tree = [phi[h][0] for h in range(3)]
    two = [phi[h][1] for h in range(3)]
    three = [phi[h][2] for h in range(3)]
    hyper_tree = [psi[h][0] for h in range(3)]
    hyper_two = [psi[h][1] for h in range(3)]

    binary_determinant = (
        two[1] ** 2
        + 2 * tree[1] * three[1]
        - tree[0] * three[2]
        - two[0] * two[2]
        - three[0] * tree[2]
    )
    ternary_correction = (
        2 * (tree[1] * hyper_two[1] + two[1] * hyper_tree[1])
        - (tree[0] * hyper_two[2] + two[0] * hyper_tree[2])
        - (hyper_tree[0] * two[2] + hyper_two[0] * tree[2])
    )
    return binary_determinant, ternary_correction


def predicted_second_deepest_endpoint_data(s: int) -> tuple[int, int]:
    """Closed forms for C_[2s-6] and its one-ternary correction."""

    binary = (
        4
        * (s * s + 4 * s - 24)
        * integer_power(s, 2 * s - 10)
    )
    ternary = -8 * (5 * s - 16) * integer_power(s, 2 * s - 9)
    if binary.denominator != 1 or ternary.denominator != 1:
        raise AssertionError("endpoint closed form is unexpectedly fractional")
    return binary.numerator, ternary.numerator


def predicted_second_deepest_component_table(
    s: int, h: int
) -> tuple[int, int, int, int, int]:
    """Five normalized component formulas displayed in the proof."""

    if h == 0:
        f2_factor = Fraction((s - 1) * (s + 6), 2)
        f3_factor = Fraction(
            (s - 2) * (s - 1) * (s * s + 13 * s + 60), 8
        )
        g1_factor = Fraction((s - 2) * (s - 1), 2)
        g2_factor = Fraction(
            (s - 3) * (s - 2) * (s - 1) * (3 * s + 20), 12
        )
    elif h == 1:
        f2_factor = Fraction((s - 2) * (s + 6), 2)
        f3_factor = Fraction(
            (s - 3) * (s - 2) * (s * s + 13 * s + 60), 8
        )
        g1_factor = Fraction((s - 3) * (s - 2), 2)
        g2_factor = Fraction(
            (s - 4) * (s - 3) * (s - 2) * (3 * s + 20), 12
        )
    elif h == 2:
        f2_factor = Fraction(s * s + 3 * s - 20, 2)
        f3_factor = Fraction(
            (s - 4) * (s**3 + 10 * s * s + 17 * s - 210), 8
        )
        g1_factor = Fraction((s - 4) * (s - 3), 2)
        g2_factor = Fraction(
            (s - 5) * (s - 4) * (3 * s * s + 11 * s - 66), 12
        )
    else:
        raise ValueError("h must be 0, 1, or 2")

    scale = 2**h
    values = (
        scale * integer_power(s, s - h - 2),
        scale * integer_power(s, s - h - 4) * f2_factor,
        scale * integer_power(s, s - h - 6) * f3_factor,
        scale * integer_power(s, s - h - 3) * g1_factor,
        scale * integer_power(s, s - h - 5) * g2_factor,
    )
    if any(value.denominator != 1 for value in values):
        raise AssertionError("component table entry is unexpectedly fractional")
    return tuple(value.numerator for value in values)


def second_deepest_coefficients(s: int) -> dict[int, int]:
    """Exact three coefficients of B_(2s-6)."""

    depth = 2 * s - 6
    common = 4 * math.factorial(depth) * integer_power(s, 2 * s - 10)
    rows = {
        4 * s - 12: common * (s * s + 4 * s - 24),
        4 * s - 11: common * 2 * s * (s * s - s - 8),
        4 * s - 10: common * s * s * (s - 2) * (2 * s - 7),
    }
    if any(value.denominator != 1 for value in rows.values()):
        raise AssertionError("second-deepest coefficient is fractional")
    return {degree: value.numerator for degree, value in rows.items()}


def predicted_component_ratios(
    s: int, pages: int
) -> tuple[list[int], list[Fraction], Fraction]:
    """Return predicted L_h, a_h, and 2b_1-b_0-b_2."""

    k = pages
    leading = [2**h * k ** (s - h - 1) * s ** (k - 1) for h in range(3)]
    ratios = [
        Fraction(
            2 * (s * s - (k - 1) * s + (k - 1) * (k + 2))
            - h * (3 * s - 2 * k + 2),
            2 * s * k,
        )
        for h in range(3)
    ]
    second_difference = -Fraction(
        4 * k * k
        - 12 * k * s
        - 12 * k
        + 9 * s * s
        + 12 * s
        + 8,
        4 * k * k * s * s,
    )
    return leading, ratios, second_difference


def direct_determinant_top(s: int, pages: int) -> int:
    """Compute the first surviving high coefficient of D_k from W_{h,c}."""

    weights = {
        h: [component_weight(s, h, pages, c) for c in (1, 2, 3)]
        for h in range(3)
    }
    leading = [weights[h][0] for h in range(3)]
    a = [Fraction(weights[h][1], leading[h]) for h in range(3)]
    b = [Fraction(weights[h][2], leading[h]) for h in range(3)]

    if leading[1] ** 2 != leading[0] * leading[2]:
        raise AssertionError("highest determinant coefficient did not cancel")
    if 2 * a[1] != a[0] + a[2]:
        raise AssertionError("second-highest determinant coefficient did not cancel")

    coefficient = leading[1] ** 2 * (
        a[1] ** 2 - a[0] * a[2] + 2 * b[1] - b[0] - b[2]
    )
    if coefficient.denominator != 1:
        raise AssertionError("determinant coefficient is unexpectedly fractional")
    return coefficient.numerator


def predicted_determinant_top(s: int, pages: int) -> int:
    """Closed form for [beta^(2s+2k-6)] D_k."""

    return (
        4
        * (pages - 1)
        * pages ** (2 * s - 6)
        * s ** (2 * pages - 4)
    )


def p_top_coefficient(s: int, pages: int) -> int:
    """Closed form for [beta^(4s-10)] P_s^(2)(beta,pages)."""

    if pages < 2:
        return 0
    return 4 * s ** (2 * s - 8) * (pages - 1) * pages ** (2 * s - 6)


def stirling2(m: int, n: int) -> int:
    """Stirling number of the second kind, with exact integer recurrence."""

    if m < 0 or n < 0:
        return 0
    row = [0] * (n + 1)
    row[0] = 1
    for _ in range(m):
        next_row = [0] * (n + 1)
        for block_count in range(1, n + 1):
            next_row[block_count] = (
                block_count * row[block_count] + row[block_count - 1]
            )
        row = next_row
    return row[n]


def top_face_coefficient(s: int, depth: int) -> int:
    """Closed form for [beta^(4s-10)] B_depth(s,beta)."""

    return (
        4
        * s ** (2 * s - 8)
        * math.factorial(depth)
        * (
            stirling2(2 * s - 5, depth)
            - stirling2(2 * s - 6, depth)
        )
    )


def finite_difference_top(s: int, depth: int) -> int:
    """Compute the same coefficient directly by Newton inversion."""

    return sum(
        (-1) ** (depth - pages)
        * math.comb(depth, pages)
        * p_top_coefficient(s, pages)
        for pages in range(depth + 1)
    )


def primitive_pooled_rows(s: int) -> dict[tuple[int, int], int]:
    """Run the inherited primitive page-transfer engine at full safe degree."""

    research_open = Path(__file__).resolve().parents[2]
    primitive_dir = (
        research_open / "q1_eight_hour_campaign_2026-07-29" / "opg1757"
    )
    sys.path.insert(0, str(primitive_dir))
    try:
        from tp2_barrier_search import pooled_t_newton_rows
    finally:
        sys.path.pop(0)
    return {
        (int(depth), int(degree)): int(coefficient)
        for depth, degree, coefficient in pooled_t_newton_rows(s, 4 * s - 8)
    }


def audit_component_endpoint(
    minimum_s: int, maximum_s: int, maximum_pages: int
) -> list[list[int]]:
    """Cross-check the one/two/three-component endpoint calculation."""

    checked: list[list[int]] = []
    for s in range(minimum_s, maximum_s + 1):
        for pages in range(2, maximum_pages + 1):
            direct = direct_determinant_top(s, pages)
            predicted = predicted_determinant_top(s, pages)
            if direct != predicted:
                raise AssertionError(
                    f"D-top mismatch at s={s}, pages={pages}: "
                    f"{direct} != {predicted}"
                )

            measured = {
                h: [
                    component_weight(s, h, pages, components)
                    for components in (1, 2, 3)
                ]
                for h in range(3)
            }
            leading, ratios, b_second = predicted_component_ratios(s, pages)
            if [measured[h][0] for h in range(3)] != leading:
                raise AssertionError("component leading formula mismatch")
            measured_a = [
                Fraction(measured[h][1], measured[h][0]) for h in range(3)
            ]
            measured_b = [
                Fraction(measured[h][2], measured[h][0]) for h in range(3)
            ]
            if measured_a != ratios:
                raise AssertionError("two-component ratio formula mismatch")
            if 2 * measured_b[1] - measured_b[0] - measured_b[2] != b_second:
                raise AssertionError("three-component second difference mismatch")
            checked.append([s, pages, direct])
    return checked


def audit_second_deepest_endpoint(
    minimum_s: int, maximum_s: int
) -> list[list[int]]:
    """Check the binary/ternary hyperforest formulas independently."""

    checked: list[list[int]] = []
    for s in range(minimum_s, maximum_s + 1):
        for h in range(3):
            measured_table = (
                complete_component_weight(s, h, 1),
                complete_component_weight(s, h, 2),
                complete_component_weight(s, h, 3),
                ternary_hyperforest_endpoint(s, h, 1),
                ternary_hyperforest_endpoint(s, h, 2),
            )
            predicted_table = predicted_second_deepest_component_table(s, h)
            if measured_table != predicted_table:
                raise AssertionError(
                    f"component table mismatch at s={s}, h={h}: "
                    f"{measured_table} != {predicted_table}"
                )
        measured = second_deepest_endpoint_data(s)
        predicted = predicted_second_deepest_endpoint_data(s)
        if measured != predicted:
            raise AssertionError(
                f"second-deepest endpoint mismatch at s={s}: "
                f"{measured} != {predicted}"
            )
        checked.append([s, measured[0], measured[1]])
    return checked


def audit_pooled_top_face(
    minimum_s: int, maximum_s: int
) -> tuple[list[list[int]], list[list[int]]]:
    """Compare the theorem with exact primitive pooled expansions."""

    theorem_rows: list[list[int]] = []
    finite_triangle_rows: list[list[int]] = []
    for s in range(minimum_s, maximum_s + 1):
        primitive = primitive_pooled_rows(s)
        expected_depths = set(range(2, 2 * s - 4))
        measured_depths = {depth for depth, _ in primitive}
        if measured_depths != expected_depths:
            raise AssertionError(
                f"finite depth support mismatch at s={s}: "
                f"{measured_depths} != {expected_depths}"
            )

        for depth in range(0, 2 * s - 2):
            formula = top_face_coefficient(s, depth)
            difference = finite_difference_top(s, depth)
            measured = primitive.get((depth, 4 * s - 10), 0)
            if formula != difference or formula != measured:
                raise AssertionError(
                    f"top-face mismatch at s={s}, n={depth}: "
                    f"formula={formula}, finite_difference={difference}, "
                    f"primitive={measured}"
                )
            theorem_rows.append([s, depth, formula])

        deepest = 2 * s - 5
        deepest_rows = {
            degree: coefficient
            for (depth, degree), coefficient in primitive.items()
            if depth == deepest
        }
        expected_deepest = {
            4 * s - 10: 4
            * s ** (2 * s - 8)
            * math.factorial(2 * s - 5)
        }
        if deepest_rows != expected_deepest:
            raise AssertionError(
                f"deepest-layer mismatch at s={s}: "
                f"{deepest_rows} != {expected_deepest}"
            )

        second_deepest = 2 * s - 6
        measured_second_deepest = {
            degree: coefficient
            for (depth, degree), coefficient in primitive.items()
            if depth == second_deepest
        }
        expected_second_deepest = second_deepest_coefficients(s)
        if measured_second_deepest != expected_second_deepest:
            raise AssertionError(
                f"second-deepest mismatch at s={s}: "
                f"{measured_second_deepest} != {expected_second_deepest}"
            )

        # This exact triangle is deliberately labelled finite-only.  The
        # theorem proves its boundary and vanishing region, not every
        # interior coefficient's sign.
        for (depth, degree), coefficient in sorted(primitive.items()):
            if not (2 <= depth <= 2 * s - 5):
                raise AssertionError("primitive row lies outside depth bounds")
            if not (2 * depth <= degree <= 4 * s - 10):
                raise AssertionError("primitive row lies outside degree bounds")
            if coefficient <= 0:
                raise AssertionError("finite primitive audit found a nonpositive row")
            finite_triangle_rows.append([s, depth, degree, coefficient])
    return theorem_rows, finite_triangle_rows


def build_certificate(
    minimum_s: int = 4,
    maximum_s: int = 12,
    maximum_pages: int = 9,
) -> dict[str, object]:
    """Build a deterministic audit certificate."""

    if minimum_s < 4 or maximum_s < minimum_s:
        raise ValueError("require 4 <= minimum_s <= maximum_s")
    if maximum_pages < 2:
        raise ValueError("maximum_pages must be at least 2")

    component_rows = audit_component_endpoint(
        minimum_s, maximum_s, maximum_pages
    )
    second_deepest_rows = audit_second_deepest_endpoint(
        minimum_s, maximum_s
    )
    theorem_rows, finite_rows = audit_pooled_top_face(minimum_s, maximum_s)
    digest_payload = json.dumps(
        [
            component_rows,
            second_deepest_rows,
            theorem_rows,
            finite_rows,
        ],
        separators=(",", ":"),
    ).encode("utf-8")
    return {
        "schema": "amra.opg1757.pooled_all_depth_top_face.v1",
        "status": "PASS",
        "proved_formula": (
            "[beta^(4s-10)]B_n="
            "4*s^(2s-8)*n!*(S2(2s-5,n)-S2(2s-6,n))"
        ),
        "proved_deepest_layer": (
            "B_(2s-5)=4*s^(2s-8)*(2s-5)!*beta^(4s-10)"
        ),
        "proved_second_deepest_layer": (
            "B_(2s-6)=4*(2s-6)!*s^(2s-10)*beta^(4s-12)*"
            "((s^2+4s-24)+2s(s^2-s-8)beta+"
            "s^2(s-2)(2s-7)beta^2)"
        ),
        "component_audit": {
            "s_range": [minimum_s, maximum_s],
            "page_range": [2, maximum_pages],
            "checked_pairs": len(component_rows),
        },
        "binary_ternary_hyperforest_audit": {
            "s_range": [minimum_s, maximum_s],
            "checked_sizes": len(second_deepest_rows),
        },
        "primitive_pooled_audit": {
            "s_range": [minimum_s, maximum_s],
            "theorem_rows": len(theorem_rows),
            "finite_only_interior_rows": len(finite_rows),
        },
        "scope_firewall": (
            "The finite interior positivity audit is not an all-s proof. "
            "Only the displayed top face, cutoff, and two deepest layers "
            "are claimed as all-parameter theorems."
        ),
        "sha256": hashlib.sha256(digest_payload).hexdigest(),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--minimum-s", type=int, default=4)
    parser.add_argument("--maximum-s", type=int, default=12)
    parser.add_argument("--maximum-pages", type=int, default=9)
    args = parser.parse_args()
    certificate = build_certificate(
        args.minimum_s, args.maximum_s, args.maximum_pages
    )
    print(json.dumps(certificate, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
