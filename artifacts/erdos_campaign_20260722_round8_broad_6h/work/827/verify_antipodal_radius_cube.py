#!/usr/bin/env python3
"""Exact symbolic/finite audit for the antipodal radius-cube obstruction.

The computation is a certificate for identities stated in
``route_audit_and_antipodal_obstruction.md``.  It is not an asymptotic
computation and makes no claim about Erdős #827 itself.
"""

from __future__ import annotations

import itertools
import json
from fractions import Fraction

import sympy as sp


def symbolic() -> dict[str, str]:
    u, v, w, t = sp.symbols("u v w t", real=True)

    def n2(x: sp.Matrix) -> sp.Expr:
        return sp.expand(x.dot(x))

    def cross(x: sp.Matrix, y: sp.Matrix) -> sp.Expr:
        return sp.expand(x[0] * y[1] - x[1] * y[0])

    def radius2(x: sp.Matrix, y: sp.Matrix, z: sp.Matrix) -> sp.Expr:
        return sp.factor(
            n2(x - y) * n2(x - z) * n2(y - z)
            / (4 * cross(y - x, z - x) ** 2)
        )

    a = sp.Matrix([1, 0])
    b = sp.Matrix([u, v])
    c = sp.Matrix([w, t])
    base = radius2(a, b, c)
    common = sp.factor(
        t**2 * u * v + t * u**2 * w - t * v**2 * w
        - t * w - u * v * w**2 + u * v
    )
    differences: dict[str, str] = {}
    for signs in ((1, 1, -1), (1, -1, 1), (-1, 1, 1)):
        other = radius2(signs[0] * a, signs[1] * b, signs[2] * c)
        numerator = sp.factor(sp.together(base - other).as_numer_denom()[0])
        quotient = sp.factor(numerator / common)
        assert sp.expand(numerator - common * quotient) == 0
        differences[str(signs)] = str(quotient)

    # If B=(u+iv)^2 and C=(w+it)^2, then the collinearity of
    # 1,B,C is Im((B-1)*conj(C-1))=0.  Its imaginary part is -2*common.
    re_b, im_b = u**2 - v**2, 2 * u * v
    re_c, im_c = w**2 - t**2, 2 * w * t
    imag_product = sp.expand(im_b * (re_c - 1) - (re_b - 1) * im_c)
    assert sp.expand(imag_product + 2 * common) == 0

    return {
        "normalization": "a=(1,0), b=(u,v), c=(w,t)",
        "common_factor": str(common),
        "complex_collinearity_imaginary_part": str(imag_product),
        "identity": "Im(((u+iv)^2-1)*conj((w+it)^2-1))=-2*common_factor",
        "three_sign_flip_quotients": json.dumps(differences, sort_keys=True),
        "result": "PASS",
    }


Point = tuple[Fraction, Fraction]


def det(matrix: list[list[Fraction]]) -> Fraction:
    ans = Fraction(0)
    for permutation in itertools.permutations(range(len(matrix))):
        inversions = sum(
            permutation[i] > permutation[j]
            for i in range(len(permutation))
            for j in range(i + 1, len(permutation))
        )
        term = Fraction(1)
        for i, j in enumerate(permutation):
            term *= matrix[i][j]
        ans += -term if inversions % 2 else term
    return ans


def cross(a: Point, b: Point, c: Point) -> Fraction:
    return ((b[0] - a[0]) * (c[1] - a[1])
            - (b[1] - a[1]) * (c[0] - a[0]))


def radius2(a: Point, b: Point, c: Point) -> Fraction:
    def distance2(x: Point, y: Point) -> Fraction:
        return (x[0] - y[0]) ** 2 + (x[1] - y[1]) ** 2

    area2 = cross(a, b, c)
    assert area2
    return (distance2(a, b) * distance2(a, c) * distance2(b, c)
            / (4 * area2**2))


def finite() -> dict[str, object]:
    groups: tuple[tuple[Point, Point], ...] = (
        ((Fraction(1), Fraction(0)), (Fraction(-1), Fraction(0))),
        ((Fraction(1), Fraction(1)), (Fraction(-1), Fraction(-1))),
        ((Fraction(2), Fraction(3)), (Fraction(-2), Fraction(-3))),
    )
    points = tuple(itertools.chain.from_iterable(groups))
    collinear = []
    for ids in itertools.combinations(range(6), 3):
        if cross(*(points[i] for i in ids)) == 0:
            collinear.append(ids)
    cocircular = []
    for ids in itertools.combinations(range(6), 4):
        matrix = []
        for i in ids:
            x, y = points[i]
            matrix.append([x*x + y*y, x, y, Fraction(1)])
        if det(matrix) == 0:
            cocircular.append(ids)
    radii = [radius2(*triple) for triple in itertools.product(*groups)]
    assert not collinear and not cocircular
    assert radii == [Fraction(25, 2)] * 8
    return {
        "points": [[str(x), str(y)] for x, y in points],
        "general_position": True,
        "transversal_triangles": 8,
        "common_radius_squared": "25/2",
        "result": "PASS",
    }


if __name__ == "__main__":
    print(json.dumps({
        "schema": "amra.erdos827.round8.antipodal_radius_cube.v1",
        "symbolic": symbolic(),
        "finite_exact_example": finite(),
    }, indent=2, sort_keys=True))
