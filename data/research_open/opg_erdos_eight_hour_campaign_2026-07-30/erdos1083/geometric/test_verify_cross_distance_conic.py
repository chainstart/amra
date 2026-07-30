"""Tests for verify_cross_distance_conic.py."""

from fractions import Fraction

import verify_cross_distance_conic as conic


def test_random_geometric_identity() -> None:
    report = conic.random_identity_audit(trials=500, seed=57)
    assert report["maximum_scaled_conic_residual"] < 2e-13
    assert report["maximum_scaled_quotient_residual"] < 2e-13


def test_small_collision_enumeration() -> None:
    report = conic.collision_audit(modulus=17, alpha_index=2)
    assert report["ordered_distance_pairs"] == 17
    assert report["quotient_points"] == 9
    assert report["maximum_ordered_gamma_multiplicity"] == 1
    assert report["maximum_quotient_gamma_multiplicity"] == 2


def test_physical_incidence_capacity_barrier() -> None:
    report = conic.physical_capacity_barrier(curve_count=40)
    assert report["distinct_physical_parameters"] == 40
    assert report["maximum_residual"] < 1e-10


def test_exact_parameter_multiplicity_and_ledger() -> None:
    circles = [
        (Fraction(1), Fraction(0)),
        (Fraction(1), Fraction(1)),
        (Fraction(1), Fraction(2)),
        (Fraction(2), Fraction(0)),
        (Fraction(2), Fraction(1)),
    ]
    multiplicity = conic.parameter_multiplicity(circles)
    assert multiplicity == {
        "ordered_circle_pairs": 20,
        "distinct_parameters": 6,
        "maximum_parameter_multiplicity": 6,
    }
    ledger = conic.exponent_ledger()
    assert ledger["forced_joint_mass"] == "9/5"
    assert ledger["target_nD"] == "8/5"
    assert ledger["critical_contradiction_conditions"] == (
        "u<2/5 and ell>2/5+u/2"
    )
    assert ledger["global_target_J_conditions"] == (
        "u<=2/5 and ell>=1/2+u/4"
    )
