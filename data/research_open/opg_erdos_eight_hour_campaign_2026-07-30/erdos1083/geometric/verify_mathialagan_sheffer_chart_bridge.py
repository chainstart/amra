#!/usr/bin/env python3
"""Parameter and exponent checks for the known two-circle bridge."""

from __future__ import annotations

import json
import math
from fractions import Fraction

import sympy as sp


BALANCED_CRITICAL_INCIDENCE_EXPONENT = Fraction(9, 4)


def chart_exception(
    *,
    alpha1: float,
    alpha2: float,
    A1: float,
    A2: float,
    w1: float,
    w2: float,
    tolerance: float = 1e-10,
) -> str:
    theta = alpha2 - alpha1
    cosine = math.cos(theta)
    sine = math.sin(theta)
    delta = A1 - A2 * cosine
    delta_w = w1 - w2
    aligned = (
        abs(sine) <= tolerance
        and abs(delta) <= tolerance
        and abs(delta_w) <= tolerance
    )
    perpendicular = (
        abs(cosine) <= tolerance
        and abs(A1) <= tolerance
        and abs(A2) <= tolerance
    )
    if aligned:
        return "aligned"
    if perpendicular:
        return "perpendicular"
    return "expanding"


def source_distance_exponent(a1: float, a2: float) -> float:
    """Exponent supplied by Mathialagan--Sheffer Theorem 1.4(b)."""
    return min(2 * (a1 + a2) / 3, 2 * a1, 2 * a2)


def symbolic_special_case_certificates() -> dict[str, bool]:
    zero = sp.Integer(0)
    one = sp.Integer(1)
    three = sp.Integer(3)

    def aligned(cosine, sine, A1, A2, delta_w):
        return bool(
            sp.simplify(sine) == 0
            and sp.simplify(delta_w) == 0
            and sp.simplify(A1 - A2 * cosine) == 0
        )

    def perpendicular(cosine, A1, A2):
        return bool(
            sp.simplify(cosine) == 0
            and sp.simplify(A1) == 0
            and sp.simplify(A2) == 0
        )

    return {
        "theta_zero_aligned": aligned(one, zero, three, three, zero),
        "theta_pi_aligned": aligned(-one, zero, three, -three, zero),
        "theta_zero_wrong_center_not_aligned": not aligned(
            one, zero, three, three + one, zero
        ),
        "theta_pi_wrong_sign_not_aligned": not aligned(
            -one, zero, three, three, zero
        ),
        "theta_half_pi_formal_perpendicular": perpendicular(
            zero, zero, zero
        ),
        "theta_half_pi_active_not_perpendicular": not perpendicular(
            zero, one, three
        ),
    }


def audit() -> dict[str, object]:
    classifications = {
        "same_frame_aligned": chart_exception(
            alpha1=0.2, alpha2=0.2, A1=2.0, A2=2.0, w1=0.7, w2=0.7
        ),
        "sign_reversed_aligned": chart_exception(
            alpha1=0.2,
            alpha2=0.2 + math.pi,
            A1=2.0,
            A2=-2.0,
            w1=0.7,
            w2=0.7,
        ),
        "formal_perpendicular": chart_exception(
            alpha1=0.0,
            alpha2=math.pi / 2,
            A1=0.0,
            A2=0.0,
            w1=-1.0,
            w2=3.0,
        ),
        "nonzero_A_excludes_perpendicular": chart_exception(
            alpha1=0.0,
            alpha2=math.pi / 2,
            A1=1.0,
            A2=2.0,
            w1=-1.0,
            w2=3.0,
        ),
        "generic": chart_exception(
            alpha1=-0.4,
            alpha2=0.9,
            A1=1.2,
            A2=2.3,
            w1=0.1,
            w2=-0.6,
        ),
    }
    expected = {
        "same_frame_aligned": "aligned",
        "sign_reversed_aligned": "aligned",
        "formal_perpendicular": "perpendicular",
        "nonzero_A_excludes_perpendicular": "expanding",
        "generic": "expanding",
    }
    if classifications != expected:
        raise AssertionError("chart exception translation failed")

    symbolic = symbolic_special_case_certificates()
    if not all(symbolic.values()):
        raise AssertionError("exact symbolic exception certificate failed")

    threshold = BALANCED_CRITICAL_INCIDENCE_EXPONENT
    if source_distance_exponent(threshold, threshold) != 3:
        raise AssertionError("balanced critical threshold failed")
    if source_distance_exponent(threshold + Fraction(3, 100), threshold + Fraction(3, 100)) <= 3:
        raise AssertionError("balanced supercritical consequence failed")
    if not math.isclose(source_distance_exponent(1.5, 3.0), 3.0):
        raise AssertionError("asymmetric threshold failed")

    return {
        "schema": "amra.erdos1083.mathialagan-sheffer-chart-bridge.v1",
        "status": "PASS",
        "classifications": classifications,
        "symbolic_special_cases": symbolic,
        "balanced_incidence_exponent": str(threshold),
        "balanced_distance_exponent": str(
            source_distance_exponent(threshold, threshold)
        ),
        "perpendicular_excluded_when_A_nonzero": True,
    }


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2, sort_keys=True))
