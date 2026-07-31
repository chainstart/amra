from fractions import Fraction

from verify_rough_order_cyclotomic_escape import (
    audit,
    canonical_label,
    mann_arithmetic_row,
    polynomial_remainder,
)


def test_rough_order_audit_passes():
    result = audit()
    assert result["exact_quotient_arithmetic"] is True
    assert result["prime_power_quotient_comparisons"] == 24
    assert result["status"] == "finite_audit_passed"
    for row in result["injection_checks"]:
        assert row["exact_selected_labels"] >= row["kneser_class_lower_total"]


def test_mann_coprimality_for_non_prime_powers():
    for order in (77, 91, 143, 1001):
        row = mann_arithmetic_row(order)
        assert row["gcd_with_30"] == 1
        assert all(row["short_relation_coprime_checks"].values())


def test_exact_non_prime_power_labels_are_distinct():
    first = canonical_label(77, Fraction(1), 3, Fraction(1, 4))
    second = canonical_label(77, Fraction(9, 4), 8, Fraction(4, 9))
    assert first != second


def test_embedded_seven_gon_relation_at_order_77():
    relation = polynomial_remainder(77, set(range(0, 77, 11)))
    assert relation == (Fraction(0),) * 60


def test_five_term_boundary_at_order_35():
    relation = polynomial_remainder(35, set(range(0, 35, 7)))
    assert relation == (Fraction(0),) * 24
