"""Focused regressions for the independent square-root blind audit."""

from verify_maximum_witness_sqrt_spread_blind_audit import (
    c7_contains_both,
    endpoint_graph,
    firewall_certificate,
    four_charge_certificate,
    graph_geometry_certificate,
    l4_template_certificate,
    n32_certificate,
    recolouring_certificate,
    small_spread_certificate,
    symbolic_certificate,
)


def test_four_disjoint_charges_and_internal_double_count():
    result = four_charge_certificate()
    assert result["four_charge_subgraphs"] > 10_000
    assert result["pass"]


def test_concavity_factorizations_roots_and_scalar_endpoints():
    result = symbolic_certificate(max_g=40)
    assert result["factor_sign_rows"] > 0
    assert result["sharp_scalar_rows"] == 2 * (40 - 3)
    assert result["root_rows"] > 0
    assert result["pass"]


def test_all_small_spread_layers_are_independently_empty():
    result = small_spread_certificate(max_m=80)
    assert result["g_le_two_rows"] > 0
    assert result["even_g_three_rows"] > 0
    assert result["odd_g_three_rows"] > 0
    assert result["pass"]


def test_cyclic_endpoint_geometry_is_rebuilt_independently():
    result = graph_geometry_certificate(max_g=8)
    assert result["endpoint_graphs"] == 10
    assert result["witness_rows"] > 0
    assert result["pass"]


def test_recolouring_recomputes_defect_reserve_and_c7_guard():
    result = recolouring_certificate(max_g=5)
    assert result["recoloured_graphs"] == 4
    assert result["two_edge_colour_classes"] == 18
    assert result["exact_c7_pair_checks"] == 18
    assert result["reserve_witness_rows"] > 0
    assert result["pass"]


def test_no_c7_contains_a_repeated_class_at_first_even_endpoint():
    graph = endpoint_graph(4, "even")
    witness = min(graph["W"])
    x = min(graph["adj"][witness] & graph["P"])
    y = min(graph["adj"][witness] & graph["U"])
    assert not c7_contains_both(
        graph["adj"], (int(graph["b"]), x), (int(graph["c"]), y)
    )


def test_all_eight_l4_templates_survive_two_deletions():
    result = l4_template_certificate()
    assert result["template_endpoint_pairs"] > 1_000
    assert result["template_internal_sets"] > 0
    assert result["pass"]


def test_n32_exact_endpoint_slacks():
    result = n32_certificate(max_g=40)
    assert result["n32_endpoint_rows"] == 2 * (40 - 3)
    assert result["pass"]


def test_public_problem_firewall_is_explicit():
    assert firewall_certificate()["pass"]
