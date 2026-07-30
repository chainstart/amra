#!/usr/bin/env python3
"""Exact certificates for affine-unit minors and norm-torus axis collapse."""

from __future__ import annotations

import hashlib
import json
from math import factorial, prod

import sympy as sp


def coefficient_vector(poly: sp.Poly, degree: int) -> tuple[int, ...]:
    return tuple(int(poly.nth(index)) for index in range(degree))


def affine_inverse_rows(
    nodes: tuple[int, ...], multiplier: int, offset: int = 3
) -> tuple[tuple[int, ...], ...]:
    """Return interlaced U_i,C_i coefficient rows.

    P(x)=prod_i(x+a_i), q_i=P/(x+a_i), and

      U_i=x+a_i-M*q_i+offset,  C_i=x+a_i+M*q_i.
    """

    degree = len(nodes)
    if degree < 4 or len(set(nodes)) != degree:
        raise ValueError("need at least four distinct nodes")
    x = sp.symbols("x")
    product_poly = sp.Poly(
        sp.prod(x + node for node in nodes), x
    )
    rows = []
    for node in nodes:
        quotient, remainder = sp.div(
            product_poly, sp.Poly(x + node, x)
        )
        assert remainder.is_zero
        affine = sp.Poly(x + node, x)
        upper = affine - multiplier * quotient + sp.Poly(offset, x)
        centre = affine + multiplier * quotient
        rows.extend((
            coefficient_vector(upper, degree),
            coefficient_vector(centre, degree),
        ))
    return tuple(rows)


def selected_row_indices(degree: int) -> tuple[int, ...]:
    return (0, 1, 2, 3) + tuple(
        2 * (index - 1) for index in range(3, degree - 1)
    )


def affine_minor(
    nodes: tuple[int, ...], multiplier: int, offset: int = 3
) -> int:
    rows = affine_inverse_rows(nodes, multiplier, offset)
    selected = [rows[index] for index in selected_row_indices(len(nodes))]
    return int(sp.Matrix(selected).det())


def vandermonde(values: tuple[int, ...]) -> int:
    return prod(
        values[right] - values[left]
        for left in range(len(values))
        for right in range(left + 1, len(values))
    )


def affine_minor_absolute_formula(
    nodes: tuple[int, ...], multiplier: int
) -> int:
    degree = len(nodes)
    return (
        4
        * abs(multiplier) ** (degree - 2)
        * abs(nodes[1] - nodes[0])
        * abs(vandermonde(nodes[: degree - 2]))
    )


def superfactorial_lower_bound(degree: int, multiplier: int) -> int:
    return (
        4
        * abs(multiplier) ** (degree - 2)
        * prod(factorial(index) for index in range(1, degree - 2))
    )


def pell_power(
    base_a: int, base_b: int, squarefree: int, exponent: int
) -> tuple[int, int]:
    """Return A,B with (base_a+base_b sqrt(D))^exponent=A+B sqrt(D)."""

    result_a, result_b = 1, 0
    for _ in range(exponent):
        result_a, result_b = (
            result_a * base_a + result_b * base_b * squarefree,
            result_a * base_b + result_b * base_a,
        )
    return result_a, result_b


def torus_axis_matrix(
    pell_units: tuple[tuple[int, int, int], ...],
    max_power: int,
    multiplier: int,
) -> sp.Matrix:
    """Rows t+M/t and t-M/t in basis 1,sqrt(D_1),...,sqrt(D_r)."""

    rank = len(pell_units)
    rows: list[list[int]] = []
    for axis, (squarefree, base_a, base_b) in enumerate(pell_units):
        assert base_a * base_a - squarefree * base_b * base_b == 1
        for exponent in range(1, max_power + 1):
            value_a, value_b = pell_power(
                base_a, base_b, squarefree, exponent
            )
            plus = [0] * (rank + 1)
            minus = [0] * (rank + 1)
            plus[0] = (1 + multiplier) * value_a
            plus[axis + 1] = (1 - multiplier) * value_b
            minus[0] = (1 - multiplier) * value_a
            minus[axis + 1] = (1 + multiplier) * value_b
            rows.extend((plus, minus))
    return sp.Matrix(rows)


def boolean_word_matrix(
    pell_units: tuple[tuple[int, int, int], ...],
    multiplier: int,
) -> sp.Matrix:
    """Rows t_S+M/t_S in the squarefree-radical basis.

    Columns are indexed by radical subsets in binary order.  The local
    coefficient matrix for the choice exponent 0 or 1 is

        [[1, 0], [A_i, B_i]].

    Inversion multiplies the column indexed by T by (-1)^|T|.
    """

    matrix = sp.Matrix([[1]])
    for squarefree, base_a, base_b in pell_units:
        assert base_a * base_a - squarefree * base_b * base_b == 1
        matrix = sp.kronecker_product(
            matrix, sp.Matrix([[1, 0], [base_a, base_b]])
        )
    column_scales = tuple(
        1 + multiplier * (-1) ** index.bit_count()
        for index in range(2 ** len(pell_units))
    )
    return matrix * sp.diag(*column_scales)


def boolean_word_determinant_formula(
    pell_units: tuple[tuple[int, int, int], ...],
    multiplier: int,
) -> int:
    rank = len(pell_units)
    exponent = 2 ** (rank - 1)
    return abs(
        (1 - multiplier * multiplier) ** exponent
        * prod(base_b ** exponent for _, _, base_b in pell_units)
    )


def boolean_family_minor(
    pell_units: tuple[tuple[int, int, int], ...],
    family: tuple[int, ...],
    multiplier: int,
) -> int:
    """The row/column minor indexed by the same Boolean family."""

    rank = len(pell_units)
    if len(set(family)) != len(family):
        raise ValueError("family masks must be distinct")
    if any(mask < 0 or mask >= 2**rank for mask in family):
        raise ValueError("family mask outside Boolean cube")
    ordered = tuple(sorted(family, key=lambda mask: (mask.bit_count(), mask)))
    rows = []
    for row_mask in ordered:
        row = []
        for column_mask in ordered:
            if column_mask & ~row_mask:
                row.append(0)
                continue
            coefficient = 1
            for index, (_, base_a, base_b) in enumerate(pell_units):
                bit = 1 << index
                if column_mask & bit:
                    coefficient *= base_b
                elif row_mask & bit:
                    coefficient *= base_a
            coefficient *= (
                1 + multiplier * (-1) ** column_mask.bit_count()
            )
            row.append(coefficient)
        rows.append(row)
    return int(sp.Matrix(rows).det())


def boolean_family_minor_formula(
    pell_units: tuple[tuple[int, int, int], ...],
    family: tuple[int, ...],
    multiplier: int,
) -> int:
    determinant = 1
    for mask in family:
        determinant *= 1 + multiplier * (-1) ** mask.bit_count()
        for index, (_, _, base_b) in enumerate(pell_units):
            if mask & (1 << index):
                determinant *= base_b
    return determinant


def support_diverse_word_minor(
    pell_units: tuple[tuple[int, int, int], ...],
    exponent_vectors: tuple[tuple[int, ...], ...],
    multiplier: int,
) -> tuple[int, int]:
    """Return exact minor and formula for words with distinct supports."""

    rank = len(pell_units)
    if any(len(vector) != rank for vector in exponent_vectors):
        raise ValueError("wrong exponent-vector length")
    if any(exponent < 0 for vector in exponent_vectors for exponent in vector):
        raise ValueError("exponents must be nonnegative")
    records = []
    for vector in exponent_vectors:
        support = sum(
            1 << index
            for index, exponent in enumerate(vector)
            if exponent
        )
        local_powers = tuple(
            pell_power(base_a, base_b, squarefree, exponent)
            for (squarefree, base_a, base_b), exponent
            in zip(pell_units, vector)
        )
        records.append((support, vector, local_powers))
    if len({support for support, _, _ in records}) != len(records):
        raise ValueError("word supports must be distinct")
    records.sort(key=lambda record: (record[0].bit_count(), record[0]))

    rows = []
    formula = 1
    for row_support, _, local_powers in records:
        row = []
        for column_support, _, _ in records:
            if column_support & ~row_support:
                row.append(0)
                continue
            coefficient = 1
            for index, (value_a, value_b) in enumerate(local_powers):
                bit = 1 << index
                if column_support & bit:
                    coefficient *= value_b
                elif row_support & bit:
                    coefficient *= value_a
            coefficient *= (
                1
                + multiplier
                * (-1) ** column_support.bit_count()
            )
            row.append(coefficient)
        rows.append(row)
        formula *= 1 + multiplier * (-1) ** row_support.bit_count()
        for index, (_, value_b) in enumerate(local_powers):
            if row_support & (1 << index):
                formula *= value_b
    return int(sp.Matrix(rows).det()), formula


def certificate() -> dict:
    multiplier = 3069
    node_sets = (
        (1, 2, 3, 4),
        (-4, -1, 2, 9, 13),
        (0, 3, 4, 10, 11, 20),
        (-9, -2, 1, 5, 12, 21, 25),
        (2, 5, 9, 14, 20, 27, 35, 44),
    )
    minor_records = []
    for nodes in node_sets:
        determinants = tuple(
            abs(affine_minor(nodes, multiplier, offset))
            for offset in (-17, 0, 3, 29)
        )
        formula = affine_minor_absolute_formula(nodes, multiplier)
        assert determinants == (formula,) * 4
        minor_records.append({
            "nodes": nodes,
            "degree": len(nodes),
            "absolute_minor": formula,
            "offset_independent": True,
        })

    consecutive_records = []
    for degree in range(4, 11):
        nodes = tuple(range(1, degree + 1))
        determinant = abs(affine_minor(nodes, multiplier))
        formula = superfactorial_lower_bound(degree, multiplier)
        assert determinant == formula
        consecutive_records.append((degree, determinant))

    pell_units = (
        (2, 3, 2),
        (3, 2, 1),
        (5, 9, 4),
        (7, 8, 3),
    )
    max_power = 6
    axis_matrix = torus_axis_matrix(
        pell_units, max_power, multiplier
    )
    axis_rank = axis_matrix.rank()
    assert axis_matrix.rows == 2 * len(pell_units) * max_power
    assert axis_rank == len(pell_units) + 1
    assert len(pell_units) + 2 > axis_rank

    boolean_matrix = boolean_word_matrix(pell_units, multiplier)
    boolean_determinant = abs(int(boolean_matrix.det()))
    boolean_formula = boolean_word_determinant_formula(
        pell_units, multiplier
    )
    assert boolean_matrix.rows == 2 ** len(pell_units)
    assert boolean_matrix.rank() == boolean_matrix.rows
    assert boolean_determinant == boolean_formula

    boolean_families = (
        (0, 1, 2, 4),
        (3, 5, 6, 9, 10, 12),
        (0, 15, 7, 2, 8, 5, 10, 1),
    )
    boolean_family_records = []
    for family in boolean_families:
        determinant = boolean_family_minor(
            pell_units, family, multiplier
        )
        formula = boolean_family_minor_formula(
            pell_units, family, multiplier
        )
        assert determinant == formula
        assert determinant != 0
        boolean_family_records.append({
            "family": family,
            "absolute_minor": abs(determinant),
        })

    support_diverse_vectors = (
        (0, 0, 0, 0),
        (3, 0, 0, 0),
        (0, 2, 0, 0),
        (1, 4, 0, 0),
        (0, 0, 5, 0),
        (2, 0, 3, 0),
        (0, 1, 2, 6),
    )
    support_minor, support_formula = support_diverse_word_minor(
        pell_units, support_diverse_vectors, multiplier
    )
    assert support_minor == support_formula
    assert support_minor != 0

    payload = {
        "multiplier": multiplier,
        "minor_records": minor_records,
        "consecutive_records": consecutive_records,
        "pell_units": pell_units,
        "axis_max_power": max_power,
        "axis_parameter_count": len(pell_units) * max_power,
        "axis_row_count": axis_matrix.rows,
        "axis_rank": axis_rank,
        "first_forced_zero_minor_size": axis_rank + 1,
        "boolean_word_count": boolean_matrix.rows,
        "boolean_word_rank": boolean_matrix.rank(),
        "boolean_word_absolute_determinant": boolean_determinant,
        "boolean_word_determinant_formula": (
            "|1-M^2|^(2^(r-1))*prod_i|B_i|^(2^(r-1))"
        ),
        "boolean_family_records": boolean_family_records,
        "boolean_family_minor_formula": (
            "prod_(S in W)(1+M*(-1)^|S|)"
            "*prod_(i in S)B_i"
        ),
        "support_diverse_vectors": support_diverse_vectors,
        "support_diverse_absolute_minor": abs(support_minor),
        "support_diverse_status": (
            "arbitrary powers with pairwise distinct supports have full rank"
        ),
        "positive_scope": (
            "arbitrary distinct integral affine shifts satisfying "
            "prod(theta+a_i)=1"
        ),
        "negative_scope": (
            "rank-only extensions to unions of independent norm-torus axes"
        ),
    }
    canonical = json.dumps(
        payload, sort_keys=True, separators=(",", ":"), default=list
    )
    payload["sha256"] = hashlib.sha256(
        canonical.encode("utf-8")
    ).hexdigest()
    return payload


def main() -> int:
    result = certificate()
    print(
        "AFFINE_UNIT_MINOR"
        f"|node_tests={len(result['minor_records'])}"
        "|offsets_per_test=4"
        f"|consecutive_degrees={len(result['consecutive_records'])}"
        "|formula=4*abs(M)^(d-2)*abs(a2-a1)*abs(Vandermonde(a1..a_(d-2)))"
        "|integral_superfactorial_lower_bound=true"
    )
    print(
        "NORM_TORUS_AXIS_COLLAPSE"
        f"|independent_axes={len(result['pell_units'])}"
        f"|powers_per_axis={result['axis_max_power']}"
        f"|parameters={result['axis_parameter_count']}"
        f"|symmetrized_rows={result['axis_row_count']}"
        f"|additive_rank={result['axis_rank']}"
        f"|first_forced_zero_minor_size={result['first_forced_zero_minor_size']}"
        "|status=counterexample_to_rank_only_generalization"
    )
    print(
        "BOOLEAN_UNIT_WORD_MINOR"
        f"|independent_axes={len(result['pell_units'])}"
        f"|words={result['boolean_word_count']}"
        f"|additive_rank={result['boolean_word_rank']}"
        "|formula="
        f"{result['boolean_word_determinant_formula']}"
        "|status=exact_full_rank_obstruction"
    )
    print(
        "BOOLEAN_FAMILY_MINOR"
        f"|families={len(result['boolean_family_records'])}"
        "|max_words="
        f"{max(len(record['family']) for record in result['boolean_family_records'])}"
        f"|formula={result['boolean_family_minor_formula']}"
        "|all_nonzero=true"
    )
    print(
        "SUPPORT_DIVERSE_UNIT_WORD_MINOR"
        f"|words={len(result['support_diverse_vectors'])}"
        "|arbitrary_nonnegative_powers=true"
        "|pairwise_distinct_supports=true"
        "|full_row_rank=true"
    )
    print(f"CERTIFICATE|sha256={result['sha256']}")
    print("DONE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
