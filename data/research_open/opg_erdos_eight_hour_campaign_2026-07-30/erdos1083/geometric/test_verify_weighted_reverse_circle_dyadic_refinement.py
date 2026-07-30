from fractions import Fraction

from verify_weighted_reverse_circle_dyadic_refinement import (
    audit,
    multiplicity_thresholds,
    sharp_threshold,
    term_exponents,
)


def test_exact_term_exponents():
    kappa = Fraction(1, 4)
    multiplicity = Fraction(5, 8)
    terms = term_exponents(kappa, multiplicity)
    hub = 7 - 3 * kappa
    assert terms[1] == hub
    assert terms[0] < hub
    assert terms[2] < hub
    assert terms[3] < hub


def test_second_incidence_term_gives_minimal_threshold():
    for kappa in (Fraction(1, 10), Fraction(1, 5), Fraction(1, 4)):
        thresholds = multiplicity_thresholds(kappa)
        assert thresholds[1] == min(thresholds)
        assert thresholds[1] == sharp_threshold(kappa)


def test_endpoint_and_old_bound_improvement():
    assert sharp_threshold(Fraction(1, 5)) == 1
    assert sharp_threshold(Fraction(1, 3)) == 0
    for kappa in (Fraction(1, 5), Fraction(1, 4), Fraction(3, 10)):
        old = Fraction(5 - 15 * kappa, 11)
        assert sharp_threshold(kappa) > old


def test_subthreshold_cannot_carry_hub_mass():
    kappa = Fraction(2, 9)
    threshold = sharp_threshold(kappa)
    hub = 7 - 3 * kappa
    assert max(term_exponents(kappa, threshold - Fraction(1, 100))) < hub


def test_full_weighted_dyadic_audit():
    result = audit()
    assert result["status"] == "PASS"
    assert result["rational_kappa_cases"] == 91
    assert result["kappa_one_fourth_threshold"] == "5/8"
