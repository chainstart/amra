"""Regression tests for verify_growing_depth_heat.py."""

from fractions import Fraction

import sympy as sp

import verify_growing_depth_heat as heat


def test_heat_expansion_and_exact_component_counts() -> None:
    report = heat.audit(order=4)
    assert report["exact_count_checks"] == 21
    assert report["kernel_coefficients"]["0"] == "0"
    assert report["kernel_coefficients"]["1"] == "0"
    assert report["kernel_coefficients"]["2"] == "4*z"
    assert report["kernel_coefficients"]["3"] == "16*z**2"
    assert report["kernel_coefficients"]["4"] == "8*z**2*(5*z - 12)"
    assert report["diagonal_polynomials"]["2"] == "4*R"
    assert report["diagonal_polynomials"]["3"] == "16*R*(R - 1)"
    assert report["diagonal_polynomials"]["4"] == (
        "8*R*(R - 1)*(5*R - 22)"
    )


def test_exact_determinant_matches_full_heat_coefficient() -> None:
    # For t=5 the determinant z-degree is three and u-degree is at most six,
    # so the order-six heat expansion is the full exact coefficient.
    rows = heat.determinant_kernel(order=6)
    exact = heat.exact_normalized_determinant(24, 5)
    from_heat = heat.kernel_coefficient(rows["kernel"], 24, 5)
    assert exact == Fraction(34985, 7962624)
    assert from_heat == exact


def test_tilted_gaussian_moments() -> None:
    assert heat.tilted_gaussian_moment(0) == 1
    assert heat.tilted_gaussian_moment(1) == 0
    assert heat.tilted_gaussian_moment(2) == -heat.Z
    assert sp.expand(heat.tilted_gaussian_moment(4)) == (
        3 * heat.Z**2
    )


def test_exact_newton_stress_grid() -> None:
    report = heat.stress_audit(maximum_k=20)
    assert report["checked_newton_coefficients"] == 56
    assert report["scope"] == "Exact integer stress test; not a proof."
