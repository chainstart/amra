from fractions import Fraction

from verify_resonant_multistar_optimization import (
    multistar_cube_certificate,
    rational_lattice_optima,
    rational_sat_bound,
    sat_candidate_optima,
    sat_star_candidate_universe,
    two_layer_reduction_certificate,
)


def test_rational_lattice_all_subset_optima_are_step_two_progressions():
    optima = rational_lattice_optima()
    assert len(optima[12]["values"]) == 12
    for n in range(2, 13):
        assert optima[n]["H"] == (2 * n - 1) * (2 * n - 2)


def test_actual_sat_candidate_universe_is_exhaustively_optimized():
    assert len(sat_star_candidate_universe()) == 17
    expected = {
        1: 1,
        2: 4,
        3: 10,
        4: 18,
        5: 29,
        6: 42,
        7: 57,
        8: 75,
        9: 95,
        10: 114,
        11: 136,
        12: 160,
    }
    optima = sat_candidate_optima()
    assert {n: optima[n]["H"] for n in expected} == expected
    assert max(optima[n]["average_degree"] for n in expected) == Fraction(95, 81)


def test_rational_translations_at_actual_sat_parameters_have_average_below_two():
    for n in range(1, 13):
        values = tuple(Fraction(3 * i) for i in range(n))
        result = rational_sat_bound(values)
        assert result["H"] == result["sharp_upper_bound"]
        assert result["average_degree"] < 2


def test_two_layer_reduction_has_only_one_scalable_type():
    certificate = two_layer_reduction_certificate()
    assert certificate["scalable_type"]["b"] == 0
    assert certificate["scalable_type"]["d"] == -1
    assert len(certificate["exceptional"]) == 4


def test_multistar_cube_has_exact_logarithmic_certificate():
    for k in range(1, 6):
        result = multistar_cube_certificate(k, side_length=2)
        assert result["n"] == 2 * 4**k
        assert result["certified_average_degree"] == 1 + Fraction(k, 4)
        assert result["exact_average_degree"] == result["certified_average_degree"]
        assert result["difference_palette"] == 3 * 9**k
        assert result["certified_H"] > result["n"] ** 2
