#!/usr/bin/env python3
"""Exact certificate for the general-position antipodal radius-cube classification.

The script verifies polynomial identities only.  The infinite theorem and the
geometric exclusion of the factors are written in REPORT.md.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp


def main() -> None:
    u, v, w, t = sp.symbols("u v w t", real=True)

    common = (
        t**2 * u * v + t * u**2 * w - t * v**2 * w
        - t * w - u * v * w**2 + u * v
    )

    # After removing a nonzero squared-distance factor, these are the two
    # residual factors in R(a,b,c)^2-R(-a,b,c)^2 and
    # R(a,b,c)^2-R(a,-b,c)^2, respectively.
    residual_a = t**2 * v - t * u**2 - t * v**2 + t + v * w**2 - v
    residual_b = (
        t**2 * v - t * u**3 - t * u * v**2 + t * u
        + u**2 * v * w - u**2 * v + v**3 * w - v**3
        + v * w**2 - v * w
    )

    resultant = sp.factor(sp.resultant(residual_a, residual_b, t))
    expected_resultant = sp.factor(
        -v**2 * (u - w) * (w - 1) * (u**2 + v**2 - 1) ** 2
        * ((u - 1) ** 2 + v**2)
    )
    assert sp.expand(resultant - expected_resultant) == 0

    branch_equal_x_a = {
        "residual_a": sp.factor(residual_a.subs(w, u)),
        "residual_b": sp.factor(residual_b.subs(w, u)),
    }
    assert branch_equal_x_a["residual_a"] == (t - v) * (t * v - u**2 + 1)
    assert branch_equal_x_a["residual_b"] == sp.factor(
        (t - v) * (t * v - u**3 - u * v**2 + u + v**2)
    )
    branch_equal_x_a_difference = sp.factor(
        (t * v - u**3 - u * v**2 + u + v**2)
        - (t * v - u**2 + 1)
    )
    assert sp.expand(
        branch_equal_x_a_difference + (u - 1) * (u**2 + v**2 - 1)
    ) == 0

    branch_equal_x_one = {
        "residual_a": sp.factor(residual_a.subs(w, 1)),
        "residual_b": sp.factor(residual_b.subs(w, 1)),
    }
    assert branch_equal_x_one["residual_a"] == t * (
        t * v - u**2 - v**2 + 1
    )
    assert branch_equal_x_one["residual_b"] == sp.factor(
        t * (t * v - u**3 - u * v**2 + u)
    )
    branch_equal_x_one_difference = sp.factor(
        (t * v - u**3 - u * v**2 + u)
        - (t * v - u**2 - v**2 + 1)
    )
    assert sp.expand(
        branch_equal_x_one_difference + (u - 1) * (u**2 + v**2 - 1)
    ) == 0

    # Collinearity of 1, (u+iv)^2 and (w+it)^2.
    collinearity = sp.expand(
        2 * u * v * (w**2 - t**2 - 1)
        - (u**2 - v**2 - 1) * 2 * w * t
    )
    assert sp.expand(collinearity + 2 * common) == 0

    payload = {
        "schema": "amra.erdos827.round9.antipodal_classification.v1",
        "arithmetic": "exact symbolic polynomial arithmetic over ZZ",
        "normalization": "a=(1,0), b=(u,v), c=(w,t)",
        "common_factor": str(sp.factor(common)),
        "collinearity_identity": "Im((b^2-1)conj(c^2-1))=-2F",
        "residual_resultant": str(resultant),
        "u_equals_w_branch": {
            key: str(value) for key, value in branch_equal_x_a.items()
        },
        "u_equals_w_difference": str(branch_equal_x_a_difference),
        "w_equals_one_branch": {
            key: str(value) for key, value in branch_equal_x_one.items()
        },
        "w_equals_one_difference": str(branch_equal_x_one_difference),
        "result": "PASS",
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
