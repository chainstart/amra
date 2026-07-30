"""Regression tests for the critical anisotropic coaxial grid."""

from verify_critical_anisotropic_grid import (
    chebyshev_value,
    critical_family,
    enumerated_ledger,
    exact_affine_union_count,
    exact_formula,
    exponent_ledger,
    odd_prime_angular_escape,
    rational_cosine_search,
    two_adic_angular_escape,
)
from fractions import Fraction


def test_closed_forms_match_complete_pair_enumeration() -> None:
    for radius_count in range(1, 6):
        for height_count in range(1, 8):
            assert enumerated_ledger(
                radius_count, height_count
            ) == exact_formula(radius_count, height_count)


def test_critical_family_hits_both_thresholds() -> None:
    for t in range(2, 8):
        row = critical_family(t)
        assert row["circle_count_F"] == t**3
        assert row["point_count_N"] == t**5
        assert row["angular_pattern_size_S"] == t**2
        assert row["distinct_parameter_lines_M"] == t**2 * t * (t + 1) // 2
        assert row["maximum_line_multiplicity"] == 2 * (t**2 - 1)


def test_exponent_ledger_reconnects_exactly_to_three_fifths() -> None:
    ledger = exponent_ledger()
    assert ledger["threshold_duality"] == "3/5"
    assert "3/5+(3/10)*abs(alpha-2/3)" == ledger["combined_exponent"]
    assert "3delta/10" in ledger["fixed_gain_condition"]


def test_exact_rational_cosine_pressure_search() -> None:
    assert [
        (
            row["affine_union_count"],
            row["cosine"],
        )
        for row in (rational_cosine_search(t) for t in range(2, 6))
    ] == [
        (32, "1/2"),
        (441, "3/4"),
        (2281, "3/4"),
        (8900, "3/4"),
    ]


def test_three_quarters_chebyshev_denominators_are_strict() -> None:
    for k in range(1, 101):
        value = Fraction(1) - chebyshev_value(Fraction(3, 4), k)
        assert value.denominator == 2 ** (k + 1)
        assert value.numerator % 2 == 1


def test_two_adic_escape_bound_is_seen_in_complete_union() -> None:
    for t in range(2, 6):
        escape = two_adic_angular_escape(t * t, t * t)
        exact = rational_cosine_search(t)
        # The search minimum is no larger than the 3/4 instance, so compute
        # the latter through the public exact counter in the next assertion.
        full_count = exact_affine_union_count(t, Fraction(3, 4))
        assert full_count is not None
        assert full_count - 1 >= escape["certified_distances"]
        assert exact["affine_union_count"] >= t**3
        assert exact["nonzero_distance_count"] == (
            exact["affine_union_count"] - 1
        )


def test_odd_prime_chebyshev_valuations_and_escape_bound() -> None:
    examples = (
        (Fraction(2, 3), 3, 1),
        (Fraction(3, 5), 5, 1),
        (Fraction(4, 9), 3, 2),
    )
    for cosine, prime, denominator_valuation in examples:
        for k in range(1, 30):
            value = Fraction(1) - chebyshev_value(cosine, k)
            denominator = value.denominator
            valuation = 0
            while denominator % prime == 0:
                valuation += 1
                denominator //= prime
            assert valuation == denominator_valuation * k

    for t in range(2, 6):
        escape = odd_prime_angular_escape(t * t, t * t, 3, 3)
        full_count = exact_affine_union_count(t, Fraction(2, 3))
        assert full_count is not None
        assert full_count - 1 >= escape["certified_distances"]
