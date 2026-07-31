from verify_prime_power_cyclotomic_escape import (
    audit,
    canonical_label,
    kneser_row,
    quotient_vector,
    relation_vector,
    sign_classes,
)

from fractions import Fraction


def test_prime_power_audit_passes():
    result = audit()
    assert result["exact_quotient_arithmetic"] is True
    assert result["status"] == "finite_audit_passed"
    assert len(result["relation_space_checks"]) == 3
    assert len(result["injection_checks"]) == 2
    for row in result["relation_space_checks"]:
        assert row["relation_basis_size"] == row["relation_nullity"]
        assert row["minimum_nonzero_relation_support"] >= 7
    for row in result["injection_checks"]:
        assert row["exact_selected_labels"] >= row["kneser_class_lower_total"]


def test_relation_basis_reduces_to_zero_at_order_49():
    for residue in range(7):
        assert relation_vector(7, 2, residue) == (Fraction(0),) * 42


def test_quotient_reduction_uses_prime_power_cyclotomic_polynomial():
    coefficients = [Fraction(0) for _ in range(49)]
    for exponent in range(0, 49, 7):
        coefficients[exponent] = Fraction(1)
    assert quotient_vector(7, 2, coefficients) == (Fraction(0),) * 42


def test_distinct_prime_power_labels():
    left = canonical_label(7, 2, Fraction(1), 3, Fraction(1, 4))
    right = canonical_label(7, 2, Fraction(9, 4), 8, Fraction(4, 9))
    assert left != right


def test_periodic_kneser_bound_is_sharp():
    subgroup = set(range(0, 49, 7))
    row = kneser_row(49, subgroup, subgroup)
    assert row["stabilizer_size"] == 7
    assert row["difference_size"] == 7
    assert row["kneser_lower"] == 7
    assert row["sign_classes"] == row["sign_class_lower"] == 3


def test_aperiodic_prime_like_bound():
    left = {0, 1, 4, 13}
    right = {0, 2, 9, 21}
    row = kneser_row(49, left, right)
    assert row["stabilizer_size"] == 1
    assert row["kneser_lower"] == len(left) + len(right) - 1
    assert row["sign_classes"] >= len(left) - 1


def test_sign_classes_identify_opposite_differences():
    assert sign_classes(49, {0}, {1, 48, 7, 42}) == {1, 7}
