#!/usr/bin/env python3
"""Lightweight checks for the projection-free moment dimension ledger."""

from itertools import combinations, product
from math import comb, log2
import json


def explicit_union(d: int, k: int):
    union = set()
    for chosen in combinations(range(d), k):
        for y in (0, 1):
            for digits in product((0, 1, 2), repeat=k):
                point = [0] * d
                for index, digit in zip(chosen, digits):
                    point[index] = digit
                union.add((y, *point))
    return union


def row_support(d: int, chosen):
    result = set()
    for y in (0, 1):
        for digits in product((0, 1, 2), repeat=len(chosen)):
            point = [0] * d
            for index, digit in zip(chosen, digits):
                point[index] = digit
            result.add((y, *point))
    return result


def main() -> None:
    checks = []
    for d in range(2, 11):
        k = d // 2
        union = explicit_union(d, k)
        expected_union = 2 * sum(comb(d, s) * 2**s for s in range(k + 1))
        expected_row = 2 * 3**k
        assert len(union) == expected_union
        for chosen in combinations(range(d), k):
            assert len(row_support(d, chosen)) == expected_row
        assert expected_row >= 2 * 3 ** ((d - 1) / 2)
        assert expected_union >= 2 ** ((3 * d + 1) / 2) / (d + 1)
        checks.append({
            "d": d,
            "factor_count": d + 1,
            "rows": comb(d, k),
            "one_row_support": expected_row,
            "union_support": expected_union,
        })

    exponent_ledger = []
    for d in (30, 60, 120, 240):
        k = d // 2
        rows = comb(d, k)
        row_atoms = 2 * 3**k
        union_atoms = 2 * sum(comb(d, s) * 2**s for s in range(k + 1))
        # Normalize t by K=t^(5/9), so log_2 t=(9/5)log_2 K.
        log_t = (9 / 5) * log2(rows)
        exponent_ledger.append({
            "d": d,
            "log_t_row_matrix_dimension": log2(row_atoms) / log_t,
            "log_t_common_union_feature_dimension": log2(union_atoms) / log_t,
            "limits": {
                "row": 5 * log2(3) / 18,
                "union": 5 / 6,
            },
        })

    print(json.dumps({
        "schema": "amra.erdos1083.multivariate-moment-dimension-check.v1",
        "finite_exact_checks": checks,
        "closure_exponent_ledger": exponent_ledger,
        "result": "pass",
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
