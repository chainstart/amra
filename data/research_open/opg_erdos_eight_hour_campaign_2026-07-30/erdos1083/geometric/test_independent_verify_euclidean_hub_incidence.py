from fractions import Fraction

from independent_verify_euclidean_hub_incidence import (
    audit,
    audit_exponents,
    audit_ordered_unordered_conversion,
    audit_repeated_circle_refinement,
    audit_reverse_circles,
)


def test_reverse_circle_and_radius_audit():
    result = audit_reverse_circles()
    assert result["nonperpendicular_cosines_checked"] == 4
    assert result["radius_classes"] == {
        "real": "9/25",
        "zero": "0",
        "imaginary": "-39/25",
    }


def test_ordered_unordered_energy_conversion():
    result = audit_ordered_unordered_conversion()
    assert result["unordered_codegree"] == 122
    assert result["directed_codegree"] == 704


def test_exact_exponent_ledger():
    result = audit_exponents()
    assert result["threshold"] == "kappa < 1/5"
    assert result["gaps"]["six_eleven"] == ("3/11", "-15/11")
    assert Fraction(1, 5) - Fraction(1, 100) > 0


def test_cross_plane_repeated_circle_refinement():
    result = audit_repeated_circle_refinement()
    assert result["forced_mu_exponent"] == ("5/11", "-15/11")
    assert result["positive_range"] == "kappa < 1/3"
    assert result["cross_plane_collision_checked"] is True


def test_full_independent_audit():
    assert audit()["status"] == "PASS"
