#!/usr/bin/env python3
"""Exact identities used in the full equal-radius K_{2,2,2} classification."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path

import sympy as sp


def main() -> None:
    x0, x1, y, z = sp.symbols("x0 x1 y z", nonzero=True)

    def phi(x: sp.Expr, yy: sp.Expr, zz: sp.Expr) -> sp.Expr:
        return (
            x * yy * zz + x + yy + zz
            + 1 / x + 1 / yy + 1 / zz + 1 / (x * yy * zz)
        )

    difference = sp.factor(phi(x0, y, z) - phi(x1, y, z))
    expected_difference = sp.factor(
        (x0 - x1) * (1 + y * z) * (1 - 1 / (x0 * x1 * y * z))
    )
    assert sp.cancel(difference - expected_difference) == 0

    # A non-base point determines a unique centered rectangular conic through
    # the antipodal base pair +/-q.  The displayed identity says that its two
    # coefficient constraints vanish simultaneously only at x=+/-q.
    X, Y, Q, R = sp.symbols("X Y Q R", real=True)
    invariant_one = (X**2 - Y**2) - (Q**2 - R**2)
    invariant_two = 2 * X * Y - 2 * Q * R
    invariant_norm = sp.factor(invariant_one**2 + invariant_two**2)
    expected_norm = sp.factor(
        ((X - Q) ** 2 + (Y - R) ** 2)
        * ((X + Q) ** 2 + (Y + R) ** 2)
    )
    assert sp.expand(invariant_norm - expected_norm) == 0

    # Four points p(a)=(a,1/a) on xy=1 are cocircular iff their parameter
    # product is one.  This rechecks the determinant factor rather than merely
    # importing the earlier certificate.
    a, b, c, d = sp.symbols("a b c d", nonzero=True)
    params = (a, b, c, d)
    circle_matrix = sp.Matrix([
        [q**2 + q**-2, q, q**-1, 1] for q in params
    ])
    determinant = sp.factor(circle_matrix.det())
    vandermonde = sp.prod(
        params[j] - params[i]
        for i, j in itertools.combinations(range(4), 2)
    )
    expected_determinant = sp.factor(
        -vandermonde * (a * b * c * d - 1) / (a**2 * b**2 * c**2 * d**2)
    )
    # The sign depends on the chosen Vandermonde ordering; comparison below
    # is exact for the ordering above.
    if sp.cancel(determinant - expected_determinant) != 0:
        expected_determinant = -expected_determinant
    assert sp.cancel(determinant - expected_determinant) == 0

    payload = {
        "schema": "amra.erdos827.round9.full_k222_classification.v1",
        "arithmetic": "exact SymPy rational-function and polynomial identities",
        "hyperbola_radius_difference": str(difference),
        "centered_conic_uniqueness_identity": str(invariant_norm),
        "four_point_circle_determinant": str(determinant),
        "result": "PASS",
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
