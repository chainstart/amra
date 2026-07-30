from fractions import Fraction

from verify_translation_hyperbola_energy import (
    arithmetic_progression_certificate,
    convex_square_certificate,
    exponent_ledger,
    geometric_progression_certificate,
    hyperbola_energy,
    partner_degrees,
    sat_base_resonant_star,
)


def test_energy_identity_matches_direct_degree_sum():
    values = tuple(Fraction(i) for i in range(7))
    energy = hyperbola_energy(values, Fraction(2), Fraction(1))
    direct = partner_degrees(values, Fraction(2), Fraction(1))
    assert energy["H"] == direct["sum_degrees"]
    assert energy["H"] <= energy["energy_bound"]
    assert energy["H"] <= energy["popular_difference_bound"]


def test_arithmetic_progression_exact_samples():
    expected = {3: 12, 5: 48, 10: 288, 20: 1368}
    for n, total in expected.items():
        assert arithmetic_progression_certificate(n)["H"] == total
    result = arithmetic_progression_certificate(10)
    assert set(result["difference_solutions"]) == {
        (Fraction(0), Fraction(0)),
        (Fraction(0), Fraction(-2)),
        (Fraction(-4), Fraction(0)),
        (Fraction(-4), Fraction(-2)),
    }
    assert result["maximum_degree"] == 4


def test_geometric_progression_is_ordered_difference_sidon():
    result = geometric_progression_certificate(9)
    counts = result["difference_counts"]
    assert max(m for difference, m in counts.items() if difference != 0) == 1
    assert result["additive_energy"] == 2 * 9 * 9 - 9
    assert result["H"] <= 4 * 9 * 9


def test_small_convex_square_search_stays_constant_degree():
    for n in range(3, 11):
        result = convex_square_certificate(n)
        assert result["maximum_degree"] == 2
        assert result["H"] == n * n + n


def test_sat_base_has_explicit_linear_degree_resonant_star():
    for r in (3, 5, 8):
        result = sat_base_resonant_star(r)
        assert result["R"] == -3069
        assert result["size"] == 2 * r + 1
        assert result["fixed_edge_degree"] >= r + 1
        assert len(result["witnesses"]) == r


def test_exponent_ledger_records_the_remaining_convex_gap():
    ledger = exponent_ledger()
    assert ledger["target_average_degree"] == Fraction(2, 5)
    assert ledger["forced_total_additive_energy"] == Fraction(12, 5)
    assert ledger["forced_nonzero_popular_difference"] == Fraction(2, 5)
    assert (
        ledger["classical_convex_energy_average_bound"]
        > ledger["target_average_degree"]
    )
