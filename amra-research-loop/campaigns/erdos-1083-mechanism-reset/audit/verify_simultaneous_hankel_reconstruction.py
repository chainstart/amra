#!/usr/bin/env python3
"""Independent finite guards for the simultaneous Hankel lemma.

Finite checks only; the universal result rests on the audit proof.
"""

from fractions import Fraction
from itertools import product
import json


def dot(x, y):
    return sum(a * b for a, b in zip(x, y))


def separating_vector(points):
    dimension = len(points[0]) if points else 0
    if dimension == 0:
        return ()
    for bound in range(1, 10):
        for vector in product(range(-bound, bound + 1), repeat=dimension):
            if vector == (0,) * dimension:
                continue
            values = [dot(vector, point) for point in points]
            if len(values) == len(set(values)):
                return vector
    raise AssertionError("guard search bound exhausted")


def determinant(matrix):
    a = [[Fraction(x) for x in row] for row in matrix]
    result = Fraction(1)
    for column in range(len(a)):
        pivot = next((row for row in range(column, len(a)) if a[row][column]), None)
        if pivot is None:
            return Fraction(0)
        if pivot != column:
            a[column], a[pivot] = a[pivot], a[column]
            result = -result
        pivot_value = a[column][column]
        result *= pivot_value
        for row in range(column + 1, len(a)):
            scale = a[row][column] / pivot_value
            for j in range(column, len(a)):
                a[row][j] -= scale * a[column][j]
    return result


def rank(matrix):
    a = [[Fraction(x) for x in row] for row in matrix]
    result = 0
    columns = len(a[0]) if a else 0
    for column in range(columns):
        pivot = next((row for row in range(result, len(a)) if a[row][column]), None)
        if pivot is None:
            continue
        a[result], a[pivot] = a[pivot], a[result]
        pivot_value = a[result][column]
        a[result] = [x / pivot_value for x in a[result]]
        for row in range(len(a)):
            if row != result and a[row][column]:
                scale = a[row][column]
                a[row] = [x - scale * y for x, y in zip(a[row], a[result])]
        result += 1
    return result


def audit_row(atoms, weights):
    r = len(atoms)
    moments = [sum(c * (a ** k) for a, c in zip(atoms, weights)) for k in range(2 * r + 1)]
    hankel = [[moments[u + v] for v in range(r)] for u in range(r)]
    actual = determinant(hankel)
    vandermonde_square = Fraction(1)
    for i in range(r):
        for j in range(i + 1, r):
            vandermonde_square *= (atoms[j] - atoms[i]) ** 2
    expected = vandermonde_square
    for weight in weights:
        expected *= weight
    assert actual == expected != 0
    extended = [[moments[u + v] for v in range(r + 1)] for u in range(r + 1)]
    assert rank(hankel) == r
    assert rank(extended) == r
    return {"support": r, "determinant": str(actual), "extended_hankel_rank": r}


def main():
    rows = [
        {(0, 0, 0): Fraction(2), (1, -1, 2): Fraction(-3), (2, 1, -1): Fraction(5)},
        {(-2, 3, 1): Fraction(-1, 2), (4, 0, -3): Fraction(7, 3)},
        {(1, 1, 1): Fraction(-4), (3, -2, 0): Fraction(-5), (0, 4, 2): Fraction(6), (-1, 0, 5): Fraction(1, 7)},
    ]
    union = sorted({point for row in rows for point in row})
    vector = separating_vector(union)
    projected = [dot(vector, point) for point in union]
    assert len(projected) == len(set(projected))
    audited = []
    for row in rows:
        atoms = [dot(vector, point) for point in row]
        audited.append(audit_row(atoms, list(row.values())))
    print(json.dumps({
        "pass": True,
        "common_vector": vector,
        "union_support": len(union),
        "projected_values_distinct": True,
        "rows": audited,
        "negative_weights_present": True,
        "scope": "finite guard only"
    }, indent=2))


if __name__ == "__main__":
    main()
