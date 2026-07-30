from fractions import Fraction

from verify_escape_route_audit import (
    actual_quadratic_gap_certificate,
    breakthrough_target_ledger,
    direct_actual_quadratic_gap_energy,
    generic_rank_two_gap_lemma,
    multiple_layer_mass_ledger,
    quadratic_unit_orbit_count,
    rational_s_unit_lattice_certificate,
)


def test_actual_quadratic_gap_has_only_four_fixed_solutions():
    for length in range(4, 15):
        result = actual_quadratic_gap_certificate(length)
        assert len(result["supported_coefficient_pairs"]) == 4
        expected = (
            length**2 * (2 * length - 3) * (2 * length - 2)
        )
        assert result["H"] == expected
        assert result["average_degree"] < 4


def test_quadratic_gap_formula_matches_direct_weighted_enumeration():
    for length in range(2, 9):
        formula = actual_quadratic_gap_certificate(length)
        direct = direct_actual_quadratic_gap_energy(length)
        assert direct["H"] == formula["H"]
        assert len(direct["supported"]) == len(
            formula["supported_coefficient_pairs"]
        )


def test_generic_rank_two_gap_collapses_to_the_rational_axis():
    result = generic_rank_two_gap_lemma()
    assert result["supported_pairs"] == ((0, 0), (3, 0))
    assert result["average_upper_bound"] == "2-1/n"


def test_fixed_quadratic_unit_orbit_is_logarithmic_in_height():
    previous = 0
    for bound in (10, 100, 10_000, 10**8, 10**16):
        result = quadratic_unit_orbit_count(bound)
        assert result["signed_power_count"] > previous
        assert result["logarithmic_comparison"]
        previous = result["signed_power_count"]


def test_rational_multiplicative_subgroup_returns_to_divisor_scale():
    for prime_count in range(2, 8):
        result = rational_s_unit_lattice_certificate(prime_count)
        assert result["parameter_count"] == 2**prime_count
        assert result["average_lower_bound"] >= result["uniform_average_lower_bound"]
        assert result["growth_class"] == "exp(Theta(log(n)/loglog(n)))"


def test_multiple_layers_add_or_dilute_but_do_not_multiply_degrees():
    result = multiple_layer_mass_ledger(
        (10, 20, 30),
        (Fraction(3), Fraction(5), Fraction(7)),
    )
    assert result["union_average_degree"] <= result["union_upper_bound"]
    assert result["tensor_size"] == 6000
    assert result["tensor_average_degree"] == 13


def test_breakthrough_target_is_quantitative():
    result = breakthrough_target_ledger()
    assert result["target_average_degree"] == "n^(2/5)"
    assert "n^(12/5)" in result["equivalent_weighted_incidence"]
