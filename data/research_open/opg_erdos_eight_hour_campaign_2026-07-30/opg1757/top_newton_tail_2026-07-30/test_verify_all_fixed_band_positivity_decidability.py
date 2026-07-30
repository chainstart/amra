import sympy as sp

from verify_all_fixed_band_positivity_decidability import (
    U,
    audit,
    cauchy_bound,
    exact_integer_interval_decision,
)


def test_exact_cauchy_bound_and_negative_instance():
    polynomial = sp.Poly(U**2 - 2, U)
    assert cauchy_bound(polynomial) == 3
    result = exact_integer_interval_decision(polynomial)
    assert not result["positive_on_all_nonnegative_integers"]
    assert result["violations"] == [0, 1]


def test_mixed_coefficient_positive_integer_instance():
    polynomial = sp.Poly(U**2 - 2 * U + 2, U)
    result = exact_integer_interval_decision(polynomial)
    assert result["positive_on_all_nonnegative_integers"]
    assert result["method"] == "explicit exact Cauchy-interval enumeration"
    assert result["finite_check_endpoint"] == 3


def test_first_eight_band_replay():
    result = audit()
    assert result["status"] == "PASS"
    certificates = result["replayed_positive_bands"]
    assert len(certificates) == 8
    for band, certificate in enumerate(certificates):
        assert certificate["band"] == band
        assert certificate["minimum_depth"] == 2 * band + 1
        assert certificate["degree"] == 3 * band + 2
        assert certificate["positive_on_all_nonnegative_integers"]
        assert certificate["coefficientwise_positive"]
