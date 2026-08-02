"""Regression tests for the maximum-witness degree-spread barrier."""

from verify_maximum_witness_degree_spread import (
    common_residual_root,
    data,
    degree_cap_lower,
    endpoint_conservation,
    exhaustive_certificate,
    relaxed_degree_cap_lower,
    sharp_endpoint_graph,
    sharp_graph_certificate,
    square_root_certificate,
)


def test_even_and_odd_apparent_endpoint_rows():
    even = data(n=20, delta=8, degree_spread=3)
    assert even["kappa"] == 4
    assert even["residual_root"] == 4
    odd = data(n=21, delta=8, degree_spread=3)
    assert odd["kappa"] == 5
    assert odd["residual_root"] == 4
    assert common_residual_root(20, 8, 1) == 3
    assert common_residual_root(21, 8, 2) == 2
    assert common_residual_root(21, 8, 3) == 3


def test_degree_cap_excludes_apparent_endpoints():
    # Even: m=10, d=3, and the two boundary ranges in (9a).
    assert degree_cap_lower(20, 8, 11, 3, 6) == 96
    assert degree_cap_lower(20, 8, 11, 3, 7) == 97
    assert data(20, 8, 3)["missing"] == 89

    # Odd: the smallest lower bounds in (12a), one for each centre degree.
    assert degree_cap_lower(21, 9, 11, 3, 7) >= 107
    assert degree_cap_lower(21, 8, 11, 4, 7) >= 105
    assert data(21, 8, 3)["missing"] == 99


def test_square_root_scalar_endpoints_are_sharp():
    for g in (4, 7, 20):
        even_delta = g * g - 2 * g - 2
        even_kappa = 2 * g - 2
        even_n = 2 * even_delta + even_kappa
        even_missing = even_n * (even_n - 1) // 2 - even_n**2 // 4 - 1
        assert relaxed_degree_cap_lower(
            even_n, even_delta, g, even_kappa - 1
        ) == even_missing

        odd_delta = g * g - 2 * g - 1
        odd_kappa = 2 * g - 1
        odd_n = 2 * odd_delta + odd_kappa
        odd_missing = odd_n * (odd_n - 1) // 2 - odd_n**2 // 4 - 1
        assert relaxed_degree_cap_lower(
            odd_n, odd_delta, g, odd_kappa - 1
        ) == odd_missing


def test_square_root_factorization_certificate():
    result = square_root_certificate(max_g=80)
    assert result["comparison_rows"] > 0
    assert result["sharp_scalar_endpoint_rows"] == 2 * (80 - 3)
    assert result["pass"]


def test_graph_level_sharp_endpoints():
    even = sharp_endpoint_graph(4, "even")
    assert (even["n"], even["delta"], even["maximum"]) == (18, 6, 10)
    odd = sharp_endpoint_graph(4, "odd")
    assert (odd["n"], odd["delta"], odd["maximum"]) == (21, 7, 11)
    result = sharp_graph_certificate(max_g=20)
    assert result["graph_rows"] == 34
    assert result["pass"]


def test_sharp_graph_repeated_colour_stress_is_reserve_paid():
    for g in (4, 5, 11, 20):
        for parity in ("even", "odd"):
            row = sharp_endpoint_graph(g, parity)
            assert row["repeated_pair_capacity"] >= g
            assert row["recoloured_defect"] == g
            assert row["missing_star_reserve"] >= g


def test_l4_at_first_template_parameter():
    assert sharp_endpoint_graph(5, "even", audit_l4=True)["l4_checked"]
    assert sharp_endpoint_graph(5, "odd", audit_l4=True)["l4_checked"]


def test_degree_spread_two_is_excluded():
    for n, delta in ((20, 9), (21, 9)):
        row = data(n, delta, degree_spread=2)
        assert row["residual_root"] > row["kappa"]


def test_endpoint_conservation_formulas():
    even = endpoint_conservation("even", 7, 2, 0)
    assert even["synchronization"] == 14
    assert even["conserved"] == 7
    assert even["pass"]
    odd = endpoint_conservation("odd", 7, 3, 0, 4)
    assert odd["synchronization"] == 11
    assert odd["conserved"] == 4
    assert odd["pass"]


def test_exhaustive_arithmetic_certificate():
    result = exhaustive_certificate(max_n=250)
    assert result["excluded_g_le_two_rows"] > 0
    assert result["g_three_parameter_rows"] > 0
    assert result["g_three_excluded_scalar_rows"] > 0
    assert result["endpoint_rows"] > 0
    assert result["pass"]
