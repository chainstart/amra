from fractions import Fraction

from verify_euclidean_hub_incidence import (
    audit,
    conditional_kappa_threshold,
    finite_circle_injectivity_check,
    forced_repeat_exponent,
    hub_exponent_ledger,
)


def test_reverse_circle_injectivity_and_perpendicular_exception():
    result = finite_circle_injectivity_check()
    assert result["nonperpendicular_parameter_triples"] == 210
    assert result["distinct_nonperpendicular_circles"] == 210
    assert result["perpendicular_opposite_collision"] == 1
    assert result["cross_plane_cosine_radial_collision"] == 1


def test_one_fifth_threshold_and_balanced_gap():
    assert hub_exponent_ledger(Fraction(1, 5))[
        "total_saving"
    ] == 0
    balanced = hub_exponent_ledger(Fraction(1, 2))
    assert balanced["upper_total"] == Fraction(65, 11)
    assert balanced["lower_total"] == Fraction(11, 2)
    assert balanced["total_saving"] == Fraction(-9, 22)


def test_conditional_saving_threshold():
    assert conditional_kappa_threshold(Fraction(0)) == Fraction(1, 5)
    assert conditional_kappa_threshold(Fraction(9, 22)) == Fraction(
        1, 2
    )


def test_cross_plane_repeat_exponent():
    assert forced_repeat_exponent(Fraction(1, 5)) == Fraction(2, 11)
    assert forced_repeat_exponent(Fraction(1, 4)) == Fraction(5, 44)
    assert forced_repeat_exponent(Fraction(1, 3)) == 0


def test_full_hub_audit():
    result = audit()
    assert result["status"] == "PASS"
    assert result["unconditional_hub_exclusion"] == "0 < kappa < 1/5"
