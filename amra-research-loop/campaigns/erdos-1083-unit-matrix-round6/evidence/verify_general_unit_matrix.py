#!/usr/bin/env python3
"""Exact finite guards for the symbolic all-m relative-unit matrix lemma."""

from __future__ import annotations

from fractions import Fraction
import json


def variables(m: int) -> tuple[str, ...]:
    return ("g", "f", "b") + tuple(f"r{i}" for i in range(1, m + 1)) + tuple(
        f"q{i}" for i in range(1, m + 1)
    )


def row(m: int, terms: dict[str, int]) -> list[int]:
    names = variables(m)
    return [terms.get(name, 0) for name in names]


def matrices(m: int) -> tuple[list[list[int]], list[list[int]], dict[str, list[int]]]:
    source = [row(m, {"g": 1, f"r{i}": 1}) for i in range(1, m + 1)]
    fixed_f = [row(m, {"f": 1})]
    complement = [row(m, {"f": 1, f"q{i}": 1}) for i in range(1, m + 1)]
    fixed_gb = [row(m, {"g": 1, "b": 1})]
    identities = [
        row(m, {"b": 1, f"r{i}": -1, f"q{i}": -1}) for i in range(1, m + 1)
    ]
    full = source + fixed_f + complement + fixed_gb + identities
    source_identity = source + fixed_f + identities
    return full, source_identity, {
        "source": list(range(0, m)),
        "fixed_f": [m],
        "complement": list(range(m + 1, 2 * m + 1)),
        "fixed_gb": [2 * m + 1],
        "identities": list(range(2 * m + 2, 3 * m + 2)),
    }


def rank(matrix: list[list[int]]) -> int:
    work = [[Fraction(value) for value in row_] for row_ in matrix]
    pivot = 0
    for column in range(len(work[0])):
        selected = next((r for r in range(pivot, len(work)) if work[r][column]), None)
        if selected is None:
            continue
        work[pivot], work[selected] = work[selected], work[pivot]
        scale = work[pivot][column]
        work[pivot] = [value / scale for value in work[pivot]]
        for r in range(len(work)):
            if r != pivot and work[r][column]:
                factor = work[r][column]
                work[r] = [x - factor * y for x, y in zip(work[r], work[pivot])]
        pivot += 1
        if pivot == len(work):
            break
    return pivot


def determinant(matrix: list[list[int]]) -> int:
    """Fraction-free Bareiss determinant."""
    work = [row_[:] for row_ in matrix]
    n = len(work)
    sign = 1
    previous = 1
    for k in range(n - 1):
        selected = next((r for r in range(k, n) if work[r][k]), None)
        if selected is None:
            return 0
        if selected != k:
            work[k], work[selected] = work[selected], work[k]
            sign *= -1
        pivot = work[k][k]
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                work[i][j] = (work[i][j] * pivot - work[i][k] * work[k][j]) // previous
        previous = pivot
        for i in range(k + 1, n):
            work[i][k] = 0
    return sign * work[-1][-1]


def apply(matrix: list[list[int]], vector: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(sum(a * b for a, b in zip(row_, vector)) for row_ in matrix)


def full_unit_minor(m: int, matrix: list[list[int]], groups: dict[str, list[int]]) -> int:
    selected_rows = groups["source"] + groups["fixed_f"] + groups["complement"] + groups["fixed_gb"]
    selected_columns = list(range(1, 2 * m + 3))  # delete g
    square = [[matrix[r][c] for c in selected_columns] for r in selected_rows]
    return determinant(square)


def source_unit_minor(m: int, matrix: list[list[int]]) -> int:
    # All source-identity rows; delete columns g and b.
    selected_columns = [1] + list(range(3, 2 * m + 3))
    square = [[row_[c] for c in selected_columns] for row_ in matrix]
    return determinant(square)


def main() -> None:
    rows = []
    for m in range(1, 33):
        full, source_only, groups = matrices(m)
        gauge = (1, 0, -1) + (-1,) * m + (0,) * m
        spectrum = (0, 0, 1) + (0,) * m + (1,) * m
        full_rank = rank(full)
        source_rank = rank(source_only)
        full_det = full_unit_minor(m, full, groups)
        source_det = source_unit_minor(m, source_only)
        assert full_rank == 2 * m + 2
        assert source_rank == 2 * m + 1
        assert abs(full_det) == abs(source_det) == 1
        assert apply(full, gauge) == (0,) * len(full)
        assert apply(source_only, gauge) == (0,) * len(source_only)
        assert apply(source_only, spectrum) == (0,) * len(source_only)
        assert apply(full, spectrum) != (0,) * len(full)

        # Check the affine formula at nonconsecutive symbolic labels s_i.
        a = 7
        scalar_labels = tuple(2 * i * i - 5 for i in range(1, m + 1))
        particular = (
            a,
            2 * a,
            -3 * a,
        ) + tuple((s - 1) * a for s in scalar_labels) + tuple(
            -(s + 2) * a for s in scalar_labels
        )
        expected = (
            tuple(s * a for s in scalar_labels)
            + (2 * a,)
            + tuple(-s * a for s in scalar_labels)
            + (-2 * a,)
            + (0,) * m
        )
        assert apply(full, particular) == expected
        rows.append({
            "m": m,
            "variables": 2 * m + 3,
            "full_rows": 3 * m + 2,
            "full_rank": full_rank,
            "full_unit_minor_determinant": full_det,
            "source_identity_rows": 2 * m + 1,
            "source_identity_rank": source_rank,
            "source_unit_minor_determinant": source_det,
        })

    print(json.dumps({
        "schema": "amra.erdos1083.unit-matrix-round6.general-m.v1",
        "checked_m": [1, 32],
        "formula": {
            "variables": "2m+3",
            "full_rank": "2m+2",
            "full_kernel": "Z*(1,0,-1,-1_i,0_i)",
            "source_identity_rank": "2m+1",
            "source_identity_kernel": "Z*gauge direct-sum Z*(0,0,1,0_i,1_i)",
            "smith_nonzero_invariants": "all 1, because each matrix has a maximal minor of determinant plus or minus 1",
        },
        "finite_guards": rows,
        "actual_block_realization_proved": False,
        "public_exponent_changed": False,
        "lean_used": False,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
