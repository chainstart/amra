#!/usr/bin/env python3
"""Independent finite checks for the projection-free moment no-go ledger."""

from fractions import Fraction
from itertools import combinations, product
from math import comb, log2
import json


def matrix_rank(matrix):
    work = [[Fraction(value) for value in row] for row in matrix]
    rows = len(work)
    columns = len(work[0]) if rows else 0
    pivot_row = 0
    for column in range(columns):
        pivot = next((r for r in range(pivot_row, rows) if work[r][column]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        scale = work[pivot_row][column]
        work[pivot_row] = [value / scale for value in work[pivot_row]]
        for row in range(rows):
            if row != pivot_row and work[row][column]:
                factor = work[row][column]
                work[row] = [
                    left - factor * right
                    for left, right in zip(work[row], work[pivot_row])
                ]
        pivot_row += 1
        if pivot_row == rows:
            break
    return pivot_row


def moment_matrix(atom_count, feature_count):
    atoms = tuple(range(1, atom_count + 1))
    weights = tuple((-1) ** atom * (atom + 1) for atom in atoms)
    evaluation = [[atom**degree for atom in atoms] for degree in range(feature_count)]
    return [
        [sum(weights[a] * evaluation[i][a] * evaluation[j][a] for a in range(atom_count))
         for j in range(feature_count)]
        for i in range(feature_count)
    ]


def explicit_union(d, k):
    result = set()
    for chosen in combinations(range(d), k):
        for y in (0, 1):
            for digits in product((0, 1, 2), repeat=k):
                point = [0] * d
                for index, digit in zip(chosen, digits):
                    point[index] = digit
                result.add((y, *point))
    return result


def main():
    rank_checks = []
    for atoms in range(1, 8):
        low_features = max(0, atoms - 1)
        low_rank = matrix_rank(moment_matrix(atoms, low_features))
        full_rank = matrix_rank(moment_matrix(atoms, atoms))
        assert low_rank <= low_features < atoms
        assert full_rank == atoms
        rank_checks.append({
            "atoms": atoms,
            "features_below_atoms": low_features,
            "rank_below": low_rank,
            "rank_at_atom_count": full_rank,
        })

    support_checks = []
    for d in range(2, 11):
        k = d // 2
        row_atoms = 2 * 3**k
        union_formula = 2 * sum(comb(d, s) * 2**s for s in range(k + 1))
        union_enumerated = len(explicit_union(d, k))
        assert union_enumerated == union_formula
        assert union_formula >= 2 ** ((3 * d + 1) / 2) / (d + 1)
        support_checks.append({
            "d": d,
            "K": comb(d, k),
            "row_atoms": row_atoms,
            "union_atoms": union_formula,
        })

    ledgers = []
    for d in (30, 60, 120, 240, 480):
        k = d // 2
        K = comb(d, k)
        row_atoms = 2 * 3**k
        union_atoms = 2 * sum(comb(d, s) * 2**s for s in range(k + 1))
        log_t = Fraction(9, 5) * log2(K)
        row_exponent = log2(row_atoms) / log_t
        union_exponent = log2(union_atoms) / log_t
        separate_exponent = log2(K * row_atoms) / log_t
        assert abs(separate_exponent - (Fraction(5, 9) + row_exponent)) < 1e-12
        ledgers.append({
            "d": d,
            "row_exponent": row_exponent,
            "union_exponent": union_exponent,
            "separate_row_sum_exponent": separate_exponent,
        })

    print(json.dumps({
        "schema": "amra.erdos1083.projection-free-moment-independent-check.v1",
        "rank_factorization_examples": rank_checks,
        "phi6_support_checks": support_checks,
        "exponent_ledgers": ledgers,
        "limits": {
            "row": 5 * log2(3) / 18,
            "union": 5 / 6,
            "separate_row_sum": 5 / 9 + 5 * log2(3) / 18,
        },
        "result": "pass",
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
