import itertools

import verify_edge_character_synchronization as verifier


def test_exact_six_edge_quotient_counts_and_offsets() -> None:
    certificate = verifier.build_certificate(1260)
    assert certificate["all_external_indices_distinct"]
    assert certificate["external_indices_disjoint_from_original"]
    assert certificate["moduli_gcd"] == 1
    for edge in certificate["edge_certificates"]:
        assert edge["common_sum"] == sum(edge["external_pair"])
        assert edge["offset_difference"] > 0
        assert edge["selected_value_count"] == (
            2 * 1260 // edge["modulus"]
        )
        assert edge["representation_count"] == (
            2 * 1260**2 // edge["modulus"]
        )
        assert edge["average_representation_multiplicity"] == 1260


def test_cycle_is_frustrated_and_gram_identity_is_universal() -> None:
    certificate = verifier.build_certificate(1260)
    assert certificate["transversal_cycle_count_mod_84"] == 0
    assert certificate["gram_identity_exhaustive_on_range_0_4"]


def test_root_reconstruction_for_exact_vertex_potentials() -> None:
    vertices = tuple(range(8))
    modulus = 11
    source_potentials = {
        vertex: (3 * vertex * vertex + 2 * vertex + 5) % modulus
        for vertex in vertices
    }
    edge_labels = {
        (left, right): (
            source_potentials[left] - source_potentials[right]
        )
        % modulus
        for left, right in itertools.combinations(vertices, 2)
    }
    recovered = verifier.reconstruct_potentials(
        vertices, edge_labels, modulus, root=3
    )
    assert verifier.potential_disagreements(
        vertices, edge_labels, recovered, modulus
    ) == 0


def test_one_corrupted_edge_creates_only_one_disagreement() -> None:
    vertices = tuple(range(7))
    modulus = 13
    edge_labels = {
        (left, right): (left - right) % modulus
        for left, right in itertools.combinations(vertices, 2)
    }
    edge_labels[(4, 6)] = (edge_labels[(4, 6)] + 1) % modulus
    recovered = verifier.reconstruct_potentials(
        vertices, edge_labels, modulus, root=0
    )
    assert verifier.potential_disagreements(
        vertices, edge_labels, recovered, modulus
    ) == 1
