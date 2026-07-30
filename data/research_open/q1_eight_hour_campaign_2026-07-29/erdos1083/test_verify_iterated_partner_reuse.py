from fractions import Fraction

import verify_iterated_partner_reuse as verifier


def test_exponential_hubs_are_b4_and_have_unique_differences() -> None:
    certificate = verifier.b4_certificate(9, 4)
    assert certificate["is_b4"]
    assert certificate["difference_count"] == 9 * 8


def test_codegrees_have_exact_two_level_bound() -> None:
    for base, hub_count in ((4, 4), (4, 7), (4, 10), (9, 7)):
        certificate = verifier.codegree_certificate(hub_count, base)
        assert (
            certificate["difference_count"]
            == certificate["expected_difference_count"]
        )
        assert (
            certificate["on_difference_minimum"]
            == certificate["expected_on_difference"]
        )
        assert (
            certificate["on_difference_maximum"]
            == certificate["expected_on_difference"]
        )
        assert (
            certificate["off_difference_maximum"]
            <= certificate["off_difference_bound"]
        )


def test_single_star_has_quadratic_centre_degree_but_global_bound() -> None:
    hub_count = 8
    nodes = verifier.single_star_nodes(hub_count, 4)
    certificate = verifier.graph_certificate(nodes, hub_count, 4)
    assert certificate["maximum_degree"] == hub_count * (hub_count - 1)
    assert certificate["wedge_identity_holds"]
    assert certificate["moment_bound_holds"]
    assert certificate["service_bound_holds"]


def test_parallel_cliques_realize_short_cycles_at_full_layer_capacity() -> None:
    certificate = verifier.parallel_clique_certificate(9, 13, 4)
    assert certificate["maximum_layer_count"] == 13
    assert certificate["expected_layer_count"] == 13
    assert certificate["all_heights_positive"]
    assert certificate["service_count"] == 13 * 9 * 8 // 2
    assert certificate["cycle_checks"] == {4: True, 6: True, 8: True}


def test_anchor_coherent_exponent_beats_required_saving() -> None:
    certificate = verifier.exponent_certificate(1, 30)
    assert certificate["coherent_network_c"] > Fraction(2, 5)
    assert certificate["margin"] > 0
