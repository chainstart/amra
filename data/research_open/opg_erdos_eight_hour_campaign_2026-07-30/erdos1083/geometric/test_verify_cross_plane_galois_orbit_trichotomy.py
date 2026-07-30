"""Tests for the cross-plane Galois-orbit trichotomy."""

from fractions import Fraction

from verify_cross_plane_galois_orbit_trichotomy import (
    audit,
    critical_orbit_threshold,
    cyclotomic_label_degree_checks,
    cyclotomic_tensor,
    cyclotomic_tensor_ledger,
    heavy_label_audit,
    label_statistics,
    orbit_expansion_audit,
    verify_tensor_against_closed_ledger,
)


def test_heavy_label_theorem_on_nonuniform_matrix():
    weights = [
        [5, 0, 2, 1],
        [4, 3, 0, 1],
        [0, 3, 2, 1],
        [1, 0, 2, 1],
    ]
    result = heavy_label_audit(weights, Fraction(2, 5))
    assert result["heavy_label_count"] >= 1
    assert Fraction(result["heavy_energy_fraction"]) >= Fraction(3, 5)


def test_exact_cyclotomic_tensor_formulas():
    for prime in (5, 7, 11):
        ledger = cyclotomic_tensor_ledger(prime)
        degree = (prime - 1) // 2
        assert ledger["labels"] == degree * prime**2
        assert ledger["row_support"] == degree * prime
        assert ledger["label_support"] == prime
        assert ledger["row_mass"] == degree * prime**5
        assert ledger["label_mass"] == prime**5
        assert ledger["cross_codegree"] == degree * prime**11 * (prime - 1)
        assert ledger["orbit_inequality_is_exact"]
        assert ledger["orbit_lower_bound"] == str(ledger["labels"])


def test_enumerated_tensor_matches_closed_ledger():
    result = verify_tensor_against_closed_ledger(5)
    assert result["closed_ledger_match"]
    assert result["matrix_rows"] == 25
    assert result["matrix_labels"] == 50


def test_heavy_labels_and_orbit_bound_are_exact_on_cyclotomic_model():
    prime = 5
    degree = 2
    matrix = cyclotomic_tensor(prime)
    stats = label_statistics(matrix)
    heavy = heavy_label_audit(matrix, Fraction(1, 2))
    assert heavy["heavy_label_count"] == degree * prime**2
    assert heavy["heavy_energy_fraction"] == "1"

    orbits = [
        [
            chord_index * prime * prime + shift
            for chord_index in range(degree)
        ]
        for shift in range(prime * prime)
    ]
    orbit_result = orbit_expansion_audit(
        stats["codegrees"], orbits, degree
    )
    assert orbit_result["degree_orbit_lower_bound"] == str(
        degree * prime**2
    )
    assert orbit_result["density_lower_bound"] == str(
        degree * prime**2
    )


def test_cyclotomic_labels_have_expected_degree():
    checks = cyclotomic_label_degree_checks(5, shifts=(0, 1, 2))
    assert len(checks) == 6
    assert {check["degree"] for check in checks} == {2}


def test_critical_exponent_threshold():
    result = critical_orbit_threshold(
        Fraction(13), Fraction(1), Fraction(3)
    )
    assert result["orbit_energy_threshold_exponent"] == "11"
    assert result["average_per_label_threshold_exponent"] == "10"
    improved = critical_orbit_threshold(
        Fraction(13), Fraction(1), Fraction(13, 4)
    )
    assert improved["orbit_energy_threshold_exponent"] == "43/4"
    assert improved["average_per_label_threshold_exponent"] == "39/4"


def test_full_audit():
    result = audit()
    assert result["verdict"] == "PASS"
    assert result["minimal_polynomial_checks"] == 10
    assert result["explicit_tensor_check"]["closed_ledger_match"]
